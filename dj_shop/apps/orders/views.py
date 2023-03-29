from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_card import ShopCard
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# from apps.accounts.models import CustomerBuyer
# from .models import Order,OrderDetails,PaymentType
from apps.products.models import ProductGroup

# from .forms import OrderForm
# from apps.discounts.forms import CoupenForm
# from apps.discounts.models import Coupon
from django.db.models import Q,Count
import datetime
from django.contrib import messages

#-------------------------------------------------------------------------------- update shopcard status in navbar
def status_shop_card(request):
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    return HttpResponse(shop_card.item_count)
#-------------------------------------------------------------------------------- shop card page
class ShopCardView(View):
    def get(self,request,*args,**kwargs):
        user_id=request.user.id
        shop_card=ShopCard(request,user_id)
        
        return render(request,'orders_app/shop_card.html',{'shop_card':shop_card})
#-------------------------------------------------------------------------------- render partials  ** for updating shopcard list **
def show_shop_card(request):
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    product_count=shop_card.item_count
    total_price=shop_card.cal_total_price()
    delivery_price= 0 if total_price>2000000 else 25000
    tax_price=total_price*0.09
    final_price=total_price+delivery_price+tax_price
    
    return render(request,'orders_app/partials/show_shop_card.html',{'shop_card':shop_card,'product_count':product_count,'total_price':total_price,'delivery_price':delivery_price,'tax_price':tax_price,'final_price':final_price})
#-------------------------------------------------------------------------------- ajax function  for adding to shopcard
def add_to_shop_card(request):
    product_id=request.GET.get('product_id')
    number=request.GET.get('number')
    
    product=get_object_or_404(Product,id=product_id)
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    shop_card.add_to_shop_card(product,number)
    
    return HttpResponse(shop_card.item_count)
#-------------------------------------------------------------------------------- ajax function  for deleting a product from a shopcard
def delete_from_shop_card(request):
    product_id=request.GET.get('product_id')
    product=get_object_or_404(Product,id=product_id)

    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    shop_card.delete_from_shop_card(product)

    return redirect('orders:show_shop_cards')
#-------------------------------------------------------------------------------- ajax function  for adding extra number of product in shopcard
def add_more_product(request):
    product_id=request.GET.get('product_id')
    number=request.GET.get('number')
    product=get_object_or_404(Product,id=product_id)
    
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    shop_card.add_more_product(product,number)
    
    return redirect('orders:show_shop_cards')
