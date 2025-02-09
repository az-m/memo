from .models import CompanyDetails, UserDetails, TaskProgress, UserFeedback
from .serializers import CompanyDetailSerializer, UserDetailSerializer, UserTaskSerializer, \
    AllTasksSerializer, UserFeedbackSerializer
import jwt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


# user views


@api_view(['GET', 'PATCH', 'DELETE'])
def get_update_user(request):
    token = get_token_auth_header(request)
    decoded_token = jwt.decode(token, options={"verify_signature": False})

    if decoded_token.get("sub"):
        user_sub = decoded_token["sub"]

        try:
            user_record = UserDetails.objects.get(pk=user_sub)
        except UserDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserDetailSerializer(user_record)
        return Response(serializer.data)

    elif request.method == "PATCH":

        print(request.data)

        if request.data.get("user_xp"):
            request.data["user_xp"] += user_record.user_xp
            request.data["user_level"] += user_record.user_level

        serializer = UserDetailSerializer(user_record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        user_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_user(request):

    serializer = UserDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# company views


@api_view(['GET', 'PATCH'])
def get_update_company(request, cid):

    try:
        company_record = CompanyDetails.objects.get(pk=cid)
    except CompanyDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CompanyDetailSerializer(company_record)
        return Response(serializer.data)

    elif request.method == "PATCH":

        request.data["company_xp"] = request.data["company_xp"] + company_record.company_xp

        serializer = CompanyDetailSerializer(company_record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# task views


@api_view(['GET'])
def get_user_tasks(request):
    token = get_token_auth_header(request)
    decoded_token = jwt.decode(token, options={"verify_signature": False})

    if decoded_token.get("sub"):
        user_sub = decoded_token["sub"]

        try:
            user_record = UserDetails.objects.get(pk=user_sub)
        except UserDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserTaskSerializer(user_record)
    return Response(serializer.data)


@api_view(['POST'])
def add_task(request):
    serializer = AllTasksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
def update_task(request, tid):

    try:
        task_record = TaskProgress.objects.get(pk=tid)
    except TaskProgress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = AllTasksSerializer(task_record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def add_feedback(request):
    serializer = UserFeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_feedback(request, fid):

    try:
        feedback_record = UserFeedback.objects.get(pk=fid)
    except UserFeedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    feedback_record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
