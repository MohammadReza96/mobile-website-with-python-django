from django.shortcuts import render
from django.views import View
#----------------------------------------------------- create view for favorite products
class AddToFavoriteView(View):
    def get(self,request,*args,**kwargs):
        pass