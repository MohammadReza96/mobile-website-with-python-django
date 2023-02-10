from django.shortcuts import render
from django.conf import settings
from django.views import View

# for loading media_url anywhere & everytime
#------------------------------------------
def media_admin(request):
    return {'media_url':settings.MEDIA_URL}

#index page show
#--------------------------------------------------------- 
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'index_app/index.html')