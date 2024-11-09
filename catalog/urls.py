from django.urls import path
from . import views


urlpatterns = [
    path('', views.sales_of_item, name='home'),
    path('scalar_function', views.scalar_function, name='scalar_function'),
    path('table_function',  views.table_function, name='table_function'),
    path('items/new', views.add_item, name='new_item')
]
