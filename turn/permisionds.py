from rest_framework.permissions import BasePermission,SAFE_METHODS


class ISoner(BasePermission):
    def has_permission(self, request, view):#قبل از ورد بررسی میکند
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):#بعد از ورد بررسی میکند
        if request.method in SAFE_METHODS:
            return True
        return obj.user==request.user