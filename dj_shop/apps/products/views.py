from django.shortcuts import render,get_object_or_404
from apps.products.models import Product,ProductGroup,FeatureValue,Brand
from django.views import View
from django.db.models import Q,Count,Max,Min,Avg
from django.http import JsonResponse
from django.core.paginator import Paginator

#------------------------------------------------------------------------------------------------ get product group 
def get_product_group():
    return ProductGroup.objects.filter(Q(group_isactive=True) & Q(group_parent=None))
#------------------------------------------------------------------------------------------------ render partials parts
# cheapest product in site
def cheapest_product(request,*args,**kwargs):
    cheap_product=Product.objects.filter(product_isactive=True).order_by('product_price')[:4]
    product_group=get_product_group()
    context={
            'product': cheap_product,
            'product_group':product_group
    }
    return render(request,'product_app/partials/cheapest_product.html',context)
#------------------------------------------------------------------------------------------------    
# newest product in site
def newest_product(request,*args,**kwargs):
    newest_product=Product.objects.filter(product_isactive=True).order_by('-product_publish_date')[:8]
    product_group=get_product_group()
    context={
            'product': newest_product,
            'product_group':product_group
    }
    return render(request,'product_app/partials/newest_product.html',context)
#------------------------------------------------------------------------------------------------
# Favorite Product  in site
def favorite_product(request,*args,**kwargs):
        product_group=ProductGroup.objects.filter(Q(group_isactive=True) & ~Q(group_parent=None)).annotate(product_count= Count('products_of_group')).order_by('-product_count')[:6]
        context={
            'product_group':product_group
        }
        return render(request,'product_app/partials/favorite_product.html',context)
#------------------------------------------------------------------------------------------------
# related Product  in product detail page
def related_product(request,*args,**kwargs):
        curent_product=get_object_or_404(Product,product_slug=kwargs['slug']) # new way to get data from database
        related_product=[]
        for group in curent_product.product_group.all():
            related_product.extend(Product.objects.filter(Q(product_isactive=True) & Q(product_group=group) & ~Q(id=curent_product.id)))
        context={
            'related_product':related_product
        }

        return render(request,'product_app/partials/RelatedProduct.html',context)











#------------------------------------------------------------------------------------------------ page details parts

# show list of product group in 1 page
class ProductGroupView(View):
    def get(self,request,*args,**kwargs):
        product_group=ProductGroup.objects.filter(Q(group_isactive=True) & ~Q(group_parent=None)).annotate(product_count= Count('products_of_group')).order_by('-product_count')
        context={
            'product_group':product_group
        }
        return render(request,'product_app/product_group.html',context)