from django import forms

from ticketing.models import Cinema, Session


class CinemaInfoForm(forms.ModelForm):
    """修改影院信息的表单"""
    class Meta:
        model = Cinema
        exclude = ['cinema_id', 'score']


class SessionFrom(forms.ModelForm):
    """场次安排"""
    class Meta:
        model = Session
        fields = ['movie_id', 'house_id', 'date', 'time', 'price']
        labels = {'movie_id': '电影', 'house_id': '放映厅', 'date': '日期', 'time': '时间', 'price': '价格'}
        widgets = {'date': forms.DateTimeInput(attrs={'type': 'date'}),
                   'time': forms.DateTimeInput(attrs={'type': 'time'})}