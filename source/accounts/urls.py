from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('admin_page/', views.admin_page, name='admin-page'),
    path('users/<str:pk_test>/', views.users_page, name='users'),
    path('del_item', views.del_item, name='del_item'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_orders', views.user_orders, name='user_orders'),
    path('invoice/<str:order_id>/', views.invoice, name='invoice'),
    path('search/', views.searchapi, name='search'),
    

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_sent.html"), name='password_reset_done'),
    path('reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_change.html"), name='password_reset_complete'),



]