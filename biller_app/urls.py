from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('callstart', views.CallStartRecordView)
router.register('callend', views.CallEndRecordView)

urlpatterns = [

    path('', views.index, name='index'),
    path('biller/', views.biller, name='biller'),
    path('rest/', include(router.urls)),
    path('subscriber/<str:subscriber>', views.find_subscriber, name='subscriber_only'),
    path('subscriber/<str:subscriber>/<int:month>/<int:year>', views.find_subscriber_month_year, name='subscriber_month_year'),

]
