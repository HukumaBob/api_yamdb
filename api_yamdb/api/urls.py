from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet,
                    get_confirmation_code, get_token)
app_name = 'api'
# router_v1 = routers.DefaultRouter()
# router_v1.register('users', UserViewSet)
# urlpatterns = [
#    path('', include(router_v1.urls)),
#    path('auth/signup/', get_confirmation_code, name='get_code'),
#    path('auth/token/', get_token, name='get_token'),
#    ]

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, 'categories')
v1_router.register('genres', GenreViewSet, 'genres')
v1_router.register('genres', TitleViewSet, 'titles')
v1_router.register('users', UserViewSet)
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('auth/signup/', get_confirmation_code, name='get_code'),
    path('auth/token/', get_token, name='get_token'),
]
