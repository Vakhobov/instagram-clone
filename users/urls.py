from tkinter.font import names

from django.urls import path
from .views import SignUpView, VerifyAPIView, GetNewVerification, ChangeUserInformationView, ChangeUserPhotoView, \
    LoginView, LoginRefreshTokenView, LogOutView, ForgotPasswordView, ResetPasswordView

urlpatterns =[
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('login/refresh/', LoginRefreshTokenView.as_view(), name='login_refresh'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify' ),
    path('new-verify/', GetNewVerification.as_view(), name='new_verify'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change_user'),
    path('change-user-photo/', ChangeUserPhotoView.as_view(), name='photo'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]