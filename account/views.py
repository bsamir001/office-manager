from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import userregisterform,VerifycodeForm,User_RegisterForm
from .utils import send_otp_code
import random
from .models import Otpcode,User,patent
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
class userregisterviews(View):
    form_class=userregisterform
    template_name='accounts/register.html'
    def get(self,request):
        form=self.form_class
        return render(request,self.template_name,{'form':form})
    #برای ذخیره دوباره اطلاعات و استفداه مجدد در برنامه
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            user1 = User.objects.filter(phone_number=phone).exists()
            if user1:
                random_code=random.randint(1000,9999)
                send_otp_code(form.cleaned_data['phone'],random_code)
                Otpcode.objects.create(phone_number=phone,code=random_code)
                request.session['user_registration_info'] = {
                    'phone_number':phone,
                }
                messages.success(request, 'we sent you code', 'success')
                return redirect('account:verify_code')
            else:
                random_code = random.randint(1000, 9999)
                send_otp_code(form.cleaned_data['phone'], random_code)
                Otpcode.objects.create(phone_number=form.cleaned_data['phone'],code=random_code)
                request.session['user_registration_info']={
                    'phone_number':form.cleaned_data['phone'],
                }
                messages.success(request,'we sent you code','success')
                return redirect('account:verify_code')
        return render(request,self.template_name,{'form':form})
class userregisterverifycodeview(View):
    form_class=VerifycodeForm
    def get(self,request):
        form=self.form_class
        return render(request,'accounts/verify.html',{'form': form})
    def post(self,request):
        user_session = request.session.get('user_registration_info')
        if user_session:
            phone_number = user_session.get('phone_number')
            code_instance = Otpcode.objects.get(phone_number=phone_number)
            form = self.form_class(request.POST)
            if form.is_valid():
                    user1 = User.objects.filter(phone_number=phone_number).exists()
                    print(user1)
                    if user1:
                        cd = form.cleaned_data
                        if cd['code']==code_instance.code:
                                messages.success(request,'you registerd333','success')
                                user=User.objects.get(phone_number=phone_number)
                                code_instance.delete()
                                print(user)
                                if user is not None:
                                    if user.is_active:
                                        login(request, user)
                                        messages.success(request, 'احراز هویت با موفقیت انجام شد', 'success')
                                        return redirect('account:deatel')
                                    else:
                                        return messages.error(request, 'حساب غیرفعال است', 'warning')
                                else:
                                    messages.error(request, 'کاربری با این اطلاعات وجود ندارد', 'warning')
                                    return redirect('account:register')
                        else:
                            messages.error(request,'this code is wrong','danger')
                            return redirect('account:verify_code')
                    else:
                        cd=form.cleaned_data
                        if cd['code']==code_instance.code:
                            User.objects.create_user(user_session['phone_number'])#user_session['password']
                            code_instance.delete()
                            messages.success(request,'you registerd','success')
                            user = User.objects.get(phone_number=phone_number)
                            login(request, user)
                            return redirect('account:register')
                        else:
                            messages.error(request, 'this code is wrong', 'danger')
                            return redirect('account:verify_code')
        else:
            messages.error(request, 'User registration information not found', 'danger')
            return redirect('account:verify_code')
@method_decorator(login_required, name='dispatch')
class User_register(View):
    form_class=User_RegisterForm
    def get(self,request):
        form=self.form_class
        return render(request,'accounts/registerdata.html',{'form':form})
    def post(self,request):
        user_id = request.user
        form = self.form_class(request.POST)
        contaxt={'form':form,'user':user_id}
        if form.is_valid():
            patent1=form.save(commit=False)
            patent1.user = user_id
            patent1.save()
        return render(request,'accounts/registerdata.html',contaxt)
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logout was successfully', 'success')
        return redirect('account:test')


class Deatel_register(View):

    def get(self, request):
        if request.user.is_authenticated:
            # اگر کاربر لاگین کرده باشد
            user = request.user
            patents = patent.objects.filter(user=user)
            if patents.exists():
                patent_obj = patents.first()
                context = {'user': user, 'patent': patent_obj}
                return render(request, 'accounts/deatel.html', context)
            else:
                # اگر کاربر لاگین کرده باشد اما مدل Patent مرتبط با کاربر یافت نشد
                return render(request, 'no_patent.html')
        else:
            # اگر کاربر لاگین نکرده باشد
            return render(request, 'not_logged_in.html')














''' def get(self,request):
        model=patent
        form={'form':model}
        return render(request,'accounts/deatel.html',form)
    def post(self,request,patent_id):
        model = patent
        form = {'form': model}
        patent1= patent.objects.filter(user=patent.user)
        if patent1.exists():
            form = patent1.first()
            context = {'patent': form}
            return render(request, 'accounts/deatel.html', context)
        else:
            # مدل با شناسه مورد نظر یافت نشد
            return render(request, 'accounts/deatel.html')'''
#وصل کردن اطلاعات کاربر به اطلاعات قلی اش مونده اس
