from rest_framework import serializers
from .models import Movies


class MovieSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.username')
    
    title = serializers.CharField(max_length=100)
    poster = serializers.CharField(max_length=300)
    duration_minutes = serializers.IntegerField()
    descripcion = serializers.CharField(max_length=500)
    calificacion = serializers.IntegerField()
    
    class Meta:
        model = Movies
        fields = [
            "id",
            'user',
            "title",
            "poster",
            "duration_minutes",
            "descripcion",
            "calificacion",
        ]
        
    