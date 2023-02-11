from django.shortcuts import render,redirect
from apps.accounts.forms import RegisterUserForm,VerifyRegisterForm,LoginUserForm,ChangePassword,RememberPassword
from apps.accounts.models import CustomUser
from django.views import View
from modules.kavehnegar_module import send_sms
from modules.random_code_maker import code_maker
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


#----------------------------------------------------------------------------------------------- sign up user
class RegisterUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        register_form=RegisterUserForm()
        return render(request,'account_app/register_user_form.html',{'register_form':register_form})
    
    def post(self,request,*args,**kwargs):
        get_form=RegisterUserForm(request.POST)
        if get_form.is_valid():
            user=get_form.cleaned_data                            # first clean data
            active_code=code_maker(6)                     # second create active code
            CustomUser.objects.create_user(                       # third create user
                mobile_number=user['mobile_number'],
                active_code=active_code,
                password=user['password'],
                # name=user['name'],
                # family=user['family'],
                # email=user['email']
            )
            send_sms(user['mobile_number'],f'کد فعال سازی حساب شما {active_code} می باشد')       # fourth send active code sms
            
            request.session['user_session']={                     # fifth create session for verifying user in verfiy page
                'active_code':str(active_code),
                'mobile_number':str(user['mobile_number']),
                'remember_password': False
            }
            

            messages.success(request,'اطلاعات شما با موفقیت ثبت شد. لطفا کد فعال سازی پیامک شده را وارد کنید','success')
            return redirect('accounts:verify')
        
        return render(request,'account_app/register_user_form.html',{'register_form':get_form})

#----------------------------------------------------------------------------------------------- verify user
class VerifyRegisterUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        verify_register_form=VerifyRegisterForm()
        return render(request,'account_app/verify_register_form.html',{'verify_register_form':verify_register_form})
    
    def post(self,request,*args,**kwargs):
        get_form=VerifyRegisterForm(request.POST)
        if get_form.is_valid():
            verify_user=get_form.cleaned_data
            user_sessions=request.session['user_session']
            if verify_user['active_code']==user_sessions['active_code']:
                if user_sessions['remember_password'] ==False:
                    user=CustomUser.objects.get(mobile_number=user_sessions['mobile_number'])
                    user.is_active=True
                    user.active_code=code_maker(6)
                    user.save()
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('accounts:login')
                else:
                    return redirect('accounts:changepassword')
                
            else:
                messages.error(request,'کد وارد شده معتبر نیست','danger')
                return render(request,'account_app/verify_register_form.html',{'verify_register_form':get_form})
            
        messages.error(request,'اطلاع وارد شده معتبر نیست','danger')
        return render(request,'account_app/verify_register_form.html',{'verify_register_form':get_form})

#----------------------------------------------------------------------------------------------- login user
class LoginUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kargs):
        login_form=LoginUserForm()
        return render(request,'account_app/login_user_form.html',{'login_form':login_form})
    
    def post(self,request,*args,**kargs):
        get_form=LoginUserForm(request.POST)
        if get_form.is_valid():
            user=get_form.cleaned_data
            user_data=authenticate(username=user['mobile_number'],password=user['password'])
            if user_data is not None:
                db_user=CustomUser.objects.get(mobile_number=user['mobile_number'])
                if db_user.is_active==True:
                    if db_user.is_admin==False :
                        messages.success(request,'ورود با موفقیت انجام شد','success')
                        
                        login(request,user_data)
                        
                        next_url=request.GET.get('next')
                        if next_url is not None:
                            return redirect(next_url)
                        else:
                            return redirect('index:home')
                        
                    else:
                        messages.error(request,'کاربر ادمین نمی تواند از این بخش وارد شود','warning')
                        return render(request,'account_app/login_user_form.html',{'login_form':get_form})
                else:
                    # print('index-not_active')  # for testing
                    messages.error(request,'حساب کاربری شما فعال نمی باشد','danger')
                    return render(request,'account_app/login_user_form.html',{'login_form':get_form})
            else:
                # print('index-mistake')   # for testing
                messages.error(request,'شماره موبایل یا رمز عبور را به درستی وارد نکرده اید!','danger')
                return render(request,'account_app/login_user_form.html',{'login_form':get_form})
        else:
            # print('index-mistake-FIRST')   # for testing
            return render(request,'account_app/login_user_form.html',{'login_form':get_form})

#-----------------------------------------------------------------------------------------------  user change password
class ChangePasswordView(View):
    
    def get(self,request,*args,**kargs):
        change_password=ChangePassword()
        return render(request,'account_app/change_password.html',{'change_password':change_password})
    
    def post(self,request,*args,**kargs):
        get_form=ChangePassword(request.POST)
        if get_form.is_valid():
            user_data=get_form.cleaned_data
            user_sessions=request.session['user_session']
            try:
                user=CustomUser.objects.get(mobile_number=user_sessions['mobile_number'])
                user.set_password(user_data['password'])
                user.active_code=code_maker(6)
                user.save()
                messages.success(request,'رمز شما با موفقیت  تغییر کرد','success')
                
                request.session['user_session']={
                                'active_code':'',
                                'mobile_number':'',
                                'remember_password': False}
                return redirect('accounts:login')
            except:
                messages.error(request,'شماره موبایل موجود نیست','danger')
                return render(request,'account_app/change_password.html',{'change_password':get_form})

        else:
            messages.error(request,'رمز ها یکسان نیست','danger')
            return render(request,'account_app/change_password.html',{'change_password':get_form})

#-----------------------------------------------------------------------------------------------  user remember password
class RememberPasswordView(View):
    
    def get(self,request,*args,**kargs):
        remember_password=RememberPassword()
        return render(request,'account_app/remember_password.html',{'remember_password':remember_password})
    
    def post(self,request,*args,**kargs):
        get_form=RememberPassword(request.POST)
        if get_form.is_valid():
            user_data=get_form.cleaned_data
            try:
                user=CustomUser.objects.get(mobile_number=user_data['mobile_number'])
                active_code=code_maker(6)
                user.active_code=active_code
                user.save()
                send_sms(user_data['mobile_number'],f'کد تایید شماره موبایل شما {active_code} است')
                
                request.session['user_session']={
                    'active_code':str(active_code),
                    'mobile_number':str(user_data['mobile_number']),
                    'remember_password': True
                }
                
                messages.success(request,'جهت تغییر رمز عبور خود  کد دریافت شده را وارد کنید','success')
                return redirect('accounts:verify')
            except:
                messages.error(request,'شماره موبایل موجود نیست','danger')
                return render(request,'account_app/remember_password.html',{'remember_password':get_form})
        else:
            messages.error(request,'فیلد ها را به درستی وارد کنید','danger')
            return render(request,'account_app/remember_password.html',{'remember_password':get_form})

#----------------------------------------------------------------------------------------------- logout user
class LogoutUser(View):
    # use for check in user is log in /log out / register /verify already
    def dispatch(self, request, *args, **kwargs): 
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        session_data=request.session.get('shop_card')
        logout(request)
        request.session['shop_card']=session_data
        return redirect('index:home')

#-----------------------------------------------------------------------------------------------  userpanel
class UserPanelView(LoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        
        return render(request,'account_app/user_panel.html',{'user':request.user})