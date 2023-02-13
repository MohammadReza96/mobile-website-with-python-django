from django.db import models

from django.db import models
from modules.file_upload_module import FileUploader
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
import datetime
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
    group_slug=models.SlugField(max_length=50,null=True)
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
    product_slug=models.SlugField(max_length=50,null=True)
    product_registerdate=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    product_publish_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    product_update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزرسانی')
    
    product_brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,related_name='brands')
    product_feature=models.ManyToManyField(Feature,through='ProductFeature') #
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='products_of_group')
    
    # product_features= ...
    # product_gallary= ...
    # order_details_product= ...                     from order app
    # discount_basket_detail_product= ...            from discount app
    
    def __str__(self):
        return self.product_name
    
    # for having product link to detail each time
    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"slug": self.product_slug})
    
    # for getting price with discount
    def get_price_by_discount(self):
        list_discount=[]
        for item in self.discount_basket_detail_product.all():   # not use .objects.all()  instead use .all()
            if (item.discount_basket.is_active==True and item.discount_basket.start_date <= datetime.datetime.now() and  datetime.datetime.now() <= item.discount_basket.end_date):
                list_discount.append(item.discount_basket.discount)
        final_discount=0
        if (len(list_discount)>0):
            final_discount=max(list_discount)
            
        return self.product_price-(self.product_price*final_discount/100)
                
                
                
                
                
    class Meta:
        verbose_name='محصول'
        verbose_name_plural='محصولات'

#----------------------------------------------------------------------------------------------------  FeatureValue
class FeatureValue(models.Model):    # we can use this model in inline mode in feature model
    value_title=models.CharField(max_length=100,verbose_name='مقدار ویژگی')
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی',null=True,blank=True,related_name='feature_value')
    # filter_values=...
    
    def __str__(self):
        return f'{self.id}  {self.value_title}'
    
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
