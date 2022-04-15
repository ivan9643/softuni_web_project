from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from softuni_web_project.accounts.forms import ProfileEditForm
from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.models import Post


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(profile_id=self.object.user_id).order_by('-publication_date')
        posts_count = len(posts)
        likes_count = sum([post.likes.count() for post in posts])
        follower_count = self.object.followers.all().count()
        following_count = self.object.following.all().count()
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user_id=self.request.user.id)
            context.update({
                'user_profile': user_profile,
            })
        context.update({
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

    def post(self, request, *args, **kwargs):
        if 'go_back_button' in request.POST:
            redirect_url = reverse_lazy('profile details', kwargs={'pk': self.request.user.id})
            return HttpResponseRedirect(redirect_url)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def get_queryset(self):
        return Profile.objects.get_queryset()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = Profile.objects.get(user_id=self.object.user_id)
        return kwargs


class ProfileDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('unauthenticated user page')

    def post(self, request, *args, **kwargs):
        if 'go_back_button' in request.POST:
            redirect_url = reverse_lazy('profile details', kwargs={'pk': self.request.user.id})
            return HttpResponseRedirect(redirect_url)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(profile_id=self.object.user_id).order_by('-publication_date')
        posts_count = len(posts)
        likes_count = sum([post.likes.count() for post in posts])
        follower_count = self.object.followers.all().count()
        following_count = self.object.following.all().count()
        context.update({
            'posts_count': posts_count,
            'likes_count': likes_count,
            'follower_count': follower_count,
            'following_count': following_count,
        })
        return context
