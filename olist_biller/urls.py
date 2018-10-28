from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from biller_app import urls
from biller_app import views

urlpatterns = [

    path('', include('biller_app.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),

]