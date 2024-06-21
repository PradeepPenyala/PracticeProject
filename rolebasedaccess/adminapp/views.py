from django.shortcuts import render
import json
from django.http import Http404, JsonResponse, HttpResponse,FileResponse
from rest_framework.views import APIView
# Create your views here.
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from .serializers import GroupSerializer,PermissionSerializer
from adminapp.models import Faqs,User,Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from adminapp.custom_throttling import BurstRateThrottle
from rest_framework.throttling import ScopedRateThrottle

class GroupCreteApi(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        name = request.data.get('name')

        group_ins = Group.objects.create(name = name)
        return JsonResponse({'success':True,'message':'group creataed successfully'})

class AllGetGroup(APIView):
    def get(self, request):
        data = Group.objects.all().order_by('-id')
        # serializer = GroupSerializer(data, many=True)
        permissions = data.permissions.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return JsonResponse({'success':True,'data':serializer.data})

class UpdateGroupName(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        group_id = request.data.get('group_id')
        name = request.data.get('name')
        try:
            grp_ins = Group.objects.get(id = group_id)

        except:
            return JsonResponse({'success':False})
        grp_ins.name = name
        grp_ins.save(update_fields=['name'])
        return JsonResponse({'success':True,'data':'updated successfully'})

class DeleteGroupName(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request):
        group_id = request.data.get('group_id')
        try:
            grp_ins = Group.objects.get(id = group_id).delete()
            return JsonResponse({'success':True,'message':'deleted successfully'})
        except:
            return JsonResponse({'success':False})

class AllGetPermissions(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return JsonResponse({'success':True,'data':serializer.data})


class AddPermissionsToRole(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        group_id = request.data.get('group_id')
        permission_ids = request.data.get('permission_ids')
        try:
            grp_ins = Group.objects.get(id=group_id)
        except:
            return JsonResponse({'success':False})
        for i in permission_ids:
            permissions = Permission.objects.get(id= i)
            grp_ins.permissions.add(permissions)

        return JsonResponse({'success':True})

class UpdatePermissionsToRole(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        group_id = request.data.get('group_id')
        permission_ids = request.data.get('permission_ids')
        try:
            grp_ins = Group.objects.get(id=group_id)
        except:
            return JsonResponse({'success':False})
        grp_ins.permissions.clear()
        permissions_to_add = Permission.objects.filter(id__in=permission_ids)
        grp_ins.permissions.add(*permissions_to_add)

        return JsonResponse({'success':True})


class FaqsCreateApi(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        if not request.user.has_perm('adminapp.add_faqs'):
            # If user doesn't have permission, return Forbidden response
            return JsonResponse({'error': 'You do not have permission to access this resource.'})

        question = request.data.get('question')
        answer = request.data.get('answer')
        faq_ins = Faqs.objects.create(question=question,answer=answer)
        return JsonResponse({'success':True})

class AllGetFaqs(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        if not request.user.has_perm('adminapp.view_faqs'):
            # If user doesn't have permission, return Forbidden response
            return JsonResponse({'error': 'You do not have permission to access this resource.'})

        data = list(Faqs.objects.all().values())
        return JsonResponse({'success':True,'data':data})


class AddingGroupToUser(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        print(user_id,'dddddd')
        try:
            user_ins = User.objects.get(id = user_id)
        except:
            return JsonResponse({'success':False,'message':'usrr not found'})
        try:
            grp_ins = Group.objects.get(id = group_id)
        except:
            return JsonResponse({"success":False,'message':'grp not found'})

        user_ins.groups.add(grp_ins)
        user_ins.save()
        return JsonResponse({'success':True,'message':'group added to user'})
class AllgetUser(APIView):
    def get(self, request):
        task = list(User.objects.all().values())
        return JsonResponse({'success':True,'data':task})

class ProductGet(APIView):
    permission_classes = [IsAuthenticated]
    
    throttle_classes = [BurstRateThrottle, ScopedRateThrottle]
    throttle_scope = 'burst'
    def get(self, request):
        data = Product.objects.active()
        # print(type(data))
        return JsonResponse({'success':True,'data':data})