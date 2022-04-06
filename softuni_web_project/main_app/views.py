import django.views.generic as views
from django.shortcuts import redirect
from django.urls import reverse_lazy

from softuni_web_project.main_app.forms import CreatePostForm
from softuni_web_project.main_app.models import Post


class UnauthenticatedUserView(views.TemplateView):
    template_name = 'main_app/unauthenticated_user_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class HomeView(views.ListView):
    model = Post
    template_name = 'main_app/home.html'
    context_object_name = 'posts'


class CreatePostView(views.CreateView):
    form_class = CreatePostForm
    template_name = 'main_app/create_post.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

