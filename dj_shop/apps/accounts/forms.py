from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from apps.accounts.models import CustomUser

#####################################################################################################
#####################################################################################################
######################################################################## create user from admin panel
#--------------------------------------------------------------------------------- user creation form
class UserCreationForm(ModelForm):
    password =forms.CharField(label='Password',widget=forms.PasswordInput()) 
    re_password =forms.CharField(label='RePassword',widget=forms.PasswordInput())  # for checking password validation
    
    class Meta:
        model=CustomUser
        fields=['mobile_number','email','name','family','gender']
    
    # check password validation
    def clean_re_password(self):
        pass1=self.cleaned_data['password']
        pass2=self.cleaned_data['re_password']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز ها باهم یکسان نیست')
        return pass2
    
    def save(self,commit=True):   #commit use for final confirm
        user=super().save(commit=False)  # if commit=False so user does not save until we save it manualy
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()  # we save user manually
        return user
#---------------------------------------------------------------------------------user modifying form
class UserChangeForm(ModelForm):
    password=ReadOnlyPasswordHashField(help_text='برای تغییر رمز عبور از <a href="../password">لینک</a> زیر اقدام کنید')  # for hashing the new password
    class Meta:
        model=CustomUser
        fields=['mobile_number','password','email','name','family','gender','is_active','is_admin']
#####################################################################################################
#####################################################################################################
############################################################################### create user from site
#---------------------------------------------------------------------------------normal user creation form
class RegisterUserForm(ModelForm):
    password =forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    re_password =forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))

    
    class Meta:
        model=CustomUser
        fields=[
            'mobile_number',
            'password',
            # 'name','family','email'
            ]
        
        widgets={
            'mobile_number': forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'}),
            # 'name': forms.TextInput(attrs={'class':'form-control','placeholder':'نام را وارد کنید'}),
            # 'family': forms.TextInput(attrs={'class':'form-control','placeholder':'فامیلی را وارد کنید'}),
            # 'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل را وارد کنید'}),
        }

    def clean_re_password(self):
        pass1=self.cleaned_data['password']
        pass2=self.cleaned_data['re_password']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز ها باهم یکسان نیست')
        return pass2
#---------------------------------------------------------------------------------verify user creation form
class VerifyRegisterForm(forms.Form):
    active_code=forms.CharField(
        label='کد فعال سازی',
        error_messages={'required':'این فیلد نمی تواند خالی باشد','invalid':'کد وارد شده صحیح نیست'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد فعال سازی را وارد کنید'})
        )
#--------------------------------------------------------------------------------- user login form
class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label='موبایل خود را وارد کنید',error_messages={'required':'این فیلد نمی تواند خالی باشد','invalid':'موبایل وارد شده صحیح نیست'},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل خود را وارد کنید'}))
    password =forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'})) 
#--------------------------------------------------------------------------------- user forget password 
class ChangePassword(forms.Form):
    password =forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'})) 
    re_password =forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))

    def clean_re_password(self):
        pass1=self.cleaned_data['password']
        pass2=self.cleaned_data['re_password']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز ها باهم یکسان نیست')
        return pass2
#--------------------------------------------------------------------------------- user forget password 
class RememberPassword(forms.Form):
    mobile_number=forms.CharField(
        label='شماره موبایل',
        error_messages={'required':'این فیلد نمی تواند خالی باشد','invalid':'کد وارد شده صحیح نیست'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'})
        )