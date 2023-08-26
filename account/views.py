from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .utils import send_otp_code
import random
from .models import Otpcode, User, patent
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import UserRegisterSerializer, VerifyCodeSerializer, UserInfoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework import status
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserRegisterViews(APIView):
    def get(self, request):
        user1 = User.objects.all()
        selizer = UserRegisterSerializer(many=True)
        return Response(selizer.data)

    # برای ذخیره دوباره اطلاعات و استفداه مجدد در برنامه
    # csrf_protected_method = method_decorator(csrf_protect) اضافی
    # @method_decorator(csrf_protect)
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        print(ser_data)
        if ser_data.is_valid():
            phone = ser_data.data.get('phone')
            user1 = User.objects.filter(phone_number=phone).exists()
            if user1:
                random_code = random.randint(1000, 9999)
                send_otp_code(ser_data.validated_data['phone'], random_code)
                Otpcode.objects.create(phone_number=phone, code=random_code)
                request.session['user_registration_info'] = {
                    'phone_number': phone,
                }
                url_address = reverse('account:verify_code_api', )
                return Response({'message': 'success', 'url_address': url_address},
                                status=status.HTTP_200_OK)
            else:
                random_code = random.randint(1000, 9999)
                send_otp_code(ser_data.validated_data['phone'], random_code)
                Otpcode.objects.create(phone_number=ser_data.validated_data['phone'], code=random_code)
                request.session['user_registration_info'] = {
                    'phone_number': ser_data.validated_data['phone'],
                }
                messages.success(request, 'we sent you code', 'success')
                url_address = reverse('account:verify_code_api', )
                return Response({'message': 'success', 'url_address': url_address},
                                status=status.HTTP_200_OK)
        return Response({'message': 'error', },
                        status=status.HTTP_400_BAD_REQUEST)


class UserRegisterVerifyCodeView(APIView):
    def get(self, request):
        serializer = VerifyCodeSerializer(many=True)
        return Response(serializer.data)

    def post(self, request):
        user_session = request.session.get('user_registration_info')
        if user_session:
            phone_number = user_session.get('phone_number')
            code_instance = Otpcode.objects.get(phone_number=phone_number)
            ser_data = VerifyCodeSerializer(data=request.data)
            if ser_data.is_valid():
                user1 = User.objects.filter(phone_number=phone_number).exists()
                print(user1)
                if user1:
                    cd = ser_data.validated_data
                    if cd['code'] == code_instance.code:
                        messages.success(request, 'you registerd333', 'success')
                        user = User.objects.get(phone_number=phone_number)
                        code_instance.delete()
                        print(user)
                        if user is not None:
                            if user.is_active:
                                login(request, user)
                                url_address = reverse('account:detail_api', )
                                return Response({'message': 'success', 'url_address': url_address},
                                                status=status.HTTP_200_OK)
                            else:
                                return Response(
                                    {'message': 'حساب غیرفعال است', },
                                    status=status.HTTP_204_NO_CONTENT)
                        else:
                            url_address = reverse('account:register_api', )
                            return Response({'message': 'حساب یافت نشد ', 'url_address': url_address},
                                            status=status.HTTP_404_NOT_FOUND)
                    else:
                        url_address = reverse('account:verify_code_api', )
                        return Response({'message': 'code wrong ', 'url_address': url_address},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    cd = ser_data.validated_data
                    if cd['code'] == code_instance.code:
                        User.objects.create_user(user_session['phone_number'])  # user_session['password']
                        code_instance.delete()
                        messages.success(request, 'you registerd', 'success')
                        user = User.objects.get(phone_number=phone_number)
                        login(request, user)
                        url_address = reverse('account:register_api', )
                        return Response({'message': 'success', 'url_address': url_address},
                                        status=status.HTTP_200_OK)

                    else:
                        url_address = reverse('account:verify_code_api', )
                        return Response({'message': 'code wrong', 'url_address': url_address},
                                        status=status.HTTP_400_BAD_REQUEST)
        else:
            url_address = reverse('account:verify_code_api', )
            return Response({'message': 'code wrong', 'url_address': url_address},
                            status=status.HTTP_400_BAD_REQUEST)


class UserCompleteInfoView(APIView):
    permission_classes = [IsAuthenticated]

    # @csrf_exempt
    def get(self, request):
        user1 = patent.objects.all()
        serializer = UserInfoSerializer(user1, many=True)
        return Response(serializer.data)

    # csrf_protected_method = method_decorator(csrf_protect)
    # @csrf_exempt
    def post(self, request):
        user_id = request.user
        request.data["user"] = user_id
        print(request.data)

        print(1)
        ser_data = UserInfoSerializer(data=request.data)
        # contaxt={'serdata':ser_data,'user':user_id}
        if ser_data.is_valid():
            ser_data.save()
            # patent1 = ser_data.save(commit=False)
            # patent1.user = user_id
            # patent1.save()
            return Response({'message': 'success', },
                            status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]
    print(permission_classes)

    @csrf_protect
    def get(self, request):
        logout(request)
        return Response({'message': 'success', },
                        status=status.HTTP_200_OK)


class DetailRegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            # اگر کاربر لاگین کرده باشد
            user = request.user
            patents = patent.objects.filter(user=user)
            if patents.exists():
                patent_obj = patents.first()
                context = {'user': user, 'patent': patent_obj}
                return render(request, 'accounts/detail.html', context)
            else:
                # اگر کاربر لاگین کرده باشد اما مدل Patent مرتبط با کاربر یافت نشد
                return render(request, 'no_patent.html')
        else:
            # اگر کاربر لاگین نکرده باشد
            return render(request, 'not_logged_in.html')
