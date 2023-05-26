from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet,
                    get_confirmation_code, get_token)

app_name = 'api'

# Create a router for API endpoints
router_v1 = routers.DefaultRouter()

# Register viewsets for different models
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

# Register nested routes for reviews and comments
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

# Define the URL patterns
urlpatterns = [
    # Include the router-generated URLs
    path('', include(router_v1.urls)),

    # Custom URL patterns for authentication
    path('auth/signup/', get_confirmation_code, name='get_code'),
    path('auth/token/', get_token, name='get_token')
]
