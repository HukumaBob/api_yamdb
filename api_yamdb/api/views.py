from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User
from .helpers import confirmation_code_to_email
from .mixins import CommonCreateListDestroyViewset
from .permissions import (IsAdminOrStuffPermission, IsAuthorOrModerator,
                          IsAdminOrReadOnly, IsAdminRole, ReadOnly)
from .serializer import (UserSerializer, SignUpSerializer, TokenSerializer,
                         ReviewSerializer, CommentSerializer, GenreSerializer,
                         CategorySerializer, TitleSerializer,
                         TitleCreateSerializer, UserWithoutRoleSerializer)
from rest_framework.response import Response

from .filters import TitleFilter


# UserViewSet
# This viewset handles operations related to User model, including CRUD operations and 'me' endpoint.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrStuffPermission]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def change_me(self, request):
        if request.method == 'PATCH':
            # Serialize the request user with UserWithoutRoleSerializer
            serializer = UserWithoutRoleSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    # Serialize the request data with SignUpSerializer
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    email = serializer.data.get('email')
    user, created = User.objects.get_or_create(
        username=username,
        email=email
    )
    confirmation_code_to_email(username)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    # Serialize the request data with TokenSerializer
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if user.confirmation_code == confirmation_code:
        # Generate a token using RefreshToken for the user
        token = RefreshToken.for_user(user)
        token_data = {'token': str(token.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(
        'Wrong confirmation code', status=status.HTTP_400_BAD_REQUEST
    )


# CommentViewSet
# This viewset handles operations related to Comment model, including CRUD operations.
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


# ReviewViewSet
# This viewset handles operations related to Review model, including CRUD operations.
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


# TitleViewSet
# This viewset handles operations related to Title model, including CRUD operations.
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminRole | ReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


# CategoryViewSet
# This viewset handles operations related to Category model, including CRUD operations.
class CategoryViewSet(CommonCreateListDestroyViewset):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly, ]
    search_fields = ['=name', ]
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination


# GenreViewSet
# This viewset handles operations related to Genre model, including CRUD operations.
class GenreViewSet(CommonCreateListDestroyViewset):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ['=name', ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = LimitOffsetPagination
