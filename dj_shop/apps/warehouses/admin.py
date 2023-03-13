from django.contrib import admin
from .models import Warehouse,WarehouseType
from apps.accounts.models import CustomUser
#------------------------------------------------------ warehousetype admin set up
@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display=['warehouse_type_title',]
#------------------------------------------------------ warehouse admin set up
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display=['product','warehouse_type','user_register','number','price','register_date']
    
    
    # for auto selecting the user base on login 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_register':
            kwargs['queryset'] = CustomUser.objects.filter(mobile_number=request.user.mobile_number)
        return super(WarehouseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)