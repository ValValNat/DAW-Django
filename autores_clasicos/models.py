from django.db import models

# Create your models here.

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

class Libro(models.Model):
    nombre= models.CharField(max_length=200)
    genero= models.CharField(max_length=200)
    num_paginas= models.PositiveBigIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)