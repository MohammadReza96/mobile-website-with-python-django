from django.contrib import admin
from .models import DiscountBasket,DiscountBasketDetails,Coupon

#-------------------------------------------------------------------------------------
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=('coupon_code','start_date','end_date','discount','is_active')
    
#-------------------------------------------------------------------------------------
class DiscountBasketDetailsinline(admin.TabularInline):   # for adding product to this DiscountBasket
    model=DiscountBasketDetails
    extra=2

@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display=('discount_title','start_date','end_date','discount','is_active')
    ordering=('is_active',)
    inlines=(DiscountBasketDetailsinline,)

    

