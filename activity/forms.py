from django import forms
from activity.models import Comment, Reply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': "دیدگاه خود را در مورد این محصول بنویسید ...", 'class': 'comment-input'})
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': "پاسخ خود را بنویسید ..", 'class': 'add-reply-input'})
        }
