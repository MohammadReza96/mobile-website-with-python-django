from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from modules.file_upload_module import FileUploader

#-----------------------------------------------------------------------------------------------------------------
class CustomUserManager(BaseUserManager): 
    def create_user(self,mobile_number,name='',family='',email='',image='',address='',city='',province='',postal_code='',active_code=None,gender=None,password=None):
        if not mobile_number:
            raise ValueError('شماره موبایل باید وارد شود')
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),  # for saveing email
            active_code=active_code,
            gender=gender
        )
        user.set_password(password) # for saving password
        user.save(using=self._db)
        return user
    #-------------------------
    def create_superuser(self,mobile_number,name,family,email,image=None,address=None,city=None,province=None,postal_code=None,password=None,active_code=None,gender=None):
        user=self.create_user(
            mobile_number=mobile_number,
            name=name,
            email=email,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password
                         )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

#-----------------------------------------------------------------------------------------------------------------
class CustomUser(AbstractBaseUser,PermissionsMixin):
    file_upload=FileUploader('images','user')
    # user_name
    mobile_number=models.CharField(max_length=11,unique=True)
    # user_data_martial
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    email=models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس کاربر',null=True,blank=True)
    gender_types=(('man','مرد'),('woman','زن'))
    gender=models.CharField(max_length=50,blank=True,choices=gender_types,default='man',null=True)
    # user_data_location
    address=models.TextField(null=True,blank=True,verbose_name='ادرس')
    city=models.CharField(max_length=50,null=True,blank=True,verbose_name='شهر')
    province=models.CharField(max_length=50,null=True,blank=True,verbose_name='استان')
    postal_code=models.CharField(max_length=12,null=True,blank=True,verbose_name='کدپستی')
    # user_data_date
    register_date=models.DateField(default=timezone.now)
    is_active=models.BooleanField(default=False)
    active_code=models.CharField(max_length=100,null=True,blank=True)
    is_admin=models.BooleanField(default=False)
    # to set username in fields
    USERNAME_FIELD='mobile_number'
    
    # fields from oneTomany or manyTomany relationship --------------------
    # user_favorites=...                                from favorite app
    # warehouse_registered=...                          from warehouses app
    # user_score=...                                    from scoring app
    
    # to set what kind of questions ask when we create a user (5 question(1-mobile_number/2-name/3-family/4-email/5-password)) # password already exits in model
    REQUIRED_FIELDS=['name','family','email']
    objects=CustomUserManager()
    
    def __str__(self):
        return self.name+' '+self.family
    
    @property
    def is_staff(self): # set that user can access to admin panel or not
        return self.is_admin