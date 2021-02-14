from django.contrib import admin
from django.urls import path
from shop import views
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    url(r'^', include('shop.urls', namespace='shop')),
]
