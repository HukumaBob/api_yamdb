from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet,
                    get_confirmation_code, get_token)
app_name = 'api'
router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', get_confirmation_code, name='get_code'),
    path('auth/token/', get_token, name='get_token'),
]
