from django.shortcuts import render,get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Blog,CommentBlog

#------------------------------------------------------------------------------ blogs page  view 
class BlogsView(View):
    def get(self,request,*args,**kwargs):
        blogs=Blog.objects.filter(blog_is_active=True).order_by('blog_publish_date')
        
        
        pagienator=Paginator(blogs,3) 
        page_number=request.GET.get('page')             # get current page number
        page_obj=pagienator.get_page(page_number) 
        return render(request,'blogs_app/blogs.html',{"page_obj":page_obj})

#------------------------------------------------------------------------------ blog page  view 
class BlogView(View):
    def get(self,request,*args,**kwargs):
        blog=get_object_or_404(Blog,blog_slug=kwargs['slug'])
        return render(request,'blogs_app/blog.html',{"blog":blog})
