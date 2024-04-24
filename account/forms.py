from django import forms
from django.core.exceptions import ValidationError

from account.models import Address, UserModel
from activity.models import Support


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'is_active')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'number', 'maxlength': '11', 'type': 'tel'}),
            'zipcode': forms.TextInput(attrs={'class': 'number', 'maxlength': '20', 'type': 'tel'})
        }
        labels = {
            'region': 'استان',
            'city': 'شهر',
            'address_detail': 'آدرس محل تحویل',
            'zipcode': 'کد پستی',
            'fullname': 'نام و نام خانوادگی گیرنده',
            'phone_number': 'شماره تلفن گیرنده',
        }

    def clean(self):
        a = self.cleaned_data.get('region')
        b = self.cleaned_data.get('city')
        c = self.cleaned_data.get('address_detail')
        d = self.cleaned_data.get('fullname')
        e = self.cleaned_data.get('phone_number')
        f = self.cleaned_data.get('zipcode')
        if all([a, b, c, d, e, f]):
            return self.cleaned_data
        raise ValidationError('لطفا تمامی فیلد ها را پر کنید')


class UserForm(forms.Form):
    first_name = forms.CharField(label="نام", label_suffix='', required=False, max_length=150)
    last_name = forms.CharField(label="نام خانوادگی", label_suffix='', required=False, max_length=150)
    human_id = forms.CharField(label="کد ملی", label_suffix='', required=False, max_length=10,
                               widget=forms.TextInput({'class': 'number', 'type': 'tel'}))

    def save(self, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.human_id = self.cleaned_data.get('human_id')
        user.save()

    def clean_human_id(self):
        human_id = self.cleaned_data.get('human_id')
        if len(human_id) != 10 and len(human_id) != 0:
            raise ValidationError('کد ملی بایستی 10 رقم باشد')
        return human_id


class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'class': 'message-input', 'placeholder': 'متن پیغام خود را بنویسید ..'})
        }
