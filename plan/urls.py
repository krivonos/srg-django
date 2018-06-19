from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init', views.init_plan, name='init'),
    path('launch', views.update_plan_dates, name='launch'),
    path('BearLakes/<int:day>/show', views.show_SessionBearLakes, name='showBearLakes'),
    path('BearLakes/<int:day>/update', views.update_SessionBearLakes, name='showBearLakes'),
]

