import django.views.generic as views
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user_id=self.request.user.id)
            context.update({
                'user_profile': user_profile
            })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user_id=self.request.user.id)
            queryset = Post.objects.filter(profile__in=user_profile.following.all())
        return queryset.order_by('-publication_date')


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

    def post(self, request, *args, **kwargs):
        if 'go_back_button' in request.POST:
            redirect_url = reverse_lazy('profile details', kwargs={'pk': self.request.user.id})
            return HttpResponseRedirect(redirect_url)
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['post'] = Post.objects.get(pk=self.object.id)
        return kwargs


class PostDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Post
    template_name = 'main_app/post-delete.html'

    def get_queryset(self):
        return Post.objects.get_queryset()

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})

    def post(self, request, *args, **kwargs):
        if 'go_back_button' in request.POST:
            redirect_url = reverse_lazy('profile details', kwargs={'pk': self.request.user.id})
            return HttpResponseRedirect(redirect_url)
        return super().post(request, *args, **kwargs)


class SearchProfilesView(views.ListView):
    template_name = 'main_app/search-profiles.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        users = []
        if 'search_text_input' in self.request.GET:
            search = self.request.GET['search_text_input']
            users = UserModel.objects.filter(username__contains=search).exclude(
                username__exact=self.request.user.username)
        elif 'show_all' in self.request.GET:
            users = UserModel.objects.all().exclude(username__exact=self.request.user.username)
        profiles = Profile.objects.filter(user__in=users).order_by('user__username')
        return profiles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if 'search' in self.request.GET:
            search = self.request.GET['search_text_input']
            context['search'] = search
        elif 'show_all' in self.request.GET:
            context['show_all'] = True
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            context['user_profile'] = user_profile
        return context


class SearchHashtagsView(views.ListView):
    template_name = 'main_app/search-hashtags.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = []
        if 'search' in self.request.GET:
            search = self.request.GET['search_text_input']
            posts = Post.objects.filter(hashtags__name__contains=search).distinct() \
                .annotate(likes_count=Count('likes')) \
                .order_by('-likes_count')
        elif 'show_all' in self.request.GET:
            posts = Post.objects.all().annotate(likes_count=Count('likes')) \
                .order_by('-likes_count')
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if 'search' in self.request.GET:
            search = self.request.GET['search_text_input']
            context['search'] = search
        elif 'show_all' in self.request.GET:
            context['show_all'] = True
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            context['user_profile'] = user_profile
        return context


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


class ViewFollowingView(LoginRequiredMixin, views.ListView):
    model = Profile
    template_name = 'main_app/view_following.html'
    context_object_name = 'profiles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = Profile.objects.get(user_id=self.request.user.id)
        context.update({
            'user_profile': user_profile
        })
        return context

    def get_queryset(self):
        user_profile = Profile.objects.get(user_id=self.request.user.id)
        return Profile.objects.filter(user__in=user_profile.following.all()).order_by('user__username')


def csrf_failure(request, reason=""):
    return render(request, 'main_app/403_csrf.html')
