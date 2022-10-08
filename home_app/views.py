from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import ComUserChoice, MealList, VendorMeal
from home_accounts.permissions import IsVendor, IsUserAuthenticated, IsAdminOnly, IsUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from .serializers import MealListSerializer, MealListSerializer2, MealListSerializer3, MealOrderSerializer, MealOrderSerializer2, MealOrderSerializer3, MealOrderSerializer4, VendorSerializer, VendorSerializer2
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from datetime import datetime    

today = datetime.now()
day = today.strftime("%a")
day_num = today.strftime("%d")
month = today.strftime("%B")
year = today.strftime("%Y")

class MealListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserAuthenticated]

    def get(self, request, format=None):
        """This method retrieves the approved list of meals for that day
           It is only accessible to all users except anonymous users.
        """
        try:
            mealist = MealList.objects.get(day_num=day_num, month=month, year=year)
            serializer = MealListSerializer3(mealist)

            data = {
                'message': 'success',
                'meal-date': f'{day_num}-{month}-{year}',
                'data': serializer.data
            }
            
            return Response(data, status = status.HTTP_200_OK)        
            
        except MealList.DoesNotExist:
            raise NotFound(detail={'message': 'There is no meal list made for today. Try again later.'})

    @swagger_auto_schema(method='post', request_body=MealListSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """This method creates a new instance of meal list for a day.
           if there is a meal list present for that day, an error message will be returned as a response and guide.
           It is only accessible to admin users and vendors.
        """
        data = {}
        data['meal_id_1'] = request.data['meal_id_1']
        data['meal_id_2'] = request.data['meal_id_2']
        data['meal_id_3'] = request.data['meal_id_3']
        data['day'] = day
        data['day_num'] = day_num
        data['month'] = month
        data['year'] = year

        if data['day'] == 'Saturday' or data['day'] == 'Sunday':
            return Response(data={'message': 'meal list can only be posted on weekdays'})
        else:
            try: 
                unique = MealList.objects.get(day_num=data['day_num'], month=data['month'], year=data['year'])
                if unique:
                    return Response(data={'message': 'Cannot post two meal lists in a day. Try updating previous meal list.'}, status=status.HTTP_400_BAD_REQUEST)
            except MealList.DoesNotExist:
                serializer = MealListSerializer2(data=data)
                if serializer.is_valid():
                    meal1 = serializer.validated_data['meal_id_1']
                    meal2 = serializer.validated_data['meal_id_2']
                    meal3 = serializer.validated_data['meal_id_3']
                    
                    if meal1 != meal2 and meal1 != meal3:

                        if meal2 != meal1 and meal2 != meal3: 

                            if meal3 != meal1 and meal3 != meal2: 

                                if meal1 == meal2 == meal3:
                                    raise PermissionDenied(detail={'message':'cannot pick one meal more than once'})

                                else:
                                    try:
                                        meal1_check = VendorMeal.objects.get(meal=meal1, day_num=day_num, month=month, year=year)
                                        meal2_check = VendorMeal.objects.get(meal=meal2, day_num=day_num, month=month, year=year)
                                        meal3_check = VendorMeal.objects.get(meal=meal3, day_num=day_num, month=month, year=year)

                                        if meal1_check and meal2_check and meal3_check:
                                            serializer.save()
                                            
                                            data = {
                                                "message":"success"
                                            }

                                            return Response(data, status = status.HTTP_200_OK)
                                    except VendorMeal.DoesNotExist:
                                        raise NotFound(detail={'message': 'meal1 or meal2 or meal3 is not available for today'})
                                        
                            else:
                                raise PermissionDenied(detail={'message':'cannot pick one meal more than once'})

                        else:
                            raise PermissionDenied(detail={'message':'cannot pick one meal more than once'})

                    else:
                        raise PermissionDenied(detail={'message':'cannot pick one meal more than once'})
                else:
                    data = {
                        "message":"failed",
                        "error":serializer.errors
                    }
                
                    return Response(data, status = status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='put', request_body=MealListSerializer())
    @action(methods=['PUT'], detail=True)
    def put(self, request, format=None):
        """update a meal list for that day only. if there is no meal list for the day, an error message will be returned.
           It is only accessible to admin users and vendors.
        """
        try:
            mealist = MealList.objects.get(day_num=day_num, month=month, year=year)
    
            if mealist:            
                serializer = MealListSerializer(mealist, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serial = []
                    for obj in serializer.validated_data:
                        serial.append(obj)
                        
                    new = []

                    for i in serial:
                        valid = serializer.validated_data[i]
                        new.append(valid)
                    
                    for i in range(0, len(new)):
                        try:
                            food = MealList.objects.get(day_num=day_num, month=month, year=year)
                            print(food)
                            vendor = VendorMeal.objects.get(meal=new[i], day_num=day_num, month=month, year=year)
                            if vendor != food.meal_id_1 and vendor != food.meal_id_2 and vendor != food.meal_id_3:
                                continue
                            else:
                                raise PermissionDenied(detail={"message": "cannot update meal list, meal already exists in today's meal list"})

                        except VendorMeal.DoesNotExist:
                            raise NotFound(detail={'message': 'cannot update meal list, meal or meals provided are not available for today'})

                    serializer.save()
                    
                    data = {
                        "message":"success"
                    }

                    return Response(data, status = status.HTTP_200_OK)

                else:
                    data = {
                        "message":"failed",
                        "error":serializer.errors
                    }
                
                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
        except MealList.DoesNotExist:
            raise NotFound(detail={'message': 'There is no meal list made for today'})

    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)
    def delete(self, request, format=None):

        """Deletes the meal list made for that day.
           It is only accessible to admin users and vendors.
        """
        
        obj = MealList.objects.get(day_num=day_num, month=month, year=year)
        if obj:      
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise NotFound(detail={'message': 'There is no meal list made for today. Try again later.'})

class MealOrderView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]
    
    def get_meal_list(self, day_num, month, year):
        try:
            return MealList.objects.get(day_num=day_num, month=month, year=year)
        except MealList.DoesNotExist:
            raise NotFound(detail={'message': 'There is no meal list made for today'})

    def get(self, request, format=None):
        """This method retrieve a single user order made for today's meal list"""

        order_list = ComUserChoice.objects.filter(day_num=day_num, month=month, year=year, user=2)

        if order_list:
            serializer = MealOrderSerializer3(order_list, many=True)

            data = {
                'message': 'success',
                'order date': f'{day_num}-{month}-{year}',
                'data': serializer.data
            }
                
            return Response(data, status = status.HTTP_200_OK) 
        
        else:
            return Response(data={"message": "There is no order made by this user for today's meal"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='post', request_body=MealOrderSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """This method creates a new instance of meal list for that day.
           if there is a meal list present for that day, an error message will be returned as a response and guide.
        """
        data = {}
        data['user'] = request.user.id
        data['meal_order'] = request.data['meal_order']
        data['day'] = day
        data['day_num'] = day_num
        data['month'] = month
        data['year'] = year

        if data['user'] != None:
            if data['day'] == 'Saturday' or data['day'] == 'Sunday':
                return Response(data={'message': 'meal orders can only be posted on weekdays'})
            else:
                try: 
                    unique = ComUserChoice.objects.filter(day_num=data['day_num'], month=data['month'], year=data['year'], user=data['user'])
                    if unique:
                        return Response(data={'message': 'Cannot post two orders in a day. Try updating previous order.'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        
                        data['meal_list'] = self.get_meal_list(data['day_num'], data['month'], data['year']).id
                        serializer = MealOrderSerializer2(data=data)
                        
                        if serializer.is_valid():
                            try:
                                vendor = VendorMeal.objects.get(meal=serializer.validated_data['meal_order'], day_num=day_num, month=month)
                                if vendor:
                                    serializer.save()
                                    
                                    data = {
                                        "message":"success"
                                    }

                                    return Response(data, status = status.HTTP_200_OK)
                            except VendorMeal.DoesNotExist:
                                raise NotFound(detail={'message': 'meal item with id is not available'})

                        else:
                            data = {
                                "message":"failed",
                                "error":serializer.errors
                            }
                        
                            return Response(data, status = status.HTTP_400_BAD_REQUEST)

                except MealList.DoesNotExist:
                    raise NotFound(detail={'message': 'order not found'})
        else:
            raise PermissionDenied(detail={'message':'non-company users are not allowed to access this page'})

    @swagger_auto_schema(method='put', request_body=MealOrderSerializer())
    @action(methods=['PUT'], detail=True)
    def put(self, request, format=None):
        """update a meal  for that day only. if there is no meal list for the day, an error message will be returned"""

        order = ComUserChoice.objects.get(day_num=day_num, month=month, year=year, user=request.data.id)
        if order:            
            serializer = MealOrderSerializer2(order, data=request.data, partial=True)
            
            if serializer.is_valid():
                try:
                    vendor = VendorMeal.objects.get(meal=serializer.validated_data['meal_order'], day_num=day_num, month=month)
                    if vendor:
                        serializer.save()
                        
                        data = {
                            "message":"success"
                        }

                        return Response(data, status = status.HTTP_200_OK)
                except VendorMeal.DoesNotExist:
                    raise NotFound(detail={'message': 'meal item with id is not available'})

            else:
                data = {
                    "message":"failed",
                    "error":serializer.errors
                }
            
                return Response(data, status = status.HTTP_400_BAD_REQUEST)
        else:
            raise NotFound(detail={'message': 'There is no meal order made for today by user'})

    def delete(self, request, format=None):

        """Deletes the meal order made for that day by a user.
           It is only accessible to admin users and non-admin users.
        """
        
        obj = ComUserChoice.objects.filter(day_num=day_num, month=month, year=year, user=request.user.id)
        if obj:      
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise NotFound(detail={'message': 'There is no meal order made by this user for today. Try again later.'})

@swagger_auto_schema(method="get")
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsVendor])
def get_all_order(request):
    """This method retrieve all orders made for today's meal list"""
    if request.method == "GET":
        order_list = ComUserChoice.objects.filter(day_num=day_num, month=month, year=year)
        if order_list:
            serializer = MealOrderSerializer3(order_list, many=True)

            data = {
                'message': 'success',
                'count': order_list.count(),
                'order date': f'{day_num}-{month}-{year}',
                'data': serializer.data
            }
                
            return Response(data, status = status.HTTP_200_OK) 
        
        else:
            return Response(data={"message": "There is no order made for today's meal"}, status=status.HTTP_400_BAD_REQUEST)

class VendorListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendor]

    def get(self, request, format=None):
        """This method retrieves the  list of meal items for that day posted by the vendor.
            It is only accessible to admin and vendor users.
        """

        try:
            vendor_list = VendorMeal.objects.filter(day_num=day_num, month=month, year=year)
            serializer = VendorSerializer2(vendor_list, many=True)

            data = {
                'message': 'success',
                'meal-date': f'{day_num}-{month}-{year}',
                'data': serializer.data
            }
            
            return Response(data, status = status.HTTP_200_OK)        
            
        except MealList.DoesNotExist:
            raise NotFound(detail={'message': 'There is no meal list made for today. Try again later.'})

    @swagger_auto_schema(method='post', request_body=VendorSerializer2())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):

        """This method creates a meal instance for that day by the vendor.
            It is only accessible to admin and vendor users.
        """
        data = {}
        data['image'] = request.data['image']
        data['meal'] = request.data['meal']
        data['price'] = request.data['price']
        data['day'] = day
        data['day_num'] = day_num
        data['month'] = month
        data['year'] = year

        obj = VendorSerializer(data=data)
        if obj.is_valid():
            obj.save()

            data = {
                'message': 'Success'
            }

            return Response(data, status=status.HTTP_200_OK)

        else:

            data = {
                'message': 'failed to create',
                'error': obj.errors
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class VendorListEdit(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendor]

    @swagger_auto_schema(method='put', request_body=VendorSerializer2())
    @action(methods=['PUT'], detail=True)
    def put(self, request, item_id, format=None):

        """This method update a meal instance for that day by the vendor.
            It is only accessible to admin and vendor users.
        """

        try:
            vendor = VendorMeal.objects.get(id=item_id, day_num=day_num, month=month, year=year)
            obj = VendorSerializer(vendor, data=request.data, partial=True)
            if obj.is_valid():
                obj.save()

                data = {
                    'message': 'Success'
                }

                return Response(data, status=status.HTTP_200_OK)

            else:

                data = {
                    'message': 'failed to create',
                    'error': obj.errors
                }

                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except VendorMeal.DoesNotExist:
            raise NotFound(detail={'message': 'there is no vendor item with given id'})

    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)
    def delete(self, request, item_id, format=None):

        """Deletes a single vendor meal list made for that day.
           It is only accessible to admin users and vendors.
        """
        try:
            obj = VendorMeal.objects.get(id=item_id, day_num=day_num, month=month, year=year)
            if obj:      
                obj.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            raise NotFound(detail={'message': 'There is no vendor item with given id'})

