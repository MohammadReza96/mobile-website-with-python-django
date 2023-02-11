from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.forms import UserCreationForm,UserChangeForm
from apps.accounts.models import CustomUser
#---------------------------------------------- 

class CustomUserAdmin(UserAdmin):
    form =UserChangeForm
    add_form =UserCreationForm
    list_display= ('mobile_number','email','name','family','gender','is_active','is_admin')
    list_filter=('is_active','is_admin','family')
    
    # modify user
    fieldsets =(
        ('login details',{'fields':('mobile_number','password')}),
        ('personal info',{'fields':('email','name','family','image','address','city','province','postal_code','gender','active_code')}),
        ('permissions',{'fields':('is_active','is_admin','is_superuser','groups','user_permissions')})
    )
    
    # create user
    add_fieldsets =(
        ('account details',{'fields':('mobile_number','email','name','family','gender','password','re_password')}),
    )
    
    search_fields=('mobile_number',)
    ordering = ('mobile_number',)
    filter_horizontal =('groups','user_permissions')

admin.site.register(CustomUser,CustomUserAdmin)