# l = [{'id': 1, 'content': '写的太好了', 'parent_id': None, 'child': [{'id': 4, 'content': '你眼瞎吗', 'parent_id': 1, 'child': [
#     {'id': 5, 'content': '我看是', 'parent_id': 4,
#      'child': [{'id': 7, 'content': '你是没呀', 'parent_id': 5, 'child': []}]}]}]},
#      {'id': 2, 'content': '你说得对', 'parent_id': None,
#       'child': [{'id': 6, 'content': '鸡毛', 'parent_id': 2, 'child': []}]},
#      {'id': 3, 'content': '顶楼上', 'parent_id': None,
#       'child': [{'id': 8, 'content': '惺惺惜惺惺想寻', 'parent_id': 3, 'child': []}]}]
#
#
# def comment_tree(comment_list):
#     comment_str = "<div class='comment'>"
#     for row in comment_list:
#         tpl = "<div class='content'>%s</div>" % (row['content'])
#         comment_str += tpl
#         if row['child']:
#             child_str = comment_tree(row['child'])
#             comment_str += child_str
#     comment_str += "</div>"
#     return comment_str
#
#
# result = comment_tree(l)
# print(result)
# import datetime
# x=[{'id': 1, 'username': '朱广飞', 'content': '写得好',
#   'create_time': datetime.datetime(2017, 12, 26, 23, 30, 18, tzinfo= < UTC >), 'parent_id': None, 'child': [
#     {'id': 2, 'username': '王华华', 'content': '垃圾吧',
#      'create_time': datetime.datetime(2017, 12, 26, 23, 30, 40, tzinfo= < UTC >), 'parent_id': 1, 'child': [
#     {'id': 3, 'username': '朱广飞', 'content': '去你大爷，你行你上啊',
#      'create_time': datetime.datetime(2017, 12, 26, 23, 31, 24, tzinfo= < UTC >), 'parent_id': 2, 'child': []}]}]}, {
#     'id': 2, 'username': '王华华', 'content': '垃圾吧',
#     'create_time': datetime.datetime(2017, 12, 26, 23, 30, 40, tzinfo= < UTC >), 'parent_id': 1, 'child': [
#     {'id': 3, 'username': '朱广飞', 'content': '去你大爷，你行你上啊',
#      'create_time': datetime.datetime(2017, 12, 26, 23, 31, 24, tzinfo= < UTC >), 'parent_id': 2, 'child': []}]}, {
#     'id': 3, 'username': '朱广飞', 'content': '去你大爷，你行你上啊', 'create_time': datetime.datetime(2017, 12, 26, 23, 31, 24,
#                                                                                           tzinfo= < UTC >), 'parent_id': 2, 'child': []}] msg_list, ---------------------------
