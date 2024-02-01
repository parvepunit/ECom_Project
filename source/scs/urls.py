
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import home, checkout, datacstfetch, couriercheck


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',  home, name='home'),
    path('shop/', include('shop.urls')),
    path('checkout/', checkout),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('datacstfetch/', datacstfetch, name='datacstfetch'),
    path('couriercheck/', couriercheck, name='couriercheck'),

    

    

    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

