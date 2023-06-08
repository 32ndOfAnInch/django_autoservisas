from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list, name="car_list"),
    path('car/<int:pk>/', views.car_details, name='car_details'),
    path('orders/', views.OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path('myorders/', views.UserOrderEntryListView.as_view(), name='user_orders'),
]
