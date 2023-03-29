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
