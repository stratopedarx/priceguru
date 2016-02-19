# -*- coding: utf-8 -*-
import random
import string
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from ..helpers import send_mail
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.views.generic import View, FormView, TemplateView, DetailView
from django.utils.decorators import method_decorator
from ..forms.user import LoginForm, RegisterForm, RestorePasswordRequestForm
from core.user.models import User
from django.contrib import messages

def redirect_if_login(f):  # Редиректит со страниц login и register если пользователь уже авторизован
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('user:userprofile'))
        else:
            return f(request, *args, **kwargs)
    return wrap


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class LoginView(TemplateView):
    form_class = LoginForm
    template_name = 'user/login.html'

    @method_decorator(redirect_if_login)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request.POST or None)
        return self.render_to_response(locals())

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(**data)
            if user and user.is_active:
                login(request, user)
                next = self.request.GET.get("next", reverse("user:userprofile"))
                return HttpResponseRedirect(next, status=301)
            else:
                errors = [_("login failed")]
        return self.render_to_response(locals())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'user/register.html'
    success_url = "/user/"

    @method_decorator(redirect_if_login)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save()
        instance.is_active = True
        instance.set_password(form.cleaned_data['password'])
        instance.save()
        user = authenticate(username=instance.username, password=form.cleaned_data['password'])
        login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, _("Registration was successfull! Now you can add your first group"))
        return super(RegisterView, self).form_valid(form)


class RegisterSuccessView(TemplateView):
    template_name = 'user/register.success.html'


class RestorePasswordRequestView(FormView):
    form_class = RestorePasswordRequestForm
    template_name = 'user/change.password.html'


    def form_valid(self, form):
        email = form.cleaned_data['email']
        new_password = ''.join(map(lambda x: random.choice(string.ascii_letters + string.digits), xrange(10)))

        user = get_user_model().objects.get(email=email)
        user.set_password(new_password)
        user.save()

        send_mail(_("Request to restore password"),
        'user/mail/change.password.html',
                  email, password=new_password)
        messages.add_message(self.request, messages.SUCCESS, _(u'Your password is reset. Check email and login.'))
        return HttpResponseRedirect(reverse("user:login"))


class RestorePasswordRequestDoneView(TemplateView):
    template_name = 'user/change.password.done.html'


class UserPage(LoginRequiredMixin, DetailView):
    model = get_user_model()

class UserSettingsView(LoginRequiredMixin, DetailView):
    template_name = 'userprofile/profile.html'
    model = get_user_model()
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)


# Попытка написать 1 класс для изменения любого поля в профиле пользователя(1 метод - 1 поле)
class UserSettingsChange(View, LoginRequiredMixin):
    http_method_names = ['post']
    context = {}

    def change_email(self):
        self.context = {'status': 'undefined'}
        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email
        try:
            validate_email(self.request.POST['email'])
        except ValidationError:
            self.context['status'] = u'error'
            self.context['message'] = u'Your email is invalid'
        else:
            is_exist = True
            try:
                u = User.objects.get(email=self.request.POST['email'])
            except User.DoesNotExist:
                is_exist = False
            else:
                if u.id != self.request.user.id:
                    is_exist = True
                else:
                    is_exist = False

            if is_exist == False:
                self.request.user.email = self.request.POST['email']
                self.context['status'] = u'success'
                self.context['message'] = u'Email was changed'
                self.context['email'] = self.request.POST['email']
            else:
                self.context['status'] = u'error'
                self.context['message'] = u'This email already used by another user'

    def change_password(self):
        if len(self.request.POST.get('password_old', '')) and len(self.request.POST.get('password_new', '')):
            if len(self.request.POST.get('password_new', '')) < 5:
                self.context['status'] = u'error'
                self.context['message'] = u'New password is too short'

            elif self.request.user.check_password(self.request.POST.get('password_old', '')):
                self.context['status'] = u'success'
                self.context['message'] = u'Password was changed'
                self.request.user.set_password(self.request.POST['password_new'])
            else:
                self.context['status'] = u'error'
                self.context['message'] = u'Authoriztion failed'
        else:
            self.context['status'] = u'error'
            self.context['message'] = u'One or both fields are empty'

    def post(self, request):
        self.context = {'status': 'undefined'}
        try:
            User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            self.context['status'] = u'error'
            self.context['message'] = u'User does not exist'
        else:
            if hasattr(self, 'change_'+str(request.POST['field'])):
                getattr(self, 'change_'+str(request.POST['field']))()
                self.request.user.save()
            else:
                self.context['status'] = u'error'
                self.context['message'] = '500 Error'

        return JsonResponse(self.context)

class UserChangeEmailAjax(View, LoginRequiredMixin):
    http_method_names = ['post']

    def post(self, request):
        context = {'status': 'undefined'}
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            context['status'] = u'error'
            context['message'] = u'User does not exist'
        else:
            from django.core.exceptions import ValidationError
            from django.core.validators import validate_email
            try:
                validate_email(request.POST['email'])
            except ValidationError:
                context['status'] = u'error'
                context['message'] = u'Your email is invalid'
            else:
                user.email = request.POST['email']
                context['status'] = u'success'
                context['message'] = u'Email was changed'

        return JsonResponse(context)

class UserChangePasswordAjax(View, LoginRequiredMixin):
    http_method_names = ['post']

    def post(self, request):
        context = {'status': 'undefined'}
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            context['status'] = u'error'
            context['message'] = u'User does not exist'
        else:
            if len(request.POST.get('password_old', '')) and len(request.POST.get('password_new', '')):
                if len(request.POST.get('password_new', '')) < 5:
                    context['status'] = u'error'
                    context['message'] = u'New password is too short'

                elif request.user.check_password(request.POST.get('password_old', '')):
                    context['status'] = u'success'
                    context['message'] = u'Password was changed'
                    user.set_password(request.POST['password_new'])
                    user.save()
                else:
                    context['status'] = u'error'
                    context['message'] = u'Authoriztion failed'
            else:
                context['status'] = u'error'
                context['message'] = u'One or both fields are empty'
        return JsonResponse(context)

