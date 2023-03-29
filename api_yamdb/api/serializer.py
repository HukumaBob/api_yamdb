from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )