from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView
from account.models import UserModel, LoginCode, Address
from activity.models import Support, Comment, Like
from django.views import View
from account.serializers import LoginCodeSerializer
from django.contrib.auth import authenticate, logout, login
import time
from lib.throttle import LoginThrottle1, LoginThrottle2
from order.models import Buy, Transaction
from account.forms import AddressForm, UserForm, SupportForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, template_name='auth/login.html', context={'step': 1})

    def post(self, request):
        phone_number = request.POST.get('phone-number-hidden', None)
        otp_code = request.POST.get('otp-hidden', None)
        if phone_number and len(phone_number.strip()) == 11 and otp_code:
            username = phone_number.strip()
            otp = otp_code.strip()
            try:
                temp_user = UserModel.objects.get(username=username)
                if temp_user.otp_try > 0:
                    temp_user.otp_try -= 1
                    temp_user.save()
                else:
                    return render(request, template_name='auth/login.html', context={'step': 1})
            except UserModel.DoesNotExist:
                pass
            user = authenticate(username=username, password=otp)
            if user:
                if user.otp_try > 0:
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    return redirect('home')
            else:
                user = UserModel.objects.filter(username=phone_number).first()
                if user:
                    temp_time = 120 - int(time.time() - user.last_otp)
                    remaining_time = temp_time if temp_time > 0 else 120
                    return render(request, template_name='auth/login.html',
                                  context={'step': 2, 'phone_number': phone_number, 'remaining_time': remaining_time})
        return render(request, template_name='auth/login.html', context={'step': 1})


class LoginAPI(CreateAPIView):
    queryset = LoginCode.objects.all()
    serializer_class = LoginCodeSerializer
    throttle_classes = [LoginThrottle1, LoginThrottle2]


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class UserPanelPersonalView(View):
    form_class = UserForm

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form_data = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                     'human_id': user.human_id}
        form = self.form_class(form_data)
        return render(request, template_name='user/user_personal.html', context={'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request.user)
        return render(request, template_name='user/user_personal.html', context={'form': form})


class UserPanelBuysListView(View):
    @method_decorator(login_required)
    def get(self, request):
        buys = Buy.get_by_user(request.user)
        return render(request, template_name='user/user_buys.html', context={'buys': buys})


class UserPanelTransactionsListView(View):
    @method_decorator(login_required)
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).all().order_by("-created_time")
        return render(request, template_name='user/user_transactions.html', context={'transactions': transactions})


class UserPanelAddressesListView(View):
    @method_decorator(login_required)
    def get(self, request):
        addresses = Address.objects.filter(user=request.user).all()
        return render(request, template_name='user/user_addresses.html', context={'addresses': addresses})


class UserPanelAddressCreateView(View):
    form_class = AddressForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        return render(request, template_name='user/user_address.html', context={'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('user_panel_addresses')
        return render(request, template_name='user/user_address.html', context={'form': form})


class UserPanelAddressDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            if address.user == request.user:
                address.delete()
                return redirect('user_panel_addresses')
            else:
                raise Http404
        except Address.DoesNotExist:
            raise Http404


class UserPanelAddressEditView(View):
    form_class = AddressForm

    @method_decorator(login_required)
    def get(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            raise Http404
        form = self.form_class(instance=address)
        return render(request, template_name='user/user_address_edit.html', context={'form': form, 'address': address})

    @method_decorator(login_required)
    def post(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            raise Http404
        form = self.form_class(request.POST, instance=address)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('user_panel_addresses')
        return render(request, template_name='user/user_address_edit.html', context={'form': form, 'address': address})


class UserPanelSupportView(View):
    form_class = SupportForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        supports = Support.objects.filter(user=request.user).order_by('created_time')
        return render(request, template_name='user/user_support.html', context={'supports': supports, 'form': form})

    @method_decorator(login_required())
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
        return redirect('user_panel_support')


class UserPanelSupportClearView(View):
    @method_decorator(login_required)
    def get(self, request):
        Support.objects.filter(user=request.user).delete()
        return redirect('user_panel_support')


class UserPanelCommentsView(View):
    @method_decorator(login_required)
    def get(self, request):
        comments = Comment.objects.filter(user=request.user).select_related('product')
        return render(request, template_name='user/user_comments.html', context={'comments': comments})


class UserPanelCommentDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.user == request.user:
                comment.delete()
            return redirect('user_panel_comments')
        except Comment.DoesNotExist:
            raise Http404


class UserPanelLikesView(View):
    @method_decorator(login_required)
    def get(self, request):
        likes = Like.objects.filter(user=request.user).select_related('product')
        return render(request, template_name='user/user_likes.html', context={'likes': likes})


class UserPanelLikeDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, like_id):
        try:
            like = Like.objects.get(id=like_id)
            if like.user == request.user:
                like.delete()
            return redirect('user_panel_likes')
        except Like.DoesNotExist:
            raise Http404
