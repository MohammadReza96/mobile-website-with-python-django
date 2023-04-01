from django.shortcuts import render
from django.conf import settings
from django.views import View
from apps.blogs.models import Blog
from .models import SliderImage
# for loading media_url anywhere & everytime
#------------------------------------------
def media_admin(request):
    return {'media_url':settings.MEDIA_URL}

#index page show
#--------------------------------------------------------- 
class IndexView(View):
    def get(self,request,*args,**kwargs):
        blogs=Blog.objects.filter(blog_is_active=True).order_by('blog_publish_date')
        slider_image=SliderImage.objects.filter(is_active=True)
        
        return render(request,'index_app/index.html',{"blogs":blogs,'slider_image':slider_image})
