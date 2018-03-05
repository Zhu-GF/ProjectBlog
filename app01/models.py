from django.db import models


# Create your models here.
class UserInfo(models.Model):
    '用户表'
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    nickname = models.CharField(max_length=32, verbose_name='用户昵称')
    password = models.CharField(max_length=32, verbose_name='用户密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    avatar = models.ImageField(verbose_name='头像', upload_to='avatar/', default='/pictures/upload/avatar/3.jpg')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')
    fan = models.ManyToManyField(to='UserInfo', through='UserFans', related_name='f',
                                 through_fields=('user', 'follower'), verbose_name='关联粉丝')

    def __str__(self):
        return self.username


class UserFans(models.Model):
    '粉丝表，与用户表互关联'
    user = models.ForeignKey(to='UserInfo', to_field='nid', related_name='master', verbose_name='博主id')
    follower = models.ForeignKey(to='UserInfo', to_field='nid', related_name='followers', verbose_name='粉丝id')

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]


class Blog(models.Model):
    '每个用户至多一个博客'
    bid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='博客标题')
    subtitle = models.CharField(max_length=32, verbose_name='博客后缀，站点')
    theame = models.CharField(max_length=32, verbose_name='博客主题')
    user = models.OneToOneField(to='UserInfo', to_field='nid')

    def __str__(self):
        return self.title


class Category(models.Model):
    '用户文章分类表'
    cid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='博客分类的标题')
    blog = models.ForeignKey(to='Blog', to_field='bid', verbose_name='博客下的分类')

    def __str__(self):
        return self.title


class Articel_Detail(models.Model):
    '文章详细内容'
    content = models.TextField(verbose_name='文章详细内容')
    article = models.OneToOneField(to='Articles', to_field='aid', verbose_name='关联文章')

    def __str__(self):
        return self.article.title


class Articles(models.Model):
    '博客文章表'
    aid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128, verbose_name='文章标题')
    abstract = models.CharField(max_length=256, verbose_name='摘要')
    release_time = models.DateTimeField(auto_now_add=True, verbose_name='文章发布时间')
    read_count = models.IntegerField(verbose_name='阅读个数', default=0)
    blog = models.ForeignKey(to='Blog', to_field='bid', verbose_name='关联博客')
    category = models.ForeignKey(to='Category', to_field='cid', verbose_name='关联博客分类')
    like_count = models.IntegerField(default=0, verbose_name='喜欢文章的赞的数目')
    dislike_count = models.IntegerField(default=0, verbose_name='不喜欢文章的数目')
    comments_count = models.IntegerField(default=0, verbose_name='评论的个数')
    tag = models.ManyToManyField(to='Tag', through='Articles2Tag', through_fields=('article', 'tag'),
                                 verbose_name='关联标签')
    article_type_choices = [(1, 'Python'), (2, 'GOlang'), (3, 'Linux'), (4, 'OpenStack'), ]
    article_type_id = models.IntegerField(choices=article_type_choices, default=None)

    def __str__(self):
        return self.title


class Articles2Tag(models.Model):
    '建立中间表，文章表和标签表'
    article = models.ForeignKey(to='Articles', to_field='aid', verbose_name='关联文章')
    tag = models.ForeignKey(to='Tag', to_field='tid', verbose_name='关联标签', related_name='tags')

    # 文章和标签要联合唯一，防止有两条相同的文章和标签
    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        return self.article.title


class Like(models.Model):
    '点赞的'
    lid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(to='Articles', to_field='aid', verbose_name='关联文章')
    user = models.ForeignKey(to='UserInfo', to_field='nid', verbose_name='关联点赞用户')
    like = models.BooleanField(verbose_name='是否喜欢')


class Comment(models.Model):
    '评论'
    cid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(to='Articles', to_field='aid', verbose_name='关联文章')
    user = models.ForeignKey(to='UserInfo', to_field='nid', verbose_name='给出此评论的用户')
    comments = models.CharField(max_length=256, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True)
    father_cid = models.ForeignKey(to='Comment', to_field='cid', verbose_name='父comment id', related_name='Father_cid',
                                   blank=True, null=True)


class Tag(models.Model):
    '文章标签'
    tid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='文章标签')
    blog = models.ForeignKey(to='Blog', to_field='bid')

    def __str__(self):
        return self.title
