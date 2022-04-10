from django.urls import path

from apps.api.views import UserList, UserListWithSameLevel

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


api_name = 'api'

urlpatterns = [
         path('staff/', UserList.as_view(), name='staff'),
         path('staff/<int:pk>/', UserListWithSameLevel.as_view(), name='staff-with-same-level'),
         path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
         path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
