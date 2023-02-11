from django.urls import path
from .views import RegisterUserView,VerifyRegisterUserView,LoginUserView,ChangePasswordView,RememberPasswordView,LogoutUser,UserPanelView
app_name='accounts'

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name='register'),
    path('verify/',VerifyRegisterUserView.as_view(),name='verify'),
    path('login/',LoginUserView.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(),name='logout'),
    path('changepassword/',ChangePasswordView.as_view(),name='changepassword'),
    path('rememberpassword/',RememberPasswordView.as_view(),name='rememberpassword'),
    path('userpanel/',UserPanelView.as_view(),name='userpanel'),


]