"""
URL configuration for testing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from classicmodels.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    # path('register/', register,name='register'),
    path('', add_customer, name = 'add_customer'),
    path('home/<int:pk>/', homes,name='homes'),
    path('shopping/<int:pk>/<int:page>', show_all_product,name='show_all_product'),
    path('shopping/order/<int:pk>/', show_all_order, name = 'all_order'),
    path('shopping/order/<int:cus_id>/<int:order_id>', each_order, name = 'each_order'),
    path('shopping/ship/<int:cus_id>/<int:order_id>', mark_as_shipped, name = 'mark_as_shipped'),

    path('shopping/review/<int:cus_id>/<int:prod_id>', ship, name = 'ship'),
    path('shopping/product/<int:cus_id>/<int:prod_id>', each_product, name = 'each_product'),

    path('add/<int:cus_id>/<int:pk>/', add_to_order, name = 'add_to_order'),
    path('order_detail/<int:cus_id>/<int:pk>', delete_from_cart, name = 'delete_item'),
    path('order_detail/<int:cus_id>', order_details, name = 'order_details'),
    path('check_out/<int:cus_id>/<int:order_id>', check_out, name = 'check_out'),


    path('bank/<int:cus_id>/', bank, name = 'bank'),

    path('shopping/<str:category>/<int:cus_id>/<int:page>', products_by_category, name='products_by_category'),


    path('revenue/<int:cus_id>', show_revenue, name = 'show_revenue'),

    path('blog/<int:cus_id>', blog, name = 'blog'),
    path('each_blog/<int:cus_id>/<int:post_id>', each_blog, name='each_blog'),
    path('shopping/favorite/delete/<int:cus_id>/<int:prod_id>', delete_from_favlist, name = 'delete_from_favlist'),



    path('favorite/<str:category>/<int:cus_id>/<int:prod_id>', add_to_favorite_from_cat, name = 'add_to_favorite_from_cat'),
    path('all/favorite/<int:cus_id>/<int:prod_id>', add_to_favorite_from_all, name = 'add_to_favorite_from_all'),
    path('shopping/favorite/<int:cus_id>', favorite_list, name = 'favorite_list'),


    path('contact/<int:cus_id>', contact, name = 'contact'),
    
    path('blog/cat/<int:cus_id>/<str:tag_name>', blog_by_tag, name = 'blog_by_tag')
    #path('shopping/search/<int:pk>/', search, name = 'search_bar')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
