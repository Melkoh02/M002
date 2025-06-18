import json

from dj_rest_auth.views import LoginView
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.api.v1.serializers import UserCreateSerializer, UserLoginResponseSerializer, UserDetailSerializer, \
    UpdateProfileSerializer
from users.models import User
from utils.pagination import CustomPageSizePagination


class UserViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def create(self, request, **kwargs):
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.data)

        return Response(UserLoginResponseSerializer(user).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, **kwargs):
        queryset = User.objects.all()

        user_type = request.query_params.get('user_type')

        if user_type:
            queryset = queryset.filter(user_type=user_type)

        paginator = CustomPageSizePagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = UserDetailSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = UserDetailSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=UpdateProfileSerializer, methods=['PATCH'])
    @transaction.atomic
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        if request.method == "PATCH":
            data = request.data
            if str(type(data)) != "<class 'dict'>":  # if not json swagger/postman request
                data = request.data.get("data")
                data = json.loads(data)
            serializer = UpdateProfileSerializer(
                instance=request.user,
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        user_data = UserDetailSerializer(request.user, context={"request": request}).data
        return Response(user_data, status=status.HTTP_200_OK)


class CustomLoginView(LoginView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({"message": "Email o Contraseña incorrecta, intentelo de nuevo"},
                            status=status.HTTP_400_BAD_REQUEST)

        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()

        # Use UserLoginResponseSerializer to format the response
        response_serializer = UserLoginResponseSerializer(instance=user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
