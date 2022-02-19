from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.utils import json

from .models import User, FriendRequest
from .serializers import RegisterSerializer, EditUserSerializer, FriendRequestSerializer, AccRejRequestSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def apiOverview(request):
    api_urls = {
        'register': '/register/',
        'login': '/login/',
        'logout': '/logout/',
        'accdelete': '/accdelete/',
        'edituser': '/edituser/',
        'sendrequest': '/sendrequest/<int:id>/',
        'AccepetRejectRequest': '/AccepetRejectRequest/',
    }
    return Response(api_urls)


@api_view(["POST"])
@permission_classes([AllowAny])
def Register_Users(request):
    try:
        data = {}
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "user has registered successfully"
            data["username"] = account.username
            data["token"] = token

        else:
            data = serializer.errors

        return Response(data)
    except IntegrityError as e:
        account = User.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})

    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Edit_User(request):
    user = User.objects.get(id=request.user.id)
    serializer = EditUserSerializer(data=request.data)
    prevname = user.user_full_name
    if serializer.is_valid():
        name = serializer.data['user_full_name']
        user.user_full_name = name
        user.save()
        return Response({'response': 'User fullname updated. previous name is '+prevname+' updated name is '+name})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    data = {}
    print(type(request.body))
    reqBody = json.loads(request.body)
    username = reqBody['username']
    print(username)
    password = reqBody['password']
    try:
        Account = User.objects.get(username=username)
    except BaseException as e:
        raise ValidationError({"400": f'{str(e)}'})

    token = Token.objects.get_or_create(user=Account)[0].key
    print(token)
    if not check_password(password, Account.password):
        raise ValidationError({"message": "Incorrect Login credentials"})

    if Account:
        if Account.is_active:
            print(request.user)
            login(request, Account)
            data["username"] = Account.username
            Res = {"data": data, "token": token}

            return Response(Res)

        else:
            raise ValidationError({"400": f'Account not active'})

    else:
        raise ValidationError({"400": f'Account doesnt exist'})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Acc_delete(request):
    request.user.delete()
    logout(request)
    return Response('User Account Deleted')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userincomingrequest(request):
    frndreq = FriendRequest.objects.filter(receiver=request.user)
    serializer = FriendRequestSerializer(frndreq, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def useroutgoingrequest(request):
    frndreq = FriendRequest.objects.filter(sender=request.user)
    serializer = FriendRequestSerializer(frndreq, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendrequest(request, id):
    user_obj = User.objects.get(id=id)
    frndreq = FriendRequest.objects.create(sender=request.user,receiver=user_obj,status="pending")
    frndreq.save()
    return Response("friend request is send to "+user_obj.username)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AccepetRejectRequest(request):
    serializer = AccRejRequestSerializer(data=request.data)
    if serializer.is_valid():
        requestid = serializer.data['requestid']
        requeststatus = serializer.data['requeststatus']
        frndreq = FriendRequest.objects.get(id=requestid)
        frndreq.status = requeststatus
        frndreq.save()
        print()
        return Response({'response': 'friend request ' + str(requestid) + ' is '+ str(requeststatus)})