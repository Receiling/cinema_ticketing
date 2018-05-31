from django import forms

from ticketing.models import Customer, Employee


class CustomerLoginForm(forms.ModelForm):
    class Meta:
        # 此种方法无法在页面上正常显示
        # email = forms.CharField(label='邮箱',
        #                         required=True,
        #                         error_messages={'required': u'邮箱不能为空', 'invalid': u'邮箱格式错误'},
        #                         widget=forms.EmailInput())
        # password = forms.CharField(label='密码',
        #                            required=True,
        #                            max_length=50, min_length=6,
        #                            error_messages={'required': '密码不能为空', 'min_length': '密码最少为6个字符'},
        #                            widget=forms.PasswordInput())
        model = Customer
        fields = ['username', 'password']
        labels = {'username': '用户名', 'password': '密码'}
        widgets = {'email': forms.CharField(), 'password': forms.PasswordInput()}


class EmployeeLoginForm(forms.ModelForm):
    class Meta:
        # 此种方法无法在页面上正常显示
        # email = forms.CharField(label='邮箱',
        #                         required=True,
        #                         error_messages={'required': u'邮箱不能为空', 'invalid': u'邮箱格式错误'},
        #                         widget=forms.EmailInput())
        # password = forms.CharField(label='密码',
        #                            required=True,
        #                            max_length=50, min_length=6,
        #                            error_messages={'required': '密码不能为空', 'min_length': '密码最少为6个字符'},
        #                            widget=forms.PasswordInput())
        model = Employee
        fields = ['username', 'password']
        labels = {'username': '用户名', 'password': '密码'}
        widgets = {'email': forms.CharField(), 'password': forms.PasswordInput()}


class EmployeeRegisterForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['']


class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['']

