from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from apps.products.models import Product
from .models import Scoring
from django.db.models import Avg

#-------------------------------------------- scoring view
class UserScoreView(View):
    def get(self,request,*args,**kwargs):
        product_id=request.GET.get('product_id')
        score=request.GET.get('score')
        product=Product.objects.get(id=int(product_id))
        Scoring.objects.create(
            product=product,
            scoring_user=request.user,
            score=int(score)
        )
        return HttpResponse('امتیاز شما با موفقیت ثبت شد')


# class AverageScoreUpdateView(View):
#     def get(self,request,*args,**kwargs):
#         average_score=Scoring.objects.all().aggregate(average_score=Avg('score'))['average_score']
#         return HttpResponse(average_score)
