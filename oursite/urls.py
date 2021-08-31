from . import views
from django.urls import path
app_name='oursite'
urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('addstock',views.addStock,name='addStock')
]