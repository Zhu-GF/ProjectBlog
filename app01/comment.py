

def comment_tree(comment_list):
    comment_str = "<div class='comment'>"
    for row in comment_list:
        tpl = "<div class='content'>%s: <span>%s</span> <a onclick='input_comment_id(this,%s);'>评论</a></div>" %(row['username'],row['content'],row['id'])
        comment_str += tpl
        if row['child']:
            child_str = comment_tree(row['child'])
            comment_str += child_str
    comment_str += "</div>"
    return comment_str

def show_comment(msg_list,*args,**kwargs):
    '展示评论，在文章最终页显示评论'
    #aid #文章id
    try:
    #     msg_list = [
    #     {'id': 1, 'content': '写的太好了', 'parent_id': None},
    #     {'id': 2, 'content': '你说得对', 'parent_id': None},
    #     {'id': 3, 'content': '顶楼上', 'parent_id': None},
    #     {'id': 4, 'content': '你眼瞎吗', 'parent_id': 1},
    #     {'id': 5, 'content': '我看是', 'parent_id': 4},
    #     {'id': 6, 'content': '鸡毛', 'parent_id': 2},
    #     {'id': 7, 'content': '你是没呀', 'parent_id': 5},
    #     {'id': 8, 'content': '惺惺惜惺惺想寻', 'parent_id': 3},
    # ]
    #目标 (多添加一个child键 ：msg_list_dict={1:{'id': 1, 'content': '写的太好了', 'parent_id': None,'child':[]},2:{'id': 2, 'content': '你说得对', 'parent_id': None,'child':[]},}
        msg_list_dict={}
        for item in msg_list:
            item['child']=[]
            msg_list_dict[item['id']]=item         #将msg_list变成上面的数据结构，新增一个child键
        # msg_list_dict = {
        #     1: {'id': 1, 'content': '写的太好了', 'parent_id': None},
        #     2: {'id': 2, 'content': '你说得对', 'parent_id': None},
        #     3: {'id': 3, 'content': '顶楼上', 'parent_id': None},
        #     4: {'id': 4, 'content': '你眼瞎吗', 'parent_id': 1},
        #     5: {'id': 5, 'content': '我看是', 'parent_id': 4},
        #     6: {'id': 6, 'content': '鸡毛', 'parent_id': 2},
        #     7: {'id': 7, 'content': '你是没呀', 'parent_id': 5},
        #     8: {'id': 8, 'content': '惺惺惜惺惺想寻', 'parent_id': 3},
        # }  # 这个是变化后的数据结构
        result=[]   #目标列表，将child添加到该列表中
        for item in msg_list:
            pid = item['parent_id']
            if pid:
                msg_list_dict[pid]['child'].append(item)
            else:
                result.append(item)
        response=comment_tree(result)
        print('目标数据',result)
    except Exception as e:
        print(e,'异常了')
        response='<div>暂无评论，请添加评论</div>'
    return response



    # to_show_list=[
    #     {'id': 1, 'content': '写的太好了', 'parent_id': None,
    #      'childeren':[{'id': 4, 'content': '你眼瞎吗', 'parent_id': 1,'childeren':[{'id': 5, 'content': '我看是', 'parent_id': 4},]},]}
    # ]   目标数据结构
