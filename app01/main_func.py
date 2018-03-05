from django.shortcuts import HttpResponse, render, redirect
from app01 import models
from app01 import forms
from django.db.models import F, Count, Q


def my_blog(request, *args, **kwargs):
    # 个人博客主页,博客详细页
    # 获取博客文章列表
    main_info = {}  # 定义一个空列表，里面存放传入前端的数据
    subtitle = kwargs.get('subtitle')
    blog = models.Blog.objects.filter(subtitle=subtitle).first()
    # 获取文章列表
    article_list = models.Articles.objects.filter(blog__subtitle=subtitle).all()
    main_info['article_list'] = article_list
    # 获取文章分类列表
    category_list = models.Articles.objects.filter(blog__subtitle=subtitle).values('category_id',
                                                                                   'category__title').annotate(
        c=Count('aid'))
    main_info['category_list'] = category_list
    # 获取标签分类列表
    tags_list = models.Articles2Tag.objects.filter(article__blog__subtitle=subtitle).values('tag_id',
                                                                                            'tag__title').annotate(
        c=Count('id'))
    main_info['tags_list'] = tags_list
    # 获取按日期分类的
    date_list = models.Articles.objects.filter(blog__subtitle=subtitle).extra(
        select={'ctime': "date_format(release_time,'%%Y-%%m')"}).values('ctime').annotate(ct=Count('aid'))
    # date_list=models.Articles.objects.filter(blog__subtitle=subtitle).extra(
    #     select={'ctime':"strftime('%%Y-%%m',release_time)"}).values('ctime').annotate(c=Count('aid')) 这个用于sqllite数据库，mysql需要使用自己的时间日期函数
    main_info['date_list'] = date_list
    main_info['blog'] = blog
    # 需要添加分页————————————————————————————————————
    return render(request, 'my_blog.html', {'main_info': main_info, 'subtitle': subtitle})


from app01.views import login_decorate
import json

from django.db import transaction


@login_decorate
def like(request, *args, **kwargs):
    '点赞或者点踩 True赞，False踩，done已经赞过或踩过，wrong出错了'
    info_dict = {'count_num': 0, 'status': 'false'}
    received_data = request.POST
    like_dict = {}
    user = models.UserInfo.objects.filter(blog__subtitle=kwargs.get('subtitle')).first()  # 点赞或踩的用户
    article = models.Articles.objects.filter(aid=int(received_data.get('aid'))).first()  # 被点赞或踩的文章
    like_dict['user'] = user
    like_dict['article'] = article
    try:
        if models.Like.objects.filter(article=article, user=user).values('lid').first() != None:  # 如果查询到说明已经点过赞或踩了
            info_dict['status'] = 'done'  # 操作过了
        else:
            with transaction.atomic():
                if received_data.get('val') == '1':
                    like_dict['like'] = True
                    models.Like.objects.create(**like_dict)
                    models.Articles.objects.filter(aid=int(received_data.get('aid'))).update(
                        like_count=F('like_count') + 1)
                    like_count = models.Articles.objects.filter(aid=int(received_data.get('aid'))).values(
                        'like_count').first()
                    info_dict['status'] = 'true'
                    info_dict['count_num'] = like_count.get('like_count')
                else:
                    like_dict['like'] = False
                    models.Like.objects.create(**like_dict)
                    models.Articles.objects.filter(aid=int(received_data.get('aid'))).update(
                        like_count=F('dislike_count') + 1)
                    dislike_count = models.Articles.objects.filter(aid=int(received_data.get('aid'))).values(
                        'dislike_count').first()
                    info_dict['count_num'] = dislike_count.get('dislike_count')
                    info_dict['status'] = 'false'
    except Exception as e:
        info_dict['status'] = 'wrong'
    return HttpResponse(json.dumps(info_dict))


def blog_mainpage(request, *args, **kwargs):
    '按文章类型 type_id显示文章 ---------博客网主页'
    # 如果用户登录，则获取用户session中的subtitle
    main_info = {}
    # aid=kwargs.get('aid')
    aid = int(kwargs.get('aid')) if kwargs.get('aid') else None
    if aid:
        article_list = models.Articles.objects.filter(article_type_id=aid).all()
    else:
        article_list = models.Articles.objects.filter().all()
    article_type_list = models.Articles.article_type_choices
    if request.session.get('subtitle'):
        blog = models.Blog.objects.filter(subtitle=request.session.get('subtitle')).values('title', 'subtitle').first()
        main_info['blog'] = blog
    main_info['article_list'] = article_list
    main_info['article_type_list'] = article_type_list
    main_info['type_id'] = aid
    # 需要添加分页————————————————————————————————————
    return render(request, 'blog_mainpage.html', {'main_info': main_info})


