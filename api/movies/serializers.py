from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Movies, UserFeedback


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    avg_rating = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField()
    
    def to_representation(self, instance):
        ret = super(MovieSerializer, self).to_representation(instance)
        try:
            ret['avg_rating'] = round(instance['avg_rating'], 1)
        except:
            pass
        return ret

    class Meta:
        model = Movies
        fields = ('id', 'name', 'year', 'count', 'avg_rating')
        validators = [
            UniqueTogetherValidator(
                queryset=Movies.objects.all(),
                fields=['name', 'year']
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserFeedbackSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = UserFeedback
        fields = ('movie', 'rating', 'comment', 'created_by')


class MovieDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    avg_rating = serializers.FloatField(read_only=True)
    count = serializers.IntegerField(read_only=True)
    feedback = UserFeedbackSerializer(source='movies_feedback', many=True)

    def to_representation(self, instance):
        ret = super(MovieDetailSerializer,self).to_representation(instance)
        try:
            ret['avg_rating'] = round(instance.avg_rating, 1)
        except:
            pass
        return ret

    class Meta:
        model = Movies
        fields = ('id', 'name', 'year', 'count', 'avg_rating', 'feedback')
