from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.urls import reverse_lazy
from softuni_web_project.accounts.forms import CreateProfileForm, ProfileEditForm
from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.models import Post


class UserRegisterView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('unauthenticated user page')


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
        posts = Post.objects.filter(user_id=self.object.user_id)
        posts_count = len(posts)
        likes_count = sum([post.likes for post in posts])
        context.update({
            'posts_count': posts_count,
            'likes_count': likes_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'posts': posts,
        })
        return context


class ProfileEditView(views.UpdateView):
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def get_queryset(self):
        return Profile.objects.get_queryset()


class ProfileDeleteView(views.DeleteView):
    model = Profile
    template_name = "accounts/profile-delete.html"
    # form_class = ProfileDeleteForm

    def get_success_url(self):
        return reverse_lazy('unauthenticated user page')

    # def get_queryset(self):
    #     return Profile.objects.get_queryset()
