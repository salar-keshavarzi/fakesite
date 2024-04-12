from django.db import models
from lib.base_model import BaseModel
from account.models import UserModel
from product.models import Product
from django.utils.translation import gettext_lazy as _


class Like(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{str(self.user)}-{str(self.product)}"

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('likes')


class Comment(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False, null=False, verbose_name=_('comment content'))

    def __str__(self):
        return f"{str(self.user)}-{str(self.product)}"

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Reply(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(blank=False, null=False, verbose_name=_('comment content'))

    def __str__(self):
        return f"{str(self.user)}-reply"

    class Meta:
        verbose_name = _('reply')
        verbose_name_plural = _('replies')


class Support(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='supports')
    message = models.TextField(null=False, blank=False, verbose_name=_('message'))
    response = models.TextField(null=True, blank=True, verbose_name=_('response'))
    is_answered = models.BooleanField(default=False, editable=False, verbose_name=_('answered'))

    def __str__(self):
        return f"{str(self.user)}-support"

    def save(self, *args, **kwargs):
        if self.response:
            self.is_answered = True
        else:
            self.is_answered = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('support')
        verbose_name_plural = _('supports')
