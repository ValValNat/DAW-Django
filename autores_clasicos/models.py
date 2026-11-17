from django.db import models

# Create your models here.

class Edificio(models.Model):
    class Ciudad(models.TextChoices):
        SEVILLA = 'SE', 'Sevilla',
        MADRID = 'MA', 'Madrid'
        BARCELONA = 'BA', 'Barcelona'
        MURCIA = 'MU', 'Murcia'
        BIELEFELD = 'BI', 'Bielefeld'

    nombre= models.CharField(max_length=200)
    ciudad=models.CharField(max_length=3, choices=Ciudad.choices)


class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    numeroObras = models.PositiveIntegerField()
    fechaNacimiento = models.DateField()
    funado = models.BooleanField()

    #le añado el campo imagen, imagefield porque es imagen. el upload to crea una carpeta llamada autores dentro de media.
    #con blank y null en true permite que el autor no tenga foto de antes
    '''
    ImageField guarda la referencia a la imagen, .url obtiene su dirección web y HTML utiliza esa dirección para mostrarla.
    '''
    imagen = models.ImageField(
        upload_to='autores/',
        blank=True,
        null=True
    )
def __str__(self):
    return f'{self.nombre}, {self.numeroObras}, {self.fechaNacimiento}, {self.funado}'


class Editorial(models.Model):
    nombre=models.CharField(max_length=200)
    edificio=models.ManyToManyField(
        Edificio,
        blank=True,
        null=True
    )


class Libro(models.Model):
    nombre= models.CharField(max_length=200)
    genero= models.CharField(max_length=200)
    num_paginas= models.PositiveBigIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editorial= models.ForeignKey(Editorial, on_delete=models.PROTECT, blank=True, null=True)

    '''
    ForeignKey(on_delete=models.PROTECT) -> no se borra si se borra el relacionado
    CASCADE -> se borran los hijitos
    -------------
    Relaciones:
    -Uno a muchos se hace sin poner nada, con fk normal
        autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
        Lo pongo en LIBRO y asi digo un LIBRO puede tener un autor
        pero un autor muchos libros
    -el many to many tenemos que decir a django que cree una tabla intermedia
    autores= models.ManyToManyField(Autor, related_name="hola", blank=True)
    (debes mirar en bbdd en qué entidad concreta se crea el campo cuando es m:n), las normas de formalización
    La tabla intermedia puede tener un atributo extra o varios (relacion aula- personasClase tiene olor)->
    Pues añades un nuevo parametro despues de Autor, que es through="nombreClase"->
     esa clase que he creado tiene fk de cada una de las otras dos tablas
     + el resto de atributos que me den la gana
     -onetoonefield es uno a uno
     models.OneToOneField(...)


     -> agregar haces libro.autores.add(autor)
--------
related_name: sirve para personalizar el acceso inverso a una relación. SUSTITUYE AL _set      .all()
__ : sirve para consultas: Libro.objects.filter(edificio__nombre='Torre del Oro')
     y coge y atraviesa todo


__ (doble guion bajo): sirve para navegar por relaciones en consultas (filter, annotate, aggregate, etc.).



USAR SELECT_RELATED() y prefetch_related()
HAGO UN JOIN CREO O ALGO ASI
Y PREFETCH RELATED
    '''
