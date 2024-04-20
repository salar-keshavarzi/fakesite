from django import forms
from account.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'is_active')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'number', 'maxlength': '11'}),
            'zipcode': forms.TextInput(attrs={'class': 'number', 'maxlength': '20'})
        }
        labels = {
            'region': 'استان',
            'city': 'شهر',
            'address_detail': 'آدرس محل تحویل',
            'zipcode': 'کد پستی',
            'fullname': 'نام و نام خانوادگی گیرنده',
            'phone_number': 'شماره تلفن گیرنده',
        }

