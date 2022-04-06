from django.urls import path

from softuni_web_project.main_app.views import UnauthenticatedUserView, HomeView, CreatePostView

urlpatterns = (
    path('', UnauthenticatedUserView.as_view(), name='unauthenticated user page'),
    path('home/', HomeView.as_view(), name='home'),
    path('post/create', CreatePostView.as_view(), name='create post'),
)