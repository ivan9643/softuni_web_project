from django.urls import path

from softuni_web_project.accounts.views import UserRegisterView, UserLoginView, UserLogoutView, ProfileDetailsView

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

)
