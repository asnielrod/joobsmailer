from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('complete_developer_profile/', views.complete_developer_profile, name='complete_developer_profile'),
    path('complete_employer_profile/', views.complete_employer_profile, name='complete_employer_profile'),
    path('home/', views.some_error_handling_view, name='some_error_handling_view'),
    path('my_offers/', views.my_offers, name='my_offers'),  
    path('jobposting/', views.jobposting, name='jobposting'),
    
]
