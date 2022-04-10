from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views
from django.urls import reverse_lazy
from softuni_web_project.accounts.forms import CreateProfileForm, ProfileEditForm
from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.models import Post


class UserRegisterView(views.CreateView):
    form_class = CreateProfileForm
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
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    # def get_success_url(self):
    #     return reverse_lazy('profile details',kwargs={'pk':self.request.user.id})


class UserLogoutView(auth_views.LogoutView):
    pass


# login required mixin where needed !!!


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(profile_id=self.object.user_id)
        posts_count = len(posts)
        likes_count = sum([post.likes.count() for post in posts])
        follower_count = self.object.followers.all().count()
        following_count = self.object.following.all().count()
        user_profile = Profile.objects.get(pk=self.request.user.id)
        context.update({
            'user_profile': user_profile,
            'posts_count': posts_count,
            'likes_count': likes_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'posts': posts,
            'follower_count': follower_count,
            'following_count': following_count,
        })
        return context


class ProfileEditView(LoginRequiredMixin, views.UpdateView):
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def get_queryset(self):
        return Profile.objects.get_queryset()


class ProfileDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Profile
    template_name = "accounts/profile-delete.html"

    # form_class = ProfileDeleteForm

    def get_success_url(self):
        return reverse_lazy('unauthenticated user page')

    # def get_queryset(self):
    #     return Profile.objects.get_queryset()
