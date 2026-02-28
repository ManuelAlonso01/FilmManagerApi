# Librerías de Django (Core)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Django REST Framework (Infraestructura de API)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

# JWT (Autenticación moderna)
from rest_framework_simplejwt.tokens import RefreshToken

# Lógica de negocio
from .models import Movies
from .serializers import MovieSerializer, MovieCreateSerializer, MovieEditSerializer
from .tools import generar_resumen




#<---------------------------GET----------------------------->
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # El usuario debe estar logueado
def movie_list(request):
    movies = Movies.objects.filter(user=request.user) # Filtramos las peliculas que subio ese usuario
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # El usuario debe estar logueado
def resumen(request):
    data = generar_resumen(request.user) # Generamos el resumen en base a ese usuario
    
    if not data.get("peliculas_vistas"):
        return Response({"detail": "No hay informacion :("}, status=status.HTTP_404_NOT_FOUND)
        
    return Response(data)



#<---------------------------POST---------------------------->
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subir_pelicula(request):
    serializer = MovieCreateSerializer(data=request.data)

    if serializer.is_valid():
        # Al usar JWT, el usuario viene en el request.user
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@permission_classes([AllowAny]) # Cualquiera puede registrarse
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Usuario y contraseña son requeridos"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "El nombre de usuario ya está en uso"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Creamos el usuario
    user = User.objects.create_user(username=username, password=password)

    # Generamos los tokens manualmente para este nuevo usuario
    refresh = RefreshToken.for_user(user)

    return Response({
        "mensaje": "Usuario creado con éxito",
        "tokens": {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    }, status=status.HTTP_201_CREATED)
    

#<--------------------------PATCH---------------------------->    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editar_pelicula(request, id):
    movie = get_object_or_404(Movies, pk=id, user=request.user)
    serializer = MovieEditSerializer(movie, data=request.data, partial=True) # Partial=True le indica al serializer que
                                                                             # probablemente no van a estar todos los campos,
                                                                             # asi que actualiza los que vengan sin que se rompa.
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    