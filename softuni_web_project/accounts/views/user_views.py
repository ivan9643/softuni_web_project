from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic as views
from softuni_web_project.accounts.forms import RegisterForm, LoginForm, ChangePasswordForm


class UserRegisterView(views.CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(
            username=username,
            password=password,
        )
        login(self.request, user)
        return to_return


class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class ChangePasswordView(LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'accounts/change-password.html'
    success_url = reverse_lazy('home')