@login_decorate
def add_tags_category(request, *args, **kwargs):
    '添加标签'
    # 显示所有标签和分类
    blog_subtitle = kwargs.get('subtitle')
    blog = models.Blog.objects.filter(subtitle=blog_subtitle).first()
    tags_list = models.Tag.objects.filter(blog__subtitle=blog_subtitle).all()
    category_list = models.Category.objects.filter(blog__subtitle=blog_subtitle).all()
    main_info = {}
    main_info['blog'] = blog
    main_info['tags_list'] = tags_list
    main_info['category'] = category_list
    if request.method == "GET":
        tags_form = forms.Tag_Form()
        main_info['tags_form'] = tags_form
        category_form = forms.Category_Form()
        main_info['category_form'] = category_form
        return render(request, 'add_tags_category.html', {'main_info': main_info, 'subtitle': blog_subtitle})
    else:
        if request.POST.get('type') == 'tag_type':
            tags_form = forms.Tag_Form(request.POST)
            main_info['tags_form'] = tags_form
            category_form = forms.Category_Form()
            main_info['category_form'] = category_form
            if tags_form.is_valid():
                models.Tag.objects.create(blog=blog, title=tags_form.cleaned_data.get('tag'))
                return redirect('/add_tags_category/' + blog_subtitle)
            else:
                return render(request, 'add_tags_category.html', {'main_info': main_info, 'subtitle': blog_subtitle})
        else:
            tags_form = forms.Tag_Form()
            main_info['tags_form'] = tags_form
            category_form = forms.Category_Form(request.POST)
            main_info['category_form'] = category_form
            if category_form.is_valid():
                models.Category.objects.create(blog=blog, title=category_form.cleaned_data.get('category'))
                return redirect('/add_tags_category/' + blog_subtitle)
            else:
                return render(request, 'add_tags_category.html', {'main_info': main_info, 'subtitle': blog_subtitle})


@login_decorate
def edit_tag(request, *args, **kwargs):
    '修改标签'
    if request.POST.get('title') == '':
        return HttpResponse(json.dumps({'status': False}))
    else:
        models.Tag.objects.filter(tid=int(request.POST.get('tid'))).update(title=request.POST.get('title'))
        return HttpResponse(json.dumps({'status': True}))


@login_decorate
def edit_category(request, *args, **kwargs):
    '修改分类'
    if request.POST.get('title') == '':
        return HttpResponse(json.dumps({'status': False}))
    else:
        models.Category.objects.filter(cid=int(request.POST.get('cid'))).update(title=request.POST.get('title'))
        return HttpResponse(json.dumps({'status': True}))


@login_decorate
def delete_tag(request, *args, **kwargs):
    '修改分类'
    if request.POST.get('tid') != "":
        try:
            models.Tag.objects.filter(tid=int(request.POST.get('tid'))).delete()
            return HttpResponse(json.dumps({'status': True}))
        except Exception:
            return HttpResponse(json.dumps({'status': False}))
    else:
        return HttpResponse(json.dumps({'status': False}))


def delete_category(request, *args, **kwargs):
    '修改分类'
    if request.POST.get('cid') != "":
        try:
            models.Category.objects.filter(cid=int(request.POST.get('cid'))).delete()
            return HttpResponse(json.dumps({'status': True}))
        except Exception:
            return HttpResponse(json.dumps({'status': False}))
    else:
        return HttpResponse(json.dumps({'status': False}))


@login_decorate
def add_article(request, *args, **kwargs):
    '添加博客文章'
    blog_subtitle = kwargs.get('subtitle')
    blog = models.Blog.objects.filter(subtitle=blog_subtitle).first()
    main_info = {}
    main_info['blog'] = blog
    if request.method == "GET":
        article_form = forms.Article_Form(request, blog_subtitle)
        return render(request, 'add_article.html',
                      {'main_info': main_info, 'subtitle': blog_subtitle, 'article_form': article_form})
    else:
        article_form = forms.Article_Form(request, blog_subtitle, request.POST)
        if article_form.is_valid():
            # 将数据写入数据库-------
            data_dict = {}
            data_dict['title'] = article_form.cleaned_data['title']
            data_dict['abstract'] = article_form.cleaned_data['abstract']
            data_dict['category'] = models.Category.objects.filter(
                cid=int(article_form.cleaned_data['category'])).first()
            data_dict['article_type_id'] = int(article_form.cleaned_data['article_type_id'])
            data_dict['blog'] = blog
            article_obj = models.Articles.objects.create(**data_dict)
            # 将详细信息存入article_detail表中
            models.Articel_Detail.objects.create(content=article_form.cleaned_data['content'], article=article_obj)
            # 将标签与文章的关系存入到Article2Tag表中
            for tag_item in article_form.cleaned_data['tag']:
                models.Articles2Tag.objects.create(article=article_obj,
                                                   tag=models.Tag.objects.filter(tid=int(tag_item)).first())
            return redirect('/my_blog/' + blog_subtitle)
        else:
            return render(request, 'add_article.html',
                          {'main_info': main_info, 'subtitle': blog_subtitle, 'article_form': article_form})


