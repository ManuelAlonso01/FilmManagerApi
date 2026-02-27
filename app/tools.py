from .models import Movies
from django.db.models import Sum, Avg

def minutos_a_tiempo(minutos):
    dias = minutos // 1440
    horas = (minutos % 1440) // 60
    minutos_restantes = minutos % 60

    partes = []

    if dias > 0:
        partes.append(f"{dias} día" if dias == 1 else f"{dias} días")

    if horas > 0:
        partes.append(f"{horas} hora" if horas == 1 else f"{horas} horas")

    if minutos_restantes > 0:
        partes.append(
            f"{minutos_restantes} minuto"
            if minutos_restantes == 1
            else f"{minutos_restantes} minutos"
        )

    if not partes:
        return "0 minutos"

    if len(partes) == 1:
        return partes[0]

    if len(partes) == 2:
        return f"{partes[0]} y {partes[1]}"

    return f"{', '.join(partes[:-1])} y {partes[-1]}"
    

from django.db.models import Sum, Avg

def generar_resumen(request):
    qs = Movies.objects.filter(user=request.user)

    peliculas_vistas = qs.count()

    tiempo_invertido = qs.aggregate(
        total=Sum("duration_minutes")
    )["total"] or 0

    nota_media = qs.aggregate(
        avg=Avg("calificacion")
    )["avg"] or 0

    pelicula_mas_larga = qs.order_by("-duration_minutes").first()
    pelicula_mas_corta = qs.order_by("duration_minutes").first()

    top_mejores = qs.order_by("-calificacion")[:3]
    top_peores = qs.order_by("calificacion")[:3]

    data = {
        "peliculas_vistas": peliculas_vistas,
        "tiempo_invertido": minutos_a_tiempo(tiempo_invertido),
        "nota_media": round(nota_media, 2) if nota_media is not None else None,
        "pelicula_mas_larga": (
            f"{pelicula_mas_larga.title}, "
            f"{minutos_a_tiempo(pelicula_mas_larga.duration_minutes)}"
            if pelicula_mas_larga else 0
        ),
        "pelicula_mas_corta": (
            f"{pelicula_mas_corta.title}, "
            f"{minutos_a_tiempo(pelicula_mas_corta.duration_minutes)}"
            if pelicula_mas_corta else 0
        ),
        "top_mejores": ', '.join([m.title for m in top_mejores]),
        "top_peores": ', '.join([m.title for m in top_peores]),
    }

    return data