"""
Созданы формы для редактирования профиля,
создания поста и добавления комментария.
Связано с требованиями: 2.2., 2.3., 2.8.
"""
from django import forms
from .models import Post, User, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'post', 'created_at',)
