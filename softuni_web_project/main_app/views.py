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
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return redirect('login')


class HomeView(views.ListView):
    model = Post
    template_name = 'main_app/home.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = Profile.objects.get(user_id=self.request.user.id)
        context.update({
            'user_profile': user_profile
        })
        return context

    def get_queryset(self):
        user_profile = Profile.objects.get(user_id=self.request.user.id)
        return Post.objects.filter(profile__in=user_profile.following.all())


class PostCreateView(LoginRequiredMixin, views.CreateView):
    form_class = PostCreateForm
    template_name = 'main_app/post-create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = Profile.objects.get(user_id=self.request.user.id)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})


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
        show_all = request.POST.get('show_all', False)
        if show_all:
            users = UserModel.objects.all().exclude(username__exact=request.user.username)
            search = None
        else:
            search = request.POST['search_text_input']
            users = UserModel.objects.filter(username__contains=search).exclude(username__exact=request.user.username)
        profiles = Profile.objects.filter(user__in=users)
        users.order_by('-id')
        profiles.order_by('-user_id')

        users_profiles = list(zip(users, profiles))
        context = {
            'users_profiles': users_profiles
        }
        if search:
            context['search'] = search
        else:
            context['show_all'] = show_all
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


def csrf_failure(request, reason=""):
    return render(request, 'main_app/403_csrf.html')
