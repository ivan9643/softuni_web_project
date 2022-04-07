import django.views.generic as views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from softuni_web_project.accounts.models import Profile, CustomUser
from softuni_web_project.main_app.forms import PostCreateForm, \
    PostEditForm
from softuni_web_project.main_app.models import Post


class UnauthenticatedUserView(views.TemplateView):
    template_name = 'main_app/unauthenticated-user-page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class HomeView(views.ListView):
    model = Post
    template_name = 'main_app/home.html'
    context_object_name = 'posts'


class PostCreateView(views.CreateView):
    form_class = PostCreateForm
    template_name = 'main_app/post-create.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostEditView(views.UpdateView):
    form_class = PostEditForm
    template_name = 'main_app/post-edit.html'

    def get_queryset(self):
        return Post.objects.get_queryset()

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})


class PostDeleteView(views.DeleteView):
    model = Post
    template_name = 'main_app/post-delete.html'

    def get_queryset(self):
        return Post.objects.get_queryset()

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})


def search_profiles(request):
    context = {}
    if request.method == 'POST':
        search = request.POST['search_text_input']
        users = CustomUser.objects.filter(username__contains=search).exclude(username__exact=request.user.username)
        users_ids = [user.id for user in users]
        profiles = Profile.objects.filter(user__in=users)
        context = {
            'search': search,
            'users_profiles': zip(users, profiles)
        }
    return render(request, 'main_app/search-profiles.html', context)
