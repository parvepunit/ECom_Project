from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("email_temp/", views.email_temp, name="email_temp"),
    path("order_status/<str:orderId>/", views.order_status, name="order_status"),
    path("tracking/", views.tracking, name="tracking"),

    




] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
