
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Max, Min, Sum
from .models import Autor, Libro

'''
AGGREGATE-> ¿cuantas pags tienen todos los libros juntos? en java hacemos un bucle y guardamos numPag en variable
pero en djangos hacemos:
resultado= Libro.objects.aggregate(total=sum('num_paginas'))
te da -> {'total': 1500}

también está avg, max, min, count
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

ANNOTATE-> ¿cuántas páginas ha escrito cada autor en su vida? hariamos bucle también en java
quiero muchos resultados. Uno para Osamu, otro para Haruki

autores= Autor.object.annotate(total_paginas=Sum('libro_num_paginas')

*ten en cuenta que en libro tengo una fk que es autor. Asi que django crea de forma automática en Autor un
"libro_set" (si, django crea tmb la relacioń inversa)

Cada guión bajo significa "entra dentro de". Así que: 
entra en libro>entra en num_paginas
libro_num_paginas > django sabe que estoy accediendo a AUTOR > SU RELACION CON CADA LIBRO> ATRIBUTO DE LIBRO NUM_PAGINAS
Se puede hacer del reves, si. Django lo entiende.
'''
# PÁGINA PRINCIPAL y ANNOTATE
def funcion_principal(request):
    context = Autor.objects.annotate(
        total_libros=Count('libro')
    )

    return render(request, 'autores_clasicos/base.html', {
        'autores': context
    })


# DETALLE DE UN AUTOR
def detalle_autor(request, id):
    autor_actual = get_object_or_404(Autor, id=id)

    return render(request, 'autores_clasicos/detalle.html', {
        'autor': autor_actual
    })


# DESCRIPCIÓN
def descripcion_web(request):
    return render(request, 'autores_clasicos/descripcion.html')


# CONTACTO
def contacto_empresa(request):
    return render(request, 'autores_clasicos/contacto.html')


# LIBROS DE UN AUTOR
def libros_autor(request, id):
    libros = Libro.objects.filter(autor=id)

    return render(request, 'autores_clasicos/todos_libros.html', {
        'libros': libros
    })


# ESTADÍSTICAS GENERALES + AGGREGATE
def estadisticas(request):
    datos = Libro.objects.aggregate(
        total_libros=Count('id'),
        media_paginas=Avg('num_paginas'),
        maximo_paginas=Max('num_paginas'),
        minimo_paginas=Min('num_paginas'),
        suma_paginas=Sum('num_paginas')
    )

    return render(request, 'autores_clasicos/estadisticas.html', {
        'datos': datos
    })
