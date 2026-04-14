from django.contrib import admin
from django.urls import path
from shop.views import home
from shop import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('', views.home),
    path('product/<int:id>/', views.product_detail),
    path('add-to-cart/<int:id>/', views.add_to_cart),
    path('cart/', views.view_cart),
    path('checkout/', views.checkout),
    path('update-cart/<int:id>/<str:action>/', views.update_cart),
    path('remove-from-cart/<int:id>/', views.remove_from_cart),
    path('orders/', views.order_history),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)