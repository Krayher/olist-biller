from django.contrib import admin
from django.urls import path, include
from biller_app import urls
from biller_app import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('rest/', include('biller_app.urls')),

]