from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.index.urls',namespace='index')),
    path('accounts/',include('apps.accounts.urls',namespace='accounts')),
    path('products/',include('apps.products.urls',namespace='products')),
    path('comments/',include('apps.comments.urls',namespace='comments')),
    path('orders/',include('apps.orders.urls',namespace='orders')),
    path('scoring/',include('apps.scoring.urls',namespace='scoring')),
    path('compare/',include('apps.compare.urls',namespace='compare')),
    path('favorite/',include('apps.favorite.urls',namespace='favorite')),
    path('search/',include('apps.search.urls',namespace='search')),
    path('about_us/',include('apps.about_us.urls',namespace='about_us')),
    path('ckeditor',include('ckeditor_uploader.urls')),


    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)