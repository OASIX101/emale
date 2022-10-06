from rest_framework.decorators import APIView, action, api_view, permission_classes, authentication_classes
from rest_framework import status
from .models import CustomUser
from rest_framework.response import Response
from .serializers import CustomUserSerializer, LogInSerializer, LogOutSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .permissions import IsAdminOnly, IsUserAuthenticated
from django.contrib.auth import logout, authenticate
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out
from rest_framework_simplejwt.tokens import RefreshToken, Token
from drf_yasg.utils import swagger_auto_schema

class CreateUser(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get(self, request, format=None):
        """Gets all the non-admin users and non-vendor users that are in the database"""

        obj = CustomUser.objects.filter(is_staff=False, is_vendor=False)
        serializer = CustomUserSerializer(obj, many=True)

        data = {
            'message': 'success',
            'user count': obj.count(),
            'data' : serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(method="get")
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOnly])
def get_staff_vendor(request):
    """Gets all the admin user and vendor user that are in the database"""

    obj = CustomUser.objects.filter(is_staff=True)
    objs = CustomUser.objects.filter(is_vendor=True, is_staff=False)

    serializer = CustomUserSerializer(obj, many=True)
    serializer2 = CustomUserSerializer(objs, many=True)

    data = {
        'message': 'success',
        'admins' : serializer.data,
        'vendors' : serializer2.data
    }
    return Response(data, status=status.HTTP_200_OK)

class UserEdit(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get_user(self, user_id):
        """This checks if the user id provided is a existing user"""
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound('User with id does not exist')

    @swagger_auto_schema(method="delete")
    @action(methods=["DELETE"], detail=True)
    def delete(self, request, user_id, format=None):
        """This function is responsible for deleting a new user"""
        if request.method == "DELETE":
            obj = self.get_user(user_id)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, user_id, format=None):
        """This method is used to deactivate a user from the database"""
        obj = self.get_user(user_id)
        obj.is_active = False
        obj.save()


        data = {
            'message': 'user successfully deactivated',
            'data': CustomUserSerializer(self.get_user(user_id)).data,
            'is_active': self.get_user(user_id).is_active
        }

        return Response(data, status=status.HTTP_200_OK)
    
@swagger_auto_schema(method='post', request_body=LogInSerializer)
@api_view(['POST'])
def login_view(request):
    '''this function is used to log users in'''
    if request.method == 'POST':
        serializer = LogInSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user:
            if user.is_active == True:
                try:
                    refresh_token = RefreshToken.for_user(user)

                    user_details = {}
                    user_details['id']   = user.id
                    user_details['username'] = user.username
                    user_details['email'] = user.email
                    user_details['is_vendor'] = user.is_vendor
                    user_details['refresh_token'] = str(refresh_token)
                    user_details['access_token'] = str(refresh_token.access_token)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                        'message' : 'success',
                        'data' : user_details,
                    }
        
                    return Response(data, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            
            else:
                data = {
                    'message'  : "failed",
                    'errors': 'This account is not active'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)


        else:
            data = {
                'message'  : "failed",
                'errors': 'Please provide a valid username and password'
                }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method="post",request_body=LogOutSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsUserAuthenticated])
def logout_view(request):
    """Log out a user by blacklisting their refresh token then making use of django's internal logout function to flush out their session and completely log them out.
    Returns:
        Json response with message of success and status code of 204.
    """
    
    serializer = LogOutSerializer(data=request.data)
    
    serializer.is_valid()
    
    try:
        token = RefreshToken(token=serializer.validated_data["refresh_token"])
        token.blacklist()
        user=request.user
        user_logged_out.send(sender=user.__class__,
                                        request=request, user=user)
        logout(request)
        
        return Response({"message": "success"}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({"message": "failed", "error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method="get")
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOnly])
def activate(request, user_id):
    """This method is used to activate a user from the database"""
    try:
        obj = CustomUser.objects.get(id=user_id)
        obj.is_active = True
        obj.save()


        data = {
            'message': 'user successfully activated',
            'data': CustomUserSerializer(obj).data,
            'is_active': obj.is_active
        }

        return Response(data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        raise NotFound(detail={'message': 'user not found'})