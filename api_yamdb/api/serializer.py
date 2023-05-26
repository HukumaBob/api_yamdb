from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    # Serializer for User model

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class UserWithoutRoleSerializer(serializers.ModelSerializer):
    # Serializer for User model excluding the 'role' field
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class SignUpSerializer(serializers.Serializer):
    # Serializer for user sign up

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        # Custom validation to check if the username or email already exist
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'This user already exists!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    # Serializer for authentication token

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=254)


class CurrentTitleDefault(object):
    # Default value for the 'title' field based on the URL context

    def set_context(self, serializer_field):
        # Set the 'title' object based on the URL context
        title_id = serializer_field.context.get('view').kwargs.get('title_id')
        self.title = get_object_or_404(
            Title,
            id=title_id
        )

    def __call__(self):
        # Return the 'title' object as the default value
        return self.title


class ReviewSerializer(serializers.ModelSerializer):
    # Serializer for Review model

    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='You have already reviewed it!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    # Serializer for Comment model

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    # Serializer for Category model

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    # Serializer for Genre model

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleCreateSerializer(serializers.ModelSerializer):
    # Serializer for creating Title model

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    # Serializer for Title model

    rating = serializers.IntegerField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
