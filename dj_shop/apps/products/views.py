from django.shortcuts import render,get_object_or_404
from apps.products.models import Product,ProductGroup,FeatureValue,Brand
from django.views import View
from django.db.models import Q,Count,Max,Min,Avg
from django.http import JsonResponse
from django.core.paginator import Paginator

#------------------------------------------------------------------------------------------------ get product group 
def get_product_group():
    return ProductGroup.objects.filter(Q(group_isactive=True) & Q(group_parent=None))
#------------------------------------------------------------------------------------------------ cheapest product in site
def cheapest_product(request,*args,**kwargs):
    cheap_product=Product.objects.filter(product_isactive=True).order_by('product_price')[:4]
    product_group=get_product_group()
    context={
            'product': cheap_product,
            'product_group':product_group
    }
    return render(request,'product_app/partials/cheapest_product.html',context)
#------------------------------------------------------------------------------------------------ newest product in site
def newest_product(request,*args,**kwargs):
    newest_product=Product.objects.filter(product_isactive=True).order_by('-product_publish_date')[:8]
    product_group=get_product_group()
    context={
            'product': newest_product,
            'product_group':product_group
    }
    return render(request,'product_app/partials/newest_product.html',context)
#------------------------------------------------------------------------------------------------ Favorite Product  in site
def favorite_product(request,*args,**kwargs):
        product_group=ProductGroup.objects.filter(Q(group_isactive=True) & ~Q(group_parent=None)).annotate(product_count= Count('products_of_group')).order_by('-product_count')[:6]
        context={
            'product_group':product_group
        }
        return render(request,'product_app/partials/favorite_product.html',context)
#------------------------------------------------------------------------------------------------ related Product in product detail page
def related_product(request,*args,**kwargs):
        curent_product=get_object_or_404(Product,product_slug=kwargs['slug']) # new way to get data from database
        related_product=[]
        for group in curent_product.product_group.all():
            related_product.extend(Product.objects.filter(Q(product_isactive=True) & Q(product_group=group) & ~Q(id=curent_product.id)))
        context={
            'related_product':related_product
        }

        return render(request,'product_app/partials/related_product.html',context)
#------------------------------------------------------------------------------------------------ filter product base on group name
def get_product_group_filter(request):
    product_group_filter=ProductGroup.objects.annotate(count= Count('products_of_group'))\
        .filter(Q(group_isactive=True) & ~Q(count=0) & ~Q(group_parent=None))\
            .order_by('-count')
    return render(request,'product_app/partials/product_group_filter.html',{'product_groups':product_group_filter})
#------------------------------------------------------------------------------------------------ filter product base on brands
def get_brand(request,*args,**kwargs):
    product_group=get_object_or_404(ProductGroup,group_slug=kwargs['slug'])  # when we enter productbygroup page , we have slig as a input for this page
    brand_list_id=product_group.products_of_group.filter(product_isactive=True).values('product_brand__brand_slug')
    print(brand_list_id)
    brands=Brand.objects.filter(brand_slug__in=brand_list_id).annotate(count=Count('brands')).filter(~Q(count=0)).order_by('brand_name')
    
    return render (request,'product_app/partials/product_brand_filter.html',{'brands':brands})
#------------------------------------------------------------------------------------------------ filter product base on other filters
def get_other_features_for_each_group(request,*args,**kwargs):
    product_group=get_object_or_404(ProductGroup,group_slug=kwargs['slug'])  
    feature_list_for_each_product_group=product_group.features_of_group.all()
    feature_list_dic=dict()
    
    for feature in feature_list_for_each_product_group:
        feature_list_dic[feature]=feature.feature_value.all()
    
    return render(request,'product_app/partials/product_other_filter.html',{'feature_list_dic':feature_list_dic})





#------------------------------------------------------------------------------------------------ product detail in site
class ProductDetailView(View):
    def get(self,request,slug):
        
        product=get_object_or_404(Product,product_slug=slug) 
        if product.product_isactive:
            return render(request,'product_app/product_detail.html',{'product':product})
#------------------------------------------------------------------------------------------------ show list of product group in 1 page
class ProductGroupView(View):
    def get(self,request,*args,**kwargs):
        product_group=ProductGroup.objects.filter(Q(group_isactive=True) & ~Q(group_parent=None)).annotate(product_count= Count('products_of_group')).order_by('-product_count')
        context={
            'product_group':product_group
        }
        return render(request,'product_app/product_group.html',context)

#------------------------------------------------------------------------------------------------ show list of product of each group in 1 page
class ProductByGroupView(View):
    #################################################################################################################### how I filter the product in page 
    #####################################################################################################################################################
    #####################################################################################################################################################
    # with javascript I add sort_type as a querystring in urls  the page will refresh after call  the javascript function
    # with form I add cur_prices & filter_brand & feature_filter (other filters) as a querystring in urls and the page will refresh after submit the form
    #####################################################################################################################################################
    #####################################################################################################################################################
    #####################################################################################################################################################

    def get(self,request,*args,**kwargs):
        current_group=get_object_or_404(ProductGroup,group_slug=kwargs['slug']) # for get sth in backend from front
        product=Product.objects.filter(Q(product_isactive=True) & Q(product_group=current_group)).order_by('-product_price')   # all data we get from database

        res_aggre=product.aggregate(max_price=Max('product_price'),min_price=Min('product_price'),avg_price=Avg('product_price'))
                
        #-------------------------------------------------------------------------- price filter
        cur_prices=request.GET.get('price')
        if cur_prices:
            product=product.filter(product_price__lte=cur_prices)
        #-------------------------------------------------------------------------- brand filter 
        filter_brand=request.GET.getlist('brand')  # get data from checkbox so we use getlist to get data
        if filter_brand:
            product=product.filter(product_brand__id__in=filter_brand)
        #-------------------------------------------------------------------------- other feature base on the productgroup
        feature_filter=request.GET.getlist('feature')
        if feature_filter:
            product=product.filter(product_features__filter_value__id__in=feature_filter).distinct()
        #-------------------------------------------------------------------------- sort type
        sort_type=request.GET.get('sort_type')     # with javascript I add sort_type as a querystring in urls
    
        if not sort_type:
            sort_type="0"
        elif sort_type=="1":
            product=product.order_by('-product_price')
        elif sort_type=="2":
            product=product.order_by('product_price')

        slug=kwargs['slug']
        # -------------------------------------------------------------------------- set number of product to show in a page
        product_per_page=2   # number of product in each page
        select_number_show=request.GET.get('select_number_show')

        if not select_number_show:
            select_number_show="9"
        elif select_number_show=="1":
            product_per_page=1
            select_number_show="1"
        elif select_number_show=="2":
            product_per_page=2
            select_number_show="2"
        elif select_number_show=="4":
            product_per_page=4
            select_number_show="4"
        elif select_number_show=="6":
            product_per_page=6
            select_number_show="6"
        else:
            product_per_page=9
            select_number_show="9"
        
        # pagenate 
        pagienator=Paginator(product,product_per_page) 
        page_number=request.GET.get('page')             # get current page number
        page_obj=pagienator.get_page(page_number)       # show the number of product after seting a pagenator
        # -------------------------------------------------------------------------- show number of product before and after set a filter
        product_count=len(product)                     

        context={
            'product':product,
            'current_group':current_group,
            'res_aggre':res_aggre,
            'product_count':product_count,
            'page_obj':page_obj,
            'cur_prices':cur_prices,
            'slug':slug,
            'sort_type':sort_type,
            'select_number_show':select_number_show,
        }
        return render(request,'product_app/ProductByGroup.html',context)