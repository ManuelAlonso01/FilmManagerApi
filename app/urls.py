from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Este endpoint hace como de "logueo"
    path('token/', TokenObtainPairView.as_view(), name='token'),
    # Este sirve para obtener un nuevo access token cuando el anterior expire
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("movie-list/", views.movie_list, name='movie-list'),
    path("resumen/", views.resumen, name='resumen'),
    path('subir/', views.subir_pelicula, name='subir'),
    path('register/', views.register_api, name="register"),
    path('movie-edit/<int:id>/', views.editar_pelicula, name='movie-edit'),
]