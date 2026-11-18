
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Max, Min, Sum
from .models import Autor, Libro, Editorial, Edificio

'''
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AGGREGATE->DA DICCIONARIO ¿cuantas pags tienen todos los libros juntos? en java hacemos un bucle y guardamos numPag en variable
pero en djangos hacemos:
resultado= Libro.objects.aggregate(total=sum('num_paginas'))
te da -> {'total': 1500}

también está avg, max, min, count

----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

ANNOTATE->DA QUERYSET ¿cuántas páginas ha escrito cada autor en su vida? hariamos bucle también en java
quiero muchos resultados. Uno para Osamu, otro para Haruki

autores= Autor.object.annotate(total_paginas=Sum('libro_num_paginas')


---------------------------------------------------------------------
*ten en cuenta que en libro tengo una fk que es autor. Asi que django crea de forma automática en Autor un
"libro_set" (si, django crea tmb la relacioń inversa)

Cada guión bajo significa "entra dentro de". Así que: 
entra en libro>entra en num_paginas
libro_num_paginas > django sabe que estoy accediendo a AUTOR > SU RELACION CON CADA LIBRO> ATRIBUTO DE LIBRO NUM_PAGINAS
Se puede hacer del reves, si. Django lo entiende.

con related_name consulto objetos relacionados en forma inversa
si en Libro tengo la col de Autor como fk y le pongo el parametro de related_name:
class Libro(models.Model):
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='mariquita'
    )
yo puedo hacer
autor.mariquita.all()



----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
condiciones or con q
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
con related_name consulto objetos relacionados en forma inversa
si en Libro tengo la col de Autor como fk y le pongo el parametro de related_name:
class Libro(models.Model):
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='mariquita'
    )
     
       yo puedo hacer
autor.mariquita.all()
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
- null=True → permite guardar NULL en la base de datos.
- blank=True → permite dejar el campo vacío en los formularios y validaciones.
'''
# PÁGINA PRINCIPAL y ANNOTATE
def funcion_principal(request):

    # TODOS los autores, con el número de libros
    todos_autores = Autor.objects.annotate(
        total_libros=Count('libro')
    ).prefetch_related('libro_set') #dame en verdad todos-autores = libros agrupados por autor

    # SOLO los autores que NO están funados
    autores_no_funados = Autor.objects.filter( #y ya miro del autor si esta funado o no para guardarlo
        funado=False
    ).annotate(
        total_libros=Count('libro')
    ).prefetch_related('libro_set')

    return render(request, 'autores_clasicos/base.html', {
        'todos_autores': todos_autores,
        'autores_no_funados': autores_no_funados
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

def editorial_libros(request):
    #estoy declarando una relacion, no haciendo una consulta básica
    editoriales = Editorial.objects.annotate(
        num_libros=Count('libro')
    )
    return render(request, 'autores_clasicos/editorial_completa.html', {'editoriales': editoriales})

#MOSTRAR EDIFICIOS

def edificios_todos(request):
    edificios= Edificio.objects.all()
    return render(request, 'autores_clasicos/edificios.html', {'edificios_diccionario': edificios})