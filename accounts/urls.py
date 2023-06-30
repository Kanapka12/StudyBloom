from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import *
from .views import SignUpView, UserDetailView, UsernameChangeView, EmailChangeView, EmailChangeConfirmView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form_cstm.html'), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done_cstm.html'), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form_cstm.html'), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done_cstm.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm_cstm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_cstm.html'), name='password_reset_complete'),
    path('', UserDetailView.as_view(), name='account_detail'),
    path('username_change/', UsernameChangeView.as_view(), name='username_change'),
    path('email_change/', EmailChangeView.as_view(), name='email_change'),
    path('email_change_confirm/', EmailChangeConfirmView.as_view(), name='email_change_confirm'),
    # path('change_default_profile_image/', ChangeDefaultProfileImage.as_view(), name='change_default_profile_image'),
    # path('appearance_change/', AppearanceChangeView.as_view(), name='appearance_change'),
]
