from django.urls import path

from softuni_web_project.main_app.views import UnauthenticatedUserView, \
    HomeView, PostCreateView, PostEditView, PostDeleteView, search_profiles_view, \
    follow_view, post_like_view

urlpatterns = (
    path('', UnauthenticatedUserView.as_view(), name='unauthenticated user page'),
    path('home', HomeView.as_view(), name='home'),
    path('post/create', PostCreateView.as_view(), name='post create'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post delete'),
    path('search/profiles', search_profiles_view, name='search profiles'),
    path('follow/<int:pk>', follow_view, name='follow'),
    path('post/like/<int:pk>', post_like_view, name='post like'),

)
