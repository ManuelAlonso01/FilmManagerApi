from rest_framework import serializers
from .models import Movies


class MovieSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.username')
    
    title = serializers.CharField()
    poster = serializers.CharField()
    duration_minutes = serializers.IntegerField()
    descripcion = serializers.CharField()
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
        
class MovieCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    poster = serializers.CharField()
    duration_minutes = serializers.IntegerField()
    descripcion = serializers.CharField()
    calificacion = serializers.IntegerField()
    
    def validate_title(self, value):
        return value.strip().title()
    
    def validate_descripcion(self, value):
        return value.strip()
    
    def create(self, validated_data):
        # Extraemos el usuario que pasamos desde la vista en serializer.save(user=request.user)
        user = validated_data.pop('user') 
        
        # Usamos los valores reales del diccionario validated_data
        movie = Movies.objects.create(
            user=user,
            title=validated_data['title'],
            poster=validated_data['poster'],
            duration_minutes=validated_data['duration_minutes'],
            descripcion=validated_data['descripcion'],
            calificacion=validated_data['calificacion']
        )
        return movie
    