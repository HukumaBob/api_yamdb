from django.db.models import Avg
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from rest_framework import filters, status, viewsets
from django_filters.rest_framework import (DjangoFilterBackend, FilterSet,
                                           CharFilter)
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Comment, Genre, Review, Title, User
from .permissions import IsAdminRole, IsAdminOrReadOnly
from .serializer import (UserSerializer, SignUpSerializer, TokenSerializer,
                         GenreSerializer, CategorySerializer,
                         TitleGetSerializer, TitlePostSerializer)
from rest_framework.response import Response
from api_yamdb.settings import EMAIL_ADMIN
import uuid


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminRole]
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def change_me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


def confirmation_code_to_email(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    subject = 'YAMDb registration'
    message = f'You confirmation code {user.confirmation_code}'
    send_mail(
        subject,
        message,
        EMAIL_ADMIN,
        [user.email],
    )
    user.save()


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    username = request.data.get('username')
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['username'] != 'me':
            serializer.save()
            confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            'Wrong username', status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializer(
        user, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['email'] == user.email:
        serializer.save()
        confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Wrong email address', status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if user.confirmation_code == confirmation_code:
        token = RefreshToken.for_user(user)
        token_data = {'token': str(token.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(
        'Wrong confirmation code', status=status.HTTP_400_BAD_REQUEST
    )


class CommonCreateListDestroyViewset(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(CommonCreateListDestroyViewset):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly, ]
    search_fields = ['=name', ]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    # http_method_names = ['get', 'post', 'path', 'delete']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [TitlePostSerializer]
        return [TitleGetSerializer]


class CategoryViewSet(CommonCreateListDestroyViewset):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    search_fields = ['=name', ]
    lookup_field = 'slug'
