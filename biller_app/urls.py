from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('callstart', views.CallStartRecordView)
router.register('callend', views.CallEndRecordView)


urlpatterns = [

    path('', include(router.urls)),
    path('biller/', views.index, name='index'),
    path('biller/<str:subscriber>', views.list_call_by_subscriber, name='subscriber_only'),
    path('biller/<str:subscriber>/<int:month>/<int:year>', views.list_full_call_list, name='subscriber_year_month'),

]

#adicionar o index e depois deploy no heroku para teste