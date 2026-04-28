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


def generar_resumen(user):
    qs = Movies.objects.filter(user=user)

    peliculas_vistas = qs.filter(is_serie=False).count()
    series_vistas = qs.filter(is_serie=True).count()

    tiempo_invertido_total = qs.aggregate(
        total=Sum("duration_minutes")
    )["total"] or 0

    tiempo_invertido_peliculas = qs.filter(is_serie=False).aggregate(
        total=Sum("duration_minutes")
    )["total"] or 0

    tiempo_invertido_series = qs.filter(is_serie=True).aggregate(
        total=Sum("duration_minutes")
    )["total"] or 0

    nota_media_global = qs.aggregate(
        avg=Avg("calificacion")
    )["avg"] or 0

    nota_media_peliculas = qs.filter(is_serie=False).aggregate(
        avg=Avg("calificacion")
    )["avg"] or 0

    nota_media_series = qs.filter(is_serie=True).aggregate(
        avg=Avg("calificacion")
    )["avg"] or 0

    pelicula_mas_larga = qs.filter(is_serie=False).order_by("-duration_minutes").first()
    pelicula_mas_corta = qs.filter(is_serie=False).order_by("duration_minutes").first()

    serie_mas_larga = qs.filter(is_serie=True).order_by("-duration_minutes").first()
    serie_mas_corta = qs.filter(is_serie=True).order_by("duration_minutes").first()

    top_mejores_peliculas = qs.filter(is_serie=False).order_by("-calificacion")[:3]
    top_peores_peliculas = qs.filter(is_serie=False).order_by("calificacion")[:3]

    top_mejores_series = qs.filter(is_serie=True).order_by("-calificacion")[:3]
    top_peores_series = qs.filter(is_serie=True).order_by("calificacion")[:3]

    return {
        "peliculas_vistas": peliculas_vistas,
        "series_vistas": series_vistas,
        "tiempo_invertido_total": minutos_a_tiempo(tiempo_invertido_total),
        "tiempo_invertido_peliculas": minutos_a_tiempo(tiempo_invertido_peliculas),
        "tiempo_invertido_series": minutos_a_tiempo(tiempo_invertido_series),
        "nota_media_global": round(nota_media_global, 1) if nota_media_global else 0,
        "nota_media_peliculas": round(nota_media_peliculas, 1) if nota_media_peliculas else 0,
        "nota_media_series": round(nota_media_series, 1) if nota_media_series else 0,
        "pelicula_mas_larga": {
            "titulo": pelicula_mas_larga.title if pelicula_mas_larga else None,
            "duracion": minutos_a_tiempo(pelicula_mas_larga.duration_minutes) if pelicula_mas_larga else None
        } if pelicula_mas_larga else None,
        "pelicula_mas_corta": {
            "titulo": pelicula_mas_corta.title if pelicula_mas_corta else None,
            "duracion": minutos_a_tiempo(pelicula_mas_corta.duration_minutes) if pelicula_mas_corta else None
        } if pelicula_mas_corta else None,
        "serie_mas_larga": {
            "titulo": serie_mas_larga.title if serie_mas_larga else None,
            "duracion": minutos_a_tiempo(serie_mas_larga.duration_minutes) if serie_mas_larga else None
        } if serie_mas_larga else None,
        "serie_mas_corta": {
            "titulo": serie_mas_corta.title if serie_mas_corta else None,
            "duracion": minutos_a_tiempo(serie_mas_corta.duration_minutes) if serie_mas_corta else None
        } if serie_mas_corta else None,
        "top_mejores_peliculas": [
            {"titulo": movie.title, "calificacion": movie.calificacion}
            for movie in top_mejores_peliculas
        ],
        "top_peores_peliculas": [
            {"titulo": movie.title, "calificacion": movie.calificacion}
            for movie in top_peores_peliculas
        ],
        "top_mejores_series": [
            {"titulo": movie.title, "calificacion": movie.calificacion}
            for movie in top_mejores_series
        ],
        "top_peores_series": [
            {"titulo": movie.title, "calificacion": movie.calificacion}
            for movie in top_peores_series
        ]
    }

    data = {
        
        "peliculas_vistas": peliculas_vistas,
        "series_vistas": series_vistas,
        "tiempo_invertido_total": minutos_a_tiempo(tiempo_invertido_total),
        "tiempo_invertido_peliculas": minutos_a_tiempo(tiempo_invertido_peliculas),
        "tiempo_invertido_series": minutos_a_tiempo(tiempo_invertido_series),
        "nota_media_global": round(nota_media_global, 2) if nota_media_global is not None else None,
        "nota_media_peliculas": round(nota_media_peliculas, 2) if nota_media_peliculas is not None else None,
        "nota_media_series": round(nota_media_series, 2) if nota_media_series is not None else None,
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
        "serie_mas_larga": (
            f"{serie_mas_larga.title}, "
            f"{minutos_a_tiempo(serie_mas_larga.duration_minutes)}"
            if serie_mas_larga else 0
        ),
        "serie_mas_corta": (
            f"{serie_mas_corta.title}, "
            f"{minutos_a_tiempo(serie_mas_corta.duration_minutes)}"
            if serie_mas_corta else 0
        ),
        "top_mejores_peliculas": ', '.join([m.title for m in top_mejores_peliculas]),
        "top_peores_peliculas": ', '.join([m.title for m in top_peores_peliculas]),
        "top_mejores_series": ', '.join([m.title for m in top_mejores_series]),
        "top_peores_series": ', '.join([m.title for m in top_peores_series]),
    }

    return data