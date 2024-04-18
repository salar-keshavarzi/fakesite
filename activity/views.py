from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework.permissions import IsAuthenticated

from activity.models import Comment, Reply, Like
from product.models import Product
from rest_framework.generics import CreateAPIView, DestroyAPIView
from activity.serializers import FavoriteSerializer
from lib.permissions import FavoriteOwnerPermission

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


class AddToFavoriteAPI(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, FavoriteOwnerPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteFavoriteAPI(DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = FavoriteSerializer
    lookup_url_kwarg = 'favorite_id'
    permission_classes = [IsAuthenticated, FavoriteOwnerPermission]