class UserMonthlyHistoryAdmin(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get(self, request, user_id, month, year, format=None):
        """This method retrieve a single user order made for the provide year and month meal list. only accessible by the admin"""

        order_list = ComUserChoice.objects.filter(month=month.capitalize(), year=year, user=user_id)

        if order_list:
            serializer = MealOrderSerializer4(order_list, many=True)

            data = {
                'message': 'success',
                'order_count': order_list.count(),
                'order month': f'{month.capitalize()}-{year}',
                'data': serializer.data
            }
                
            return Response(data, status = status.HTTP_200_OK) 
        
        else:
            return Response(data={"message": "There is no order made by this user for the month provided"}, status=status.HTTP_400_BAD_REQUEST)

class UserMonthlyHistory(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]
    
    def get(self, request, month, year, format=None):
        """This method retrieve a single logged in user order made for the provided year and month meal list"""

        order_list = ComUserChoice.objects.filter(month=month.capitalize(), year=year, user=request.user.id)

        if order_list:
            serializer = MealOrderSerializer4(order_list, many=True)

            data = {
                'message': 'success',
                'order_count': order_list.count(),
                'order month': f'{month.capitalize()}-{year}',
                'data': serializer.data
            }
                
            return Response(data, status = status.HTTP_200_OK) 
        
        else:
            return Response(data={"message": "There is no order made by this user for the month provided"}, status=status.HTTP_400_BAD_REQUEST)
