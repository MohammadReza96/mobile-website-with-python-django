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
    path('favorite/',include('apps.favorite.urls',namespace='favorite')),
    path('search/',include('apps.search.urls',namespace='search')),
    path('ckeditor',include('ckeditor_uploader.urls')),


    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)