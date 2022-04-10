import django.views.generic as views
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.forms import PostCreateForm, \
    PostEditForm
from softuni_web_project.main_app.models import Post

UserModel = get_user_model()


class UnauthenticatedUserView(views.TemplateView):
    template_name = 'main_app/unauthenticated-user-page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


# my_login_password12345

class HomeView(views.ListView):
    model = Post
    template_name = 'main_app/home.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('unauthenticated user page')
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, views.CreateView):
    form_class = PostCreateForm
    template_name = 'main_app/post-create.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = Profile.objects.get(user_id=self.request.user.id)
        return kwargs


class PostEditView(LoginRequiredMixin, views.UpdateView):
    form_class = PostEditForm
    template_name = 'main_app/post-edit.html'

    def get_queryset(self):
        return Post.objects.get_queryset()

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})


class PostDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Post
    template_name = 'main_app/post-delete.html'

    def get_queryset(self):
        return Post.objects.get_queryset()

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})


def search_profiles_view(request):
    context = {}
    if request.method == 'POST':
        search = request.POST['search_text_input']
        users = UserModel.objects.filter(username__contains=search).exclude(username__exact=request.user.username)
        profiles = Profile.objects.filter(user__in=users)
        users.order_by('-id')
        profiles.order_by('-user_id')
        users = [user for user in users if not user.is_superuser and not user.is_staff]

        context = {
            'search': search,
            'users_profiles': zip(users, profiles)
        }
    return render(request, 'main_app/search-profiles.html', context)


@login_required()
def follow_view(request, pk):
    followed_profile = Profile.objects.get(pk=pk)
    following_profile = Profile.objects.get(pk=request.user.id)
    if following_profile in followed_profile.followers.all():
        followed_profile.followers.remove(following_profile)
        following_profile.following.remove(followed_profile)
    else:
        followed_profile.followers.add(following_profile)
        following_profile.following.add(followed_profile)
    return redirect('profile details', pk=pk)


@login_required()
def post_like_view(request, pk):
    post = Post.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)
    if profile in post.likes.all():
        post.likes.remove(profile)
    else:
        post.likes.add(profile)
    return redirect('profile details', pk=post.profile_id)
