from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import Q,Max,Min,Avg
from apps.products.models import Product
from .models import Favorite
#----------------------------------------------------- create view for favorite products add
class AddToFavoriteView(View):
    def get(self,request,*args,**kwargs):
        product_id=request.GET.get('product_id')
        product=Product.objects.get(id=int(product_id))
        
        flag=Favorite.objects.filter(Q(user_favorite_id=request.user.id) & Q(product_id=product_id)).exists()
        
        # for checking that user like that special product berfore not 
        if (not flag) :
            Favorite.objects.create(
                product=product,
                user_favorite=request.user
            )
            return HttpResponse('این کالا به لیست علایق شما اضافه شد')
        return HttpResponse('این کالا قبلا به لیست علایق شما اضافه شده است')
#----------------------------------------------------- create view for favorite products show
class FavoriteProductView(View):
    def get(self,request,*args,**kwargs):
        favorite_product_list=Product.objects.filter(product_favorites__user_favorite_id=request.user.id)
        return render(request,'favorite_app/favorite_product_list.html',{'favorite_product_list':favorite_product_list})
