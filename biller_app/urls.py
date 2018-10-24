from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('callstart', views.CallStartRecordView)
router.register('callend', views.CallEndRecordView)

urlpatterns = [

    path('', views.index, name='index'),
    path('biller/', views.index, name='index'),
    path('rest/', include(router.urls)),
    path('biller/<str:subscriber>', views.find_subcriber, name='subscriber_only'),
    path('biller/<str:subscriber>/<int:month>/<int:year>', views.find_subscriber_month_year, name='subscriber_month_year'),

]

#adicionar o index e depois deploy no heroku para teste