from app01.comment import show_comment


def article_page(request, *args, **kwargs):
    '文章最终页'
    aid = kwargs.get('aid')
    blog_subtitle = request.session.get('subtitle')
    article_obj = models.Articles.objects.filter(aid=aid).first()
    comment_list = models.Comment.objects.filter(article_id=aid).values('cid', 'user__username', 'comments',
                                                                        'create_time', 'father_cid__cid').all()

    if comment_list:
        msg_list = []
        for item in comment_list:
            print(item, item.get('cid'), type(item.get('cid')), item.get('comments'), 'item------')
            msg_dict = {}
            msg_dict['id'] = item.get('cid')
            msg_dict['username'] = item.get('user__username')
            msg_dict['content'] = item.get('comments')
            msg_dict['create_time'] = item.get('create_time')
            msg_dict['parent_id'] = item.get('father_cid__cid')
            msg_list.append(msg_dict)
        comment_str = show_comment(msg_list)
    else:
        comment_str = '<div>暂无评论，请添加评论~~</div>'
    if blog_subtitle:
        blog = models.Blog.objects.filter(subtitle=blog_subtitle).first()
        main_info = {}
        main_info['blog'] = blog
        return render(request, 'article_page.html',
                      {'article_obj': article_obj, 'main_info': main_info, 'comment': comment_str})
    return render(request, 'article_page.html', {'article_obj': article_obj, 'comment': comment_str})


@login_decorate
def edite_article(request, *args, **kwargs):
    '编辑博客文章'
    aid = int(kwargs.get('aid'))
    article_obj1 = models.Articles.objects.filter(aid=aid).first()
    blog_subtitle = request.session.get('subtitle')
    blog = models.Blog.objects.filter(subtitle=blog_subtitle).first()
    main_info = {}
    main_info['blog'] = blog
    data_dict = {}
    if request.method == "GET":
        data_dict['title'] = article_obj1.title
        data_dict['abstract'] = article_obj1.abstract
        data_dict['category'] = article_obj1.category.cid
        data_dict['article_type_id'] = article_obj1.article_type_id
        tags_list = models.Articles2Tag.objects.filter(article=article_obj1).all()

        tags_list_tosend = []
        for tag_item in tags_list:
            tags_list_tosend.append(tag_item.tag.tid)
        data_dict['tag'] = tags_list_tosend
        data_dict['content'] = models.Articel_Detail.objects.filter(article=article_obj1).first().content
        article_form = forms.Article_Form(request, blog_subtitle, data_dict)

        return render(request, 'edite_article.html',
                      {'main_info': main_info, 'article_form': article_form, 'subtitle': blog_subtitle})
    else:
        article_form = forms.Article_Form(request, blog_subtitle, request.POST)
        if article_form.is_valid():
            # 将数据写入数据库-------
            data_dict1 = {}
            data_dict1['title'] = article_form.cleaned_data['title']
            data_dict1['abstract'] = article_form.cleaned_data['abstract']
            data_dict1['category'] = models.Category.objects.filter(
                cid=int(article_form.cleaned_data['category'])).first()
            data_dict1['article_type_id'] = int(article_form.cleaned_data['article_type_id'])
            data_dict1['blog'] = blog
            models.Articles.objects.filter(aid=aid).update(**data_dict1)
            # 将详细信息存入article_detail表中
            models.Articel_Detail.objects.filter(article=article_obj1).update(
                content=article_form.cleaned_data['content'])
            # 将标签与文章的关系存入到Article2Tag表中
            for tag_item in article_form.cleaned_data['tag']:
                models.Articles2Tag.objects.filter(article=article_obj1).update(
                    tag=models.Tag.objects.filter(tid=int(tag_item)).first())
            return redirect('/my_blog/' + blog_subtitle)
        else:
            return render(request, 'edite_article.html',
                          {'main_info': main_info, 'subtitle': blog_subtitle, 'article_form': article_form})


@login_decorate
def delete_article(request, *args, **kwargs):
    '删除博客的文章'
    aid = int(kwargs.get('aid'))
    blog_subtitle = request.session.get('subtitle')
    from django.db import transaction
    with transaction.atomic():
        models.Articles2Tag.objects.filter(article_id=aid).delete()  # 删除关联的标签
        models.Like.objects.filter(article_id=aid).delete()  # 删除点赞表的记录
        # models.Comment.objects.filter(article_id=aid).delete()  #删除评论表的记录
        models.Articel_Detail.objects.filter(article_id=aid).delete()  # 删除文章详细内容表中的数据
        models.Articles.objects.filter(aid=aid).delete()  # 删除博客文章
    return redirect('/my_blog/' + blog_subtitle)


