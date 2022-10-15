from django.template.defaulttags import url
from django.urls import path
from . import views

app_name = 'cart'
# urlpatterns = [
#     url(r'^$', views.cart_detail, name='cart_detail'),
#     url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
#     url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
# ]

urlpatterns = [
    path('', views.cart_detail, name = 'cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

]