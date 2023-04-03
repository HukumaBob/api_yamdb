from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Incorrect username')
        return username


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(source='reviews__score__avg',
                                    read_only=True)

    class Meta:
        fields = ['id', 'name', 'genre', 'year',
                  'description', 'rating', 'category']
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         many=True,
                                         queryset=Genre.objects.all(),
                                         )
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all(),
                                            )

    class Meta:
        fields = '__all__'
        model = Title
