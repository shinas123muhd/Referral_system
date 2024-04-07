from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,ReferralSerializer
from .models import User,Referral
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
# Create your views here.

class RegisterUser(APIView):
    def post(self,request,format=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                
                code = request.data.get('reffered_by')
                
                if code:
                    referred_by_user = User.objects.get(referral_code = code)
                    
                    user = serializer.save(reffered_by = referred_by_user)
                    Referral.objects.create(referring_user=referred_by_user, referred_user=user)
                    referred_by_user.points += 1
                    referred_by_user.save()
                else:
                    user = serializer.save()
            return Response({'user_id':user.id,'message':'User Registered Successfully'}, status=status.HTTP_201_CREATED)
        
        except User.DoesNotExist:
            return Response({'message': 'Referring user not found'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserDetails(APIView):
    def get(self,request,id,format=None):
        try:
            user = User.objects.filter(id=id)
            print(user)
            serializer = UserSerializer(user,many=True)
            return Response(serializer.data)
        except:
            return Response({'message':'No User'})
        
class CustomPagination(PageNumberPagination):
    page_size = 20  
    page_size_query_param = 'page_size'
    max_page_size = 100

class ViewReferrals(APIView):
    pagination_class = CustomPagination
    def get(self,request,id,format=None):
        current_user = User.objects.get(id = id)
        reffered_users = Referral.objects.filter(referring_user = current_user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(reffered_users, request)
        serializer = ReferralSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

