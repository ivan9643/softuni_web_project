from django.urls import path

from softuni_web_project.main_app.views import UnauthenticatedUserView,\
    HomeView, PostCreateView, PostEditView, PostDeleteView

urlpatterns = (
    path('', UnauthenticatedUserView.as_view(), name='unauthenticated user page'),
    path('home', HomeView.as_view(), name='home'),
    path('post/create', PostCreateView.as_view(), name='post create'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post delete'),

)
