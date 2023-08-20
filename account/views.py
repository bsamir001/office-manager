from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .utils import send_otp_code
import random
from .models import Otpcode,User,patent
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import userrigister_selizer,Verifycodeselizer,User_Registerselizer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class userregisterviews(APIView):
    def get(self,request):
        users = User.objects.all()
        selizer=userrigister_selizer(many=True)
        return Response(selizer.data)
    #برای ذخیره دوباره اطلاعات و استفداه مجدد در برنامه
    #@csrf_protect
    csrf_protected_method = method_decorator(csrf_protect)
    def post(self,request):
        ser_data = userrigister_selizer(data=request.POST)
        if ser_data.is_valid():
            phone = ser_data.data.get('phone')
            user1 = User.objects.filter(phone_number=phone).exists()
            if user1:
                random_code=random.randint(1000,9999)
                send_otp_code(ser_data.validated_data['phone'],random_code)
                Otpcode.objects.create(phone_number=phone,code=random_code)
                request.session['user_registration_info'] = {
                    'phone_number':phone,
                }
                url_addres = reverse('account:verify_code',)
                return Response({'message': 'okkk', 'url_addres': url_addres},
                                status=status.HTTP_200_OK)
            else:
                random_code = random.randint(1000, 9999)
                send_otp_code(ser_data.validated_data['phone'], random_code)
                Otpcode.objects.create(phone_number=ser_data.validated_data['phone'],code=random_code)
                request.session['user_registration_info']={
                    'phone_number':ser_data.validated_data['phone'],
                }
                messages.success(request,'we sent you code','success')
                url_addres = reverse('account:verify_code', )
                return Response({'message': 'okkk+++', 'url_addres': url_addres},
                                status=status.HTTP_200_OK)
        return Response({'message': 'eroor',},
                        status=status.HTTP_400_BAD_REQUEST)
class userregisterverifycodeview(APIView):
    def get(self,request):
        serializer = Verifycodeselizer(many=True)
        return Response(serializer.data)
    def post(self,request):
        user_session = request.session.get('user_registration_info')
        if user_session:
            phone_number = user_session.get('phone_number')
            code_instance = Otpcode.objects.get(phone_number=phone_number)
            ser_data = Verifycodeselizer(data=request.POST)
            if ser_data.is_valid():
                    user1 = User.objects.filter(phone_number=phone_number).exists()
                    print(user1)
                    if user1:
                        cd = ser_data.validated_data
                        if cd['code']==code_instance.code:
                                messages.success(request,'you registerd333','success')
                                user=User.objects.get(phone_number=phone_number)
                                code_instance.delete()
                                print(user)
                                if user is not None:
                                    if user.is_active:
                                        login(request, user)
                                        url_addres = reverse('account:deatel', )
                                        return Response({'message': 'احراز هویت با موفقیت انجام شد', 'url_addres': url_addres},
                                                        status=status.HTTP_200_OK)
                                    else:
                                        return Response(
                                            {'message': 'حساب غیرفعال است',},
                                            status=status.HTTP_204_NO_CONTENT)
                                else:
                                    url_addres = reverse('account:register', )
                                    return Response({'message': 'حساب یافت نشد ','url_addres': url_addres },status=status.HTTP_404_NOT_FOUND)
                        else:
                            url_addres = reverse('account:verify_code', )
                            return Response({'message': 'code wrong ', 'url_addres': url_addres},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        cd=ser_data.validated_data
                        if cd['code']==code_instance.code:
                            User.objects.create_user(user_session['phone_number'])#user_session['password']
                            code_instance.delete()
                            messages.success(request,'you registerd','success')
                            user = User.objects.get(phone_number=phone_number)
                            login(request, user)
                            url_addres = reverse('account:register', )
                            return Response({'message': 'حساب  ', 'url_addres': url_addres},
                                            status=status.HTTP_200_OK)

                        else:
                            url_addres = reverse('account:verify_code', )
                            return Response({'message': 'code wrong ', 'url_addres': url_addres},
                                            status=status.HTTP_400_BAD_REQUEST)
        else:
            url_addres = reverse('account:verify_code', )
            return Response({'message': 'code wrong ', 'url_addres': url_addres},
                            status=status.HTTP_400_BAD_REQUEST)
permission_classes = [IsAuthenticated]
class User_register(APIView):
    def get(self,request):
        serializer = User_Registerselizer(many=True)
        return Response(serializer.data)

    csrf_protected_method = method_decorator(csrf_protect)
    @csrf_protect
    def post(self,request):
        user_id = request.user
        ser_data = User_Registerselizer(data=request.POST)

        #contaxt={'serdata':ser_data,'user':user_id}
        if ser_data.is_valid():
            patent1=ser_data.save(commit=False)
            patent1.user = user_id
            patent1.save()
            return Response({'message': 'suceese ',},
                            status=status.HTTP_200_OK)
            
permission_classes = [IsAuthenticated]
class UserLogoutView(LoginRequiredMixin,APIView):
    def get(self, request):
        logout(request)
        return Response({'message': 'sucess ',},
                        status=status.HTTP_200_OK)

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



