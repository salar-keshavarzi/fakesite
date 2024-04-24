from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework.permissions import IsAuthenticated

from account.models import BlockUser
from activity.forms import CommentForm, ReplyForm
from activity.models import Comment, Reply, Like
from product.models import Product
from rest_framework.generics import CreateAPIView, DestroyAPIView
from activity.serializers import FavoriteSerializer
from lib.permissions import FavoriteOwnerPermission


class ProductCommentView(View):
    form_class = CommentForm

    @method_decorator(login_required)
    def post(self, request, product_id):
        if BlockUser.objects.filter(user=request.user).exists():
            return redirect('product', product_id=product_id)
        form = self.form_class(request.POST)
        product = Product.objects.filter(id=product_id).first()
        if product:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.product = product
                instance.save()
        return redirect('product', product_id=product_id)


class CommentReplyView(View):
    form_class = ReplyForm

    @method_decorator(login_required)
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            form = self.form_class(request.POST)
            if BlockUser.objects.filter(user=request.user).exists():
                return redirect('product', product_id=comment.product_id)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.comment = comment
                instance.save()
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
