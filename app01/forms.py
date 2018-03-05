from django.forms import fields, Form, widgets
from django.core.exceptions import ValidationError
from app01 import models


class LoginForm(Form):
    '用户登录Form表单'
    username = fields.CharField(max_length=32, min_length=2, required=True,
                                widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "用户名"}))
    password1 = fields.CharField(max_length=32, min_length=2, required=True,
                                 widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': "密码"}))
    check_code = fields.CharField(widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "验证码"}))

    # remember=fields.ChoiceField(widget=widgets.CheckboxInput)

    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = request  # 将request传入Form类

    def clean_check_code(self):
        '''
        检测验证码是否输入正确
        :return:
        '''
        input_code = self.cleaned_data.get('check_code')
        session_code = self.request.session.get('check_code')
        if input_code == session_code:
            return input_code
        raise ValidationError('验证码错误')

    def clean_username(self):
        '''
        检测用户名是否在数据库中存在
        :return:
        '''
        input_username = self.cleaned_data.get('username')
        if models.UserInfo.objects.filter(username=input_username):
            return input_username
        raise ValidationError('用户名错误！')

    def clean(self):
        '''
        检测用户密码和用户名是否输入正确，明文验证
        :return:
        '''
        username = self.cleaned_data.get('username')
        input_password = self.cleaned_data.get('password1')
        password = None
        if username:
            password = models.UserInfo.objects.filter(username=username).values('password').first()['password']
        if password:
            if password == input_password:
                return self.cleaned_data
        raise ValidationError('用户名或密码错误')


class RegisterForm(Form):
    '用户注册'
    username = fields.CharField(max_length=32, min_length=2, required=True,
                                widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "用户名"}))
    nickname = fields.CharField(max_length=32, min_length=2, required=True,
                                widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "昵称"}))
    email = fields.EmailField(max_length=32, min_length=2, required=True,
                              widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "邮箱"}))
    password = fields.CharField(max_length=32, min_length=2, required=True,
                                widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': "密码"}))
    password2 = fields.CharField(max_length=32, min_length=2, required=True,
                                 widget=widgets.PasswordInput(
                                     attrs={'class': "form-control", 'placeholder': "请再次输入密码"}))
    check_code = fields.CharField(widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "验证码"}))
    avatar = fields.ImageField(
        widget=widgets.FileInput(attrs={'class': 'user_avatar', 'style': "position: absolute;right: -460px;opacity:0"}),
        required=False)

    # remember=fields.ChoiceField(widget=widgets.CheckboxInput)

    def __init__(self, request, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        username_input = self.cleaned_data.get('username')
        if models.UserInfo.objects.filter(username=username_input).values(
                'username').first() == None:  # 如果用户已经注册过
            return username_input
        raise ValidationError('该用户已注册')

    def clean_check_code(self):
        input_code = self.cleaned_data.get('check_code')
        session_code = self.request.session.get('check_code')
        if input_code.upper() == session_code:
            return input_code
        raise ValidationError('验证码错误')

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 == password2:
            return self.cleaned_data
        self.add_error('password2', ValidationError('密码不一致'))


class Update_userinfo(Form):
    '修改用户信息'
    username = fields.CharField(max_length=32, min_length=2, required=True,
                                widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "用户名"}))
    nickname = fields.CharField(max_length=32, min_length=2, required=True,
                                widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "昵称"}))
    email = fields.EmailField(max_length=32, min_length=2, required=True,
                              widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "邮箱"}))
    password = fields.CharField(max_length=32, min_length=2, required=True,
                                widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': "密码"}))
    password2 = fields.CharField(max_length=32, min_length=2, required=True,
                                 widget=widgets.PasswordInput(
                                     attrs={'class': "form-control", 'placeholder': "请再次输入密码"}))
    check_code = fields.CharField(widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "验证码"}))
    avatar = fields.ImageField(
        widget=widgets.FileInput(attrs={'class': 'user_avatar', 'style': "position: absolute;right: -460px;opacity:0"}),
        required=False)

    # remember=fields.ChoiceField(widget=widgets.CheckboxInput)

    def __init__(self, request, *args, **kwargs):
        super(Update_userinfo, self).__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        session_subtitle = self.request.session.get('subtitle')
        user_obj = models.UserInfo.objects.filter(blog__subtitle=session_subtitle).values('nid').first()
        input_username = self.cleaned_data.get('username')
        input_user_id = models.UserInfo.objects.filter(username=input_username).values('nid').first().get('nid')
        if input_user_id != None and input_user_id != user_obj.get('nid'):
            raise ValidationError('该用户名已经存在')
        return input_username

    def clean_check_code(self):
        input_code = self.cleaned_data.get('check_code')
        session_code = self.request.session.get('check_code')
        if input_code.upper() == session_code:
            return input_code
        raise ValidationError('验证码错误')

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 == password2:
            print('密码一致')
            return self.cleaned_data
        self.add_error('password2', ValidationError('密码不一致'))


class Tag_Form(Form):
    '标签表单'
    tag = fields.CharField(min_length=2, max_length=32, required=True)


class Category_Form(Form):
    '文章目录表单'
    category = fields.CharField(min_length=2, max_length=32, required=True)


class Article_Form(Form):
    '文章表单'
    title = fields.CharField(min_length=2, required=True, max_length=256)
    abstract = fields.CharField(min_length=2, required=True, max_length=256)
    content = fields.CharField(widget=widgets.Textarea, required=True)
    category = fields.ChoiceField(widget=widgets.RadioSelect)
    tag = fields.MultipleChoiceField(widget=widgets.CheckboxSelectMultiple)
    article_type_id = fields.ChoiceField(widget=widgets.RadioSelect,
                                         choices=[(1, 'Python'), (2, 'GOlang'), (3, 'Linux'), (4, 'OpenStack'), ])

    def __init__(self, request, subtitle, *args, **kwargs):
        super(Article_Form, self).__init__(*args, **kwargs)
        self.request = request
        self.subtitle = subtitle
        self.fields['category'].choices = models.Category.objects.filter(blog__subtitle=subtitle).all().values_list(
            'cid', 'title')
        self.fields['tag'].choices = models.Tag.objects.filter(blog__subtitle=subtitle).all().values_list('tid',
                                                                                                          'title')
