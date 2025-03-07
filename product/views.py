from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import ExpressionWrapper, F, IntegerField, QuerySet
from django.http import QueryDict, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
import uuid
from activity.forms import CommentForm, ReplyForm
from activity.models import Comment, Like
from product.serializers import ProductSerializer
from product.models import Product, Brand, Category, ProductImage, Inventory
from django.views.generic import View, ListView
from product.forms import SearchForm


class ProductListAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if search:
            return Product.search(product_title=search)
        return super().get_queryset()[:10]


# class ProductListView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         form = SearchForm
#         products = Product.objects.annotate(
#             discount_percent=ExpressionWrapper(100 * F('discount') / F('first_price'),
#                                                output_field=IntegerField())).all()
#         brands = Brand.objects.all()
#         categories = Category.objects.all()
#         return render(request, template_name='product/product_list.html',
#                       context={'products': products, 'brands': brands, 'categories': categories, 'form': form})

class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.annotate(
        discount_percent=ExpressionWrapper(100 * F('discount') / F('first_price'),
                                           output_field=IntegerField())).all()
    ordering = ['-is_available', '-visit_count']
    paginate_by = 24
    form_class = SearchForm

    def get_queryset(self):
        qs = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            categories = form.cleaned_data.get('category', None)
            brands = form.cleaned_data.get('brand', None)
            if categories:
                qs = qs.filter(category__in=categories)
            if brands:
                qs = qs.filter(brand__in=brands)
        return qs

    def get_ordering(self):
        ordering_options = {'most_visited': '-visit_count', 'newest': '-created_time',
                            'most_expensive': '-first_price', 'cheapest': 'first_price',
                            'bestselling': '-buy_count', 'most_discount': '-discount'}
        ordering_string = self.request.GET.get('order_by', 'most_visited')
        if ordering_string not in ordering_options.keys():
            ordering_string = 'most_visited'
        ordering = ['-is_available', ordering_options.get(ordering_string)]
        return ordering

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        form = self.form_class(self.request.GET)
        context['form'] = form
        paginator = Paginator(self.object_list, self.paginate_by)
        page = self.request.GET.get('page', None)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        temp = list()
        query_params = self.request.GET.copy().lists()
        for key, values in query_params:
            if key != 'page':
                for value in values:
                    temp.append(f"{key}={value}")
        pagination_query_string = '&'.join(temp)
        context[self.context_object_name] = objects
        context['pagination_query_string'] = pagination_query_string
        return context


class ProductPageView(View):
    def get(self, request, product_id):
        try:
            uuid.UUID(product_id, version=4)
        except ValueError:
            raise Http404
        product = Product.objects.filter(id=product_id).annotate(
            discount_percent=ExpressionWrapper(100 * F('discount') / F('first_price'),
                                               output_field=IntegerField())).first()
        if not product:
            raise Http404
        product.visit_count += 1
        product.save()
        images = ProductImage.objects.filter(product=product)
        attributes = product.get_attributes()
        inventories = Inventory.objects.filter(product=product, quantity__gt=0).select_related('color').all()
        comments = Comment.get_by_product(product=product)
        favorite = False
        comment_form = CommentForm()
        reply_form = ReplyForm()
        if request.user.is_authenticated:
            if temp := Like.objects.filter(user=request.user, product=product).first():
                favorite = temp
        return render(request, template_name='product/product.html',
                      context={'product': product, 'product_images': images, 'inventories': inventories,
                               'comments': comments, 'favorite': favorite,
                               'comment_form': comment_form, 'reply_form': reply_form, 'attributes': attributes})
