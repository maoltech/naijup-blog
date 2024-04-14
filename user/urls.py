from django.urls import path
from .views import UserSignInView, UserSignUpView, UserSignOutView, UserDetailsView, GetUserByUsernameView

urlpatterns = [
    path('auth/signin/', UserSignInView.as_view(), name='user_signin'),
    path('auth/signup/', UserSignUpView.as_view(), name='user_signup'),
    path('auth/signout/', UserSignOutView.as_view(), name='user_signout'),
    path('', UserDetailsView.as_view(), name='user_details'),
    path('<str:username>/', GetUserByUsernameView.as_view(), name='get_user_by_username'),

]
