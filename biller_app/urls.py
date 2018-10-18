from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('callstart', views.CallStartRecordView)
router.register('callend', views.CallEndRecordView)


urlpatterns = [

    path('', include(router.urls)),
    path('biller/', views.index, name='index'),
    path('biller/<str:subscriber>', views.billerSimpleReport, name='index'),
    path('biller/<str:subscriber>/<str:month>/<str:year>', views.billerCompleteReport, name='biller'),

]

#adicionar o index e depois deploy no heroku para teste