from django.db import models

from django.db import models
from modules.file_upload_module import FileUploader
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
import datetime
from middlewares.middlewares import RequestMiddleware
from django.db.models import Q,Sum,Avg

#----------------------------------------------------------------------------------------------------   Brand
class Brand(models.Model):
    # upload_image
    file_upload=FileUploader('images','Brand')
    
    brand_name=models.CharField(max_length=50,verbose_name='نام برند')
    brand_slug=models.SlugField(max_length=50,null=True)
    brand_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر برند')

    # brands=.....
    
    def __str__(self):
        return self.brand_name
    
    class Meta:
        verbose_name='برند'
        verbose_name_plural='برند ها'
        
#----------------------------------------------------------------------------------------------------  ProductGroup
class ProductGroup(models.Model):
    # upload_image
    file_upload=FileUploader('images','product_group')

    group_name=models.CharField(max_length=50,verbose_name='عنوان گروه کالا')
    group_slug=models.SlugField(max_length=50,null=True,verbose_name='شناسه گروه کالا')
    group_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر گروه کالا')
    # group_description=models.TextField(verbose_name='توضیحات گروه',blank=True,null=True)  # with ckeditor
    # group_description=RichTextUploadingField(blank=True,null=True)
    group_isactive=models.BooleanField(default=False,verbose_name='وضعیت گروه',blank=True) #
    product_registerdate=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    product_publish_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    product_update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزرسانی')
    
    group_parent=models.ForeignKey('ProductGroup',on_delete=models.CASCADE,verbose_name='والد گروه کالا',blank=True,null=True,related_name='groups') #
    # groups=...
    # products_of_group=.....
    # features_of_group=.....
    
    def __str__(self):
        return self.group_name
    
    class Meta:
        verbose_name='گروه محصول'
        verbose_name_plural='گروه های محصولات'

#----------------------------------------------------------------------------------------------------  Feature
class Feature(models.Model):
    feature_name=models.CharField(max_length=50,verbose_name='نام ویژگی')
    feature_slug=models.SlugField(max_length=100,verbose_name='شناسه ویژگی',null=True,blank=True)
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='features_of_group')
    # feature_value=...
    
    def __str__(self):
        return self.feature_name
    
    class Meta:
        verbose_name='ویژگی'
        verbose_name_plural='ویژگی ها'
        
#----------------------------------------------------------------------------------------------------  Product
class Product(models.Model):
    # upload_image
    file_upload=FileUploader('images','product')

    product_name=models.CharField(max_length=300,verbose_name='نام محصول')
    product_summery_description=RichTextUploadingField(verbose_name='خلاصه توضیحات کالا',blank=True,null=True)  # with ckeditor
    product_description=RichTextUploadingField(verbose_name='توضیحات کالا',blank=True,null=True)  # with ckeditor
    product_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر محصول')
    product_price=models.PositiveBigIntegerField(default=0,verbose_name='قیمت محصول')
    product_isactive=models.BooleanField(default=False,verbose_name='وضعیت کالا',blank=True)
    product_slug=models.SlugField(max_length=50,null=True,verbose_name='شناسه کالا')
    product_registerdate=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    product_publish_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    product_update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزرسانی')
    
    product_brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,related_name='brands')
    product_feature=models.ManyToManyField(Feature,through='ProductFeature') #
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='products_of_group')
    
    
    # fields from oneTomany or manyTomany relationship
    # product_features= ...
    # product_gallary= ...
    # product_favorites= ...                         from favorite app
    # warehouse_products=...                         from warehouses app
    #discount_basket_detail_product=...              from discount app
    # products_comments=...                          from comment app
    
    def __str__(self):
        return self.product_name
    
    # for having product link to detail each time
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.product_slug})
    
    # for getting favorite for each product  for each user
    def get_user_favorite(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        # output is True/False
        flag=self.product_favorites.filter(user_favorite=request.user).exists()
        return flag
    
    # getting number of product in warehouse
    def get_warehouse_status(self):
        num_buy=self.warehouse_products.filter(warehouse_type=1).aggregate(num_buy=Sum('number'))
        num_sell=self.warehouse_products.filter(warehouse_type=2).aggregate(num_sell=Sum('number'))
        
        input,output=0,0
        if num_buy['num_buy']!=None:
            input=num_buy['num_buy']
        if num_sell['num_sell']!=None:
            output=num_sell['num_sell']
            
        return input-output
    
    # for getting price with discount
    def get_finall_price_with_discount(self):
        current_price=self.product_price
        time_now=datetime.datetime.now()
        discount_list=[]
        discount_get=self.discount_basket_detail_product.all()
        
        for item in discount_get:
            if item.discount_basket.is_active==True and item.discount_basket.end_date>=time_now and item.discount_basket.start_date<=time_now :
                discount_list.append(item.discount_basket.discount)
        
        final_discount=0
        if len(discount_list)>0:
            final_discount=max(discount_list)
        
        return current_price-((current_price*final_discount)/100)

    def get_product_comments(self):
        all_comments=self.products_comments.filter(is_active=True)
        return all_comments

                
                
                
                
                
    class Meta:
        verbose_name='محصول'
        verbose_name_plural='محصولات'

#----------------------------------------------------------------------------------------------------  FeatureValue
class FeatureValue(models.Model):    # we can use this model in inline mode in feature model
    value_title=models.CharField(max_length=100,verbose_name='مقدار ویژگی')
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی',null=True,blank=True,related_name='feature_value')
    # filter_values=...
    
    def __str__(self):
        return f'{self.value_title}'
    
    class Meta:
        verbose_name='مقدار ویژگی'
        verbose_name_plural='مقدار ویژگی ها'
        
#----------------------------------------------------------------------------------------------------   ProductFeature
class ProductFeature(models.Model):    # we can use this model in inline mode in product model
    product_feature_product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول',related_name='product_features')
    product_feature_feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی')
    value=models.CharField(max_length=100,verbose_name='مقدار ویژگی محصول')
    filter_value=models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name='مقدار فیلتر',related_name='filter_values')
    def __str__(self):
        return f'{self.product_feature_product} : {self.product_feature_feature} = {self.value}'
    
    class Meta:
        verbose_name='ویژگی محصول'
        verbose_name_plural='ویژگی های محصولات'
#----------------------------------------------------------------------------------------------------  ProductGallary
class ProductGallary(models.Model):
    # upload_image
    file_upload=FileUploader('images','product_gallary')

    product_gallary_product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='',related_name='product_gallary')
    product_gallary_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر محصول')

    def __str__(self):
        return str(self.product_gallary_image)
    
    class Meta:
        verbose_name='تصویر محصول'
        verbose_name_plural='تصویر های محصول'

#----------------------------------------------------------------------------------------------------
