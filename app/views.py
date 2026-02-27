from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from .models import Movies
from .serializers import MovieSerializer

@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movies)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=200)
    
