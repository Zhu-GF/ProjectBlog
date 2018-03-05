import random
from PIL import ImageFont,Image,ImageDraw
def verfication_code(width=120,height=30,char_length=5,font_file=None,font_size=28,color=(255,255,255)):
    """

    :param width: 验证码图片宽度
    :param height: 验证码图片高度
    :param char_length: 验证码字符数目
    :param font_file: 字体文件路径
    :param font_size: 字体大小
    :return:
    """
    def random_color():
        """
        随机颜色
        :return:
        """
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    def random_char():
        """
        随机字母或数字
        :return:
        """
        res = random.choice([str(random.randint(0, 9)), chr(random.randint(60, 90))])
        return res
    def random_cordinate():
        """
        生成随机坐标，返列表
        :return:
        """
        return [random.randint(0,width),random.randint(0,width)]
    def random_disturbing(img_obj):
        """
        干扰点，线，弧
        :return:
        """
        draw_obj = ImageDraw.Draw(img_obj, 'RGB')  # 画笔对象
        for i in range(10):
            draw_obj.point(random_cordinate(),fill=random_color())
        for i in range(2):
            draw_obj.line(random_cordinate()+random_cordinate(),fill=random_color())
        for i in range(2):
            draw_obj.arc(random_cordinate()+random_cordinate(),random.randint(0,360),random.randint(0,360),fill=random_color())
        return draw_obj
    #将随机字符写入图片
    code_list = []
    img_obj = Image.new(mode='RGB', size=(width, height), color=color)  # 验证码 图形对象
    if font_file:
        font = ImageFont.truetype(font_file, font_size)
        print(font_size)
    else:
        font=None
    for i in range(char_length):
        draw_obj_new=random_disturbing(img_obj=img_obj)
        char=random_char()
        code_list.append(char)
        if font:
            draw_obj_new.text([i * width / char_length, random.randint(0,4)],char,font=font,fill=random_color())
        else:
            draw_obj_new.text([i * width / char_length, random.randint(0, 4)], char,
                             fill=random_color())
    return img_obj,''.join(code_list)