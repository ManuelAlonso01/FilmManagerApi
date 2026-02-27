from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Movies(models.Model):
    user = models.ForeignKey(
        User,
        # Si se borra el usuario, todas sus peliculas se borran
        on_delete=models.CASCADE,
        related_name="movies"
    )
    title = models.CharField(max_length=100)
    poster = models.CharField(max_length=300)
    duration_minutes = models.IntegerField()
    descripcion = models.CharField(max_length=500)
    calificacion = models.IntegerField()
    
    def __str__(self):
        return self.title