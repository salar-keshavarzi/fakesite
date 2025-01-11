from django import forms
from product.models import Category, Brand
from django.utils.translation import gettext_lazy as _

ORDERING_CHOICES = {
    "most_visited": "پربازدیدترین",
    "newest": "جدیدترین",
    "most_expensive": "گران ترین",
    "cheapest": "ارزان ترین",
    "bestselling": "پرفروش ترین",
    "most_discount": "بیشترین تخفیف",
}


class SearchForm(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label_suffix="",
                                              widget=forms.CheckboxSelectMultiple(attrs={'class': 'content'}),
                                              required=False, label='دسته بندی ها')
    # brand = forms.ModelMultipleChoiceField(queryset=Brand.objects.all(), label_suffix="",
    #                                        widget=forms.CheckboxSelectMultiple(attrs={'class': 'content'}),
    #                                        required=False, label='برند')
    order_by = forms.ChoiceField(choices=ORDERING_CHOICES, label_suffix="", widget=forms.Select(), required=False,
                                 label='مرتب سازی بر اساس')
