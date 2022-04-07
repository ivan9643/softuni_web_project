import django.views.generic as views
from django.shortcuts import redirect
from django.urls import reverse_lazy

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

