import re
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated and request.user.is_staff == True:
            return True
        
        else:
            raise PermissionDenied(detail={'message': 'Permission denied. User is not an admin'})

class IsUserAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET':
            if request.user.is_authenticated and request.user.is_active == True:
                return True

            else:
                raise PermissionDenied(detail={'message':'non-company users are not allowed to access this page'})

        else:
            if request.user.is_authenticated and request.user.is_staff == True:
                return True

            else:
                raise PermissionDenied(detail={'message':'Permission denied. user is not an admin'})

class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_active == True:
            if request.user.is_vendor == False:
                return True

            else:
                raise PermissionDenied(detail={'message': 'vendor users are not allowed to access this page.'})

        else:
            raise PermissionDenied(detail={'message':'non-company users are not allowed to access this page'})

class IsVendor(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.method == 'GET':
            if request.user.is_authenticated and request.user.is_staff == True:
                return True

        else:
            if request.user.is_authenticated and request.user.is_vendor == True :
                return True

            else:
                raise PermissionDenied(detail={'message':'Permission denied. user is not a vendor.'})


        