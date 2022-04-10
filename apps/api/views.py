import http

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers import UserListSerializer
from apps.api.models import User


class UserList(APIView, LimitOffsetPagination):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request):
        if request.user.position == None:
            results = self.paginate_queryset(self.queryset, request)
            serializer = UserListSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        user_information = get_object_or_404(User, id=request.user.id)
        serializer = UserListSerializer(user_information)
        return Response(serializer.data)


class UserListWithSameLevel(APIView, LimitOffsetPagination):
    def get(self, request, pk):
        if request.user.position == None:
            results = self.paginate_queryset(list(User.objects.filter(position=pk)), request)
            serializer = UserListSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(status=http.HTTPStatus.NOT_ACCEPTABLE)