@login_decorate
def filter(request, *args, **kwargs):
    '查看各种'
    main_info = {}  # 定义一个空列表，里面存放传入前端的数据
    subtitle = kwargs.get('subtitle')
    blog = models.Blog.objects.filter(subtitle=subtitle).first()
    main_info['blog'] = blog
    key = kwargs.get('key')
    val = kwargs.get('val')
    if key == 'category':
        article_list = models.Articles.objects.filter(blog__subtitle=subtitle, category_id=int(val)).all()
    elif key == 'tag':
        article_list = models.Articles.objects.filter(blog__subtitle=subtitle, articles2tag__tag_id=int(val)).all()
    else:
        article_list = models.Articles.objects.filter(blog__subtitle=subtitle).extra(
            where=["date_format(release_time,'%%Y-%%m')=%s"], params=[val, ])
    main_info['article_list'] = article_list
    return render(request, 'filter.html', {'main_info': main_info, 'subtitle': subtitle})


@login_decorate
def search(request, *args, **kwargs):
    '搜索博客文章，按大分类，个人分类，个人标签，时间'
    condition = {}
    subtitle = request.session.get('subtitle')
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v
    type_list = models.Articles.article_type_choices
    category_list = models.Category.objects.filter(blog__subtitle=subtitle).all()
    tags_list = models.Tag.objects.filter(blog__subtitle=subtitle).all()
    condition['blog__subtitle'] = subtitle
    article_list = models.Articles.objects.filter(**condition).all()
    main_info = {}
    main_info['article_list'] = article_list
    return render(request, 'search_articles.html',
                  {'main_info': main_info, 'kwargs': kwargs, 'type_list': type_list, 'category_list': category_list,
                   'tags_list': tags_list})


@login_decorate
def reset_profile(request, *args, **kwargs):
    '重新设置个人信息'
    subtitle = request.session.get('subtitle')
    main_info = {}
    blog = models.Blog.objects.filter(subtitle=subtitle).first()
    main_info['blog'] = blog
    user_obj = models.UserInfo.objects.filter(blog__subtitle=subtitle).values('username', 'nickname', 'email',
                                                                              'avatar', 'nid').first()
    if request.method == "GET":
        register_form = forms.Update_userinfo(request, user_obj)
        return render(request, 'reset_profile.html', {'register_form': register_form, 'main_info': main_info})
    else:
        register_form = forms.Update_userinfo(request, request.POST, request.FILES)
        if register_form.is_valid():
            print('------用户提交的数据')
            print(register_form.cleaned_data)
            print('-------获取session 中的验证码')
            print(request.session.get('check_code'))
            user_info_dict = register_form.cleaned_data
            # 用户注册数据正确，将数据提交到数据库中
            user_info_dict.pop('password2')
            user_info_dict.pop('check_code')
            if user_info_dict.get('avatar') == None:
                user_info_dict.pop('avatar')
            print(user_info_dict)
            models.UserInfo.objects.filter(blog__subtitle=subtitle).update(**user_info_dict)
            return redirect('/my_blog/' + subtitle)
        else:
            return render(request, 'reset_profile.html', {'register_form': register_form, 'main_info': main_info})


def add_comment(request, *args, **kwargs):
    '添加评论，在文章最终页的末尾添加评论'
    info_dict = {'status': 'false'}
    received_data = request.POST
    subtitle = request.session.get('subtitle')
    if subtitle == None:
        info_dict['status'] = 'login'
        return HttpResponse(json.dumps(info_dict))
    if received_data.get('comment') != '':
        if received_data.get('cid') != '':
            models.Comment.objects.create(
                father_cid=models.Comment.objects.filter(cid=int(received_data.get('cid'))).first()
                , article=models.Articles.objects.filter(aid=int(received_data.get('article_id'))).first(),
                comments=received_data.get('comment'),
                user=models.UserInfo.objects.filter(blog__subtitle=subtitle).first())
        else:  # 如果没有父级 id
            models.Comment.objects.create(
                article=models.Articles.objects.filter(aid=int(received_data.get('article_id'))).first(),
                comments=received_data.get('comment'),
                user=models.UserInfo.objects.filter(blog__subtitle=subtitle).first())
        info_dict['status'] = 'true'
    return HttpResponse(json.dumps(info_dict))


def logout(request):
    request.session.delete("subtitle")
    request.session.set_expiry(1)
    return redirect('/login/')
