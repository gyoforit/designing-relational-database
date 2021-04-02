from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ('user', 'like_users',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'maxlength': 200,
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ('content',)