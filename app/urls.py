from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns=[
    
    path('',views.main,name="main"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('products/',views.products,name='products'),
    path('customer/<str:pk_test>/',views.customer,name='customer'),
    path('orderform/<str:pk>',views.create_order,name="createorder"),
    path('updateform/<str:pk>/',views.updateOrder,name='update'),
    path('delete/<str:pk>',views.deleteOrder,name='delete'),
    path('login/',views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),
    path('logout',views.logoutUser,name='logout'),
    path('userpage',views.userPage,name='user-page'),
    path('account',views.accountSettings,name='account'),
    path('reset_password/', auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_Done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views. PasswordResetCompleteView.as_view(),name="password_reset_complete"),  
    
]