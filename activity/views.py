from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from activity.models import Comment, Reply
from product.models import Product


class ProductCommentView(View):
    @method_decorator(login_required)
    def post(self, request, product_id):
        comment = request.POST.get('comment-input', None)
        product = Product.objects.filter(id=product_id).first()
        if comment and product and len(comment) < 1001:
            Comment.objects.create(product=product, user=request.user, content=comment)
        return redirect('product', product_id=product_id)


class CommentReplyView(View):
    @method_decorator(login_required)
    def post(self, request, comment_id):
        reply = request.POST.get('reply-input', None)
        try:
            comment = Comment.objects.get(id=comment_id)
            if reply and len(reply) < 1001:
                Reply.objects.create(user=request.user, comment=comment, content=reply)
            return redirect('product', product_id=comment.product_id)
        except Comment.DoesNotExist:
            raise Http404
