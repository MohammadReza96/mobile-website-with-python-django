from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from modules.file_upload_module import FileUploader
from apps.products.models import Product
from apps.accounts.models import CustomUser
from extensions.jalai_converter_maker import jalali_converter

#----------------------------------------------------------------------------------------  author model 
class Author(models.Model):
    author_name=models.CharField(max_length=50,verbose_name='name')
    author_family=models.CharField(max_length=50,verbose_name='family')
    author_slug=models.SlugField(max_length=50,verbose_name='slug')
    author_email=models.EmailField(max_length=255,verbose_name='email')
    author_phone=models.CharField(max_length=11,verbose_name='phone',null=True,blank=True)
    auhtor_is_active=models.BooleanField(default=False,verbose_name='is active')
    
    def __str__(self):
        return self.author_name+' '+self.author_family
    
    class Meta:
        verbose_name='نویسنده'
        verbose_name_plural='نویسنده ها' 
#----------------------------------------------------------------------------------------  blog title group model
class BlogGroup(models.Model):
    group_title=models.CharField(max_length=20,verbose_name='title')
    
    def __str__(self):
        return self.group_title
    
    class Meta:
        verbose_name='گروه مقاله'
        verbose_name_plural='گروه مقاله'    
#----------------------------------------------------------------------------------------  blog model
class Blog(models.Model):
    file_upload=FileUploader('images','blog')
    
    blog_title=models.CharField(max_length=50,verbose_name='عنوان')
    blog_main_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس کاور مقاله')
    blog_slug=models.SlugField(max_length=50,verbose_name='شناسه')
    blog_short_text=models.TextField(verbose_name='متن خلاصه')
    blog_main_text=RichTextUploadingField(verbose_name='متن اصلی')
    
    blog_register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    blog_publish_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    blog_update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ آپدیت')
    blog_is_active=models.BooleanField(default=False,verbose_name='وضعیت مقاله')
    blog_view_number=models.PositiveIntegerField(default=0,verbose_name='تعداد بازدید')
    blog_author=models.ManyToManyField(Author,verbose_name='نویسنده',related_name='blog_author')
    blog_group=models.ForeignKey(BlogGroup,on_delete=models.CASCADE,verbose_name='گروه مقاله',related_name='blog_group')
    blog_related_product=models.ForeignKey(Product,on_delete=models.SET_NULL,verbose_name='کالا مرتبط با مقاله',null=True,blank=True,related_name='blog_product')
    
    # fields from oneTomany or manyTomany relationship --------------
    # blog_gallary=...     
    # blog_tag=...
    # blog_comments=...
    # blog_comments_like=...
    # blog_comments_dislike=...
    
    
    def __str__(self):
        return self.blog_title
    
    def blog_publish_date_jalai_type(self):
        return jalali_converter(self.blog_publish_date)
    blog_publish_date_jalai_type.short_description = 'زمان انتشار'
    
    # def blog_pgf(self,fileName):
    #     pass
    
    class Meta:
        verbose_name='مقاله'
        verbose_name_plural='مقاله ها'     
#----------------------------------------------------------------------------------------  tag model
class Tag(models.Model):
    tag_name=models.CharField(max_length=50,verbose_name='کلید واژه')
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_tag',verbose_name='مقاله')
    
    def __str__(self):
        return self.tag_name
    
    class Meta:
        verbose_name='کلید واژه'
        verbose_name_plural='کلید واژه ها'        
#----------------------------------------------------------------------------------------  blog image gallary model
class BlogGallary(models.Model):
    file_upload=FileUploader('images','blog_gallary')
    blog_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس مقاله')
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='مقاله',related_name='blog_gallary')
    
    def __str__(self):
        return self.blog.blog_slug
    
    class Meta:
        verbose_name='گالری مقاله'
        verbose_name_plural='گالری مقاله'
#----------------------------------------------------------------------------------------  blog like model
class Like(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',related_name='main_user_blog_like')
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='کالا',related_name='blog_comments_like')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثبت')
    
    class Meta:
        verbose_name='مقاله های لایک شده'
        verbose_name_plural='مقاله های لایک شده'
#----------------------------------------------------------------------------------------  blog dislike model
class DisLike(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',related_name='main_user_blog_dislike')
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='کالا',related_name='blog_comments_dislike')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name='مقاله های دیس لایک شده'
        verbose_name_plural='مقاله های دیس لایک شده'
#----------------------------------------------------------------------------------------  blog comment model
class CommentBlog(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='کالا',related_name='blog_comments')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',related_name='main_user_blog')
    user_admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='ادمین تایید کننده',null=True,blank=True,related_name='extra_user_blog_comment')
    user_comment=models.TextField(verbose_name='نظر کاربر')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ درج نظر')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت نظر',)
    
    def __str__(self):
        return f'{self.blog} - {self.user_comment}'
    
    class Meta:
        verbose_name='نظر در مورد مقاله ها'
        verbose_name_plural='نظرات در مورد مقاله ها'