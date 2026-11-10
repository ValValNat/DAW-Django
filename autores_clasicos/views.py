from django.shortcuts import render, get_object_or_404
from .models import Autor, Libro




def funcion_principal(request):
    context = Autor.objects.all()

    return render(request, 'autores_clasicos/base.html', {'autores': context})

def detalle_autor(request, id):
    autor_actual= get_object_or_404(Autor, id=id)
    
    return render(request, 'autores_clasicos/detalle.html', {'autor': autor_actual})

def descripcion_web(request):
    return render(request, 'autores_clasicos/descripcion.html')

def contacto_empresa(request):
    return render(request, 'autores_clasicos/contacto.html')

def libros_autor(request, id):
    libros= Libro.objects.filter(autor=id)
    return render(request, 'autores_clasicos/todos_libros.html', {'libros': libros})