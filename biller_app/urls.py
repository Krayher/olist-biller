from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('callstart', views.CallStartRecordView)
router.register('callend', views.CallEndRecordView)


urlpatterns = [
    path('', include(router.urls)),
    path('biller/', views.index, name='index'),
    #path('biller/<int:subscriber>', views.index, name='index'),
    #path('biller/<int:subscriber>/<int:month>/<int:year>', views.biller, name='biller'),

]