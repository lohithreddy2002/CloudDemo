from ast import Is
import json
import re
from tkinter.tix import STATUS
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MediaStorage
import os
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

class UserAvatarUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    def get(self,request):
        print(request.data)
        media_storage = MediaStorage()
        a = media_storage.bucket.objects.filter(Prefix="user_upload_files/{username}")
        files = []
        for i in a:
            files.append(i)
        return JsonResponse(
            {
                "status":"Success",
                "message":files
            },status = 200
        )

    def post(self, request):
        media_storage = MediaStorage()
        print(request.data)

        try:
            token = request.GET.get("authToken")
        except:
            return
        user = User.objects.filter(auth_token=token)
        try:
            username = user[0].username
        except:
            return JsonResponse(
            {
                "status":"Success",
                "message":"fat"
            },status = 400
        )
        file_obj = request.data.get("test")
        file_name = request.data.get("name")
        file_directory_within_bucket = 'user_upload_files/{username}'.format(username=username)
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_name
        )
        if not media_storage.exists(file_path_within_bucket):
            media_storage.save(file_path_within_bucket, file_obj)
            file_url = media_storage.url(file_path_within_bucket)
            
            return JsonResponse({
                'status': 'Success',
                'message': file_url,
            },status=200)
        else:
            return JsonResponse({
                "status":"Failed",
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)   



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        muser = User.objects.get(username=username)
    except:
        muser = None
    if not muser:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=muser)
    return Response({'token': token.key,
    "status":"Success"},
                    status=HTTP_200_OK) 

import datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_file(request):
    try:
        token = request.GET.get("authToken")
    except:
        return JsonResponse(
            {
                "message":"Failed",
                "data":"Auth Token not passed"
            },status = 400
        )
    user = User.objects.filter(auth_token=token)
    try:
        username = user[0].username
    except:
        return JsonResponse(
            {
                "message":"Success",
                "data":"No Matching user Found"
            },status = 400
        )
    media_storage = MediaStorage()
    a = media_storage.bucket.objects.filter(Prefix='user_upload_files/{username}'.format(username=username))
    files = []
    for i in a:
        data = i.get()
        files.append({
           "last modified":data["LastModified"],
           "content-type":data["ContentType"],
           "url":media_storage.url(i.key),
           "file name":i.key
        })
    return JsonResponse(
            {
                "status":"Success",
                "data":files
            },status = 200
        )






@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = User(username=username,password = password)
    if User.objects.filter(username = username).count != 0:
        return Response({'error': "username already exists"},
                        status=HTTP_400_BAD_REQUEST)
    user.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "status":"Success",
        'token': token.key},
                    status=HTTP_200_OK) 




from rest_framework import viewsets
from .models import userSerializers
from django.contrib.auth.models import User
 
 
class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers

