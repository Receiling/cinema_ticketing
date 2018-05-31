from django import forms

from ticketing.models import Customer, Employee, Movie_comment, Cinema_comment


class MovieCommentForm(forms.ModelForm):
    """电影评价的表单"""
    class Meta:
        model = Movie_comment
        fields = ['comment', 'score']
        labels = {'comment': '评论', 'score': '评分'}
        widgets = {'email': forms.TextInput()}


class CinemaCommentForm(forms.ModelForm):
    """电影评价的表单"""
    class Meta:
        model = Cinema_comment
        fields = ['comment', 'score']
        labels = {'comment': '评论', 'score': '评分'}
        widgets = {'email': forms.TextInput()}
