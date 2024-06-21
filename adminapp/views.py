from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User, Customer,UserToken,CustomerToken
from .serializers import UserSerializer,CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from .authentication import CustomTokenAuthentication

class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
        user = User.objects.get(id=data.id)
        token, created = UserToken.objects.get_or_create(user=user)
        return Response({'token': token.key})

class CreateCustomer(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            customer = Customer.objects.get(id= data.id)
            token, created = CustomerToken.objects.get_or_create(user=customer)
            return Response({'token': token.key})
        else:
            return Response({'success':False,'error':serializer.errors})

class CustomerGet(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if isinstance(user, Customer):
            if not user.has_perm('adminapp.view_customer'):
                return Response({'success': False, 'message': 'Permission denied customer'}, status=403)
        elif isinstance(user, User):
            if not user.has_perm('adminapp.view_customer'):
                return Response({'success': False, 'message': 'Permission denied user'}, status=403)
        return Response({'success': True, 'message': 'Hello Customer'})