from django.urls import path

from softuni_web_project.accounts.views import UserRegisterView, UserLoginView, UserLogoutView, ProfileDetailsView, \
    ProfileEditView, ProfileDeleteView

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('edit/<int:pk>', ProfileEditView.as_view(), name='profile edit'),
    path('delete/<int:pk>', ProfileDeleteView.as_view(), name='profile delete'),

)
