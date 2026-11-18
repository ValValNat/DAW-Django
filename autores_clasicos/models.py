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

    def __str__(self):
        return f"{self.nombre} - {self.get_ciudad_display()}"

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
    def __str__(self):
        return f"{self.nombre}"
        


class Libro(models.Model):
    nombre= models.CharField(max_length=200)
    genero= models.CharField(max_length=200)
    num_paginas= models.PositiveBigIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editorial= models.ForeignKey(Editorial, on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return f"{self.nombre} - {self.autor}"
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

-----------------------------------------------------------------------------------------------
problema n+1 y su solución-> 
dos soluciones:
-select_related() -> uno dos registros
    libros= Libro.objects.select_related("editorial") //es como una consulta JOIN, para este libro ponme los datos de su
    editorial relacionada. Es solo una consulta. Dentro de libro debe existir la col editorial que sea fk, claro

-prefetch_related() -> a veces de cada libro hay un numero indeterminado de editoriales (one to many o many to many)
para cada libro me puede sacar 4 autores, para otro 2... 
asi que usamos prefetch_related() 
asi que para usarlo haces print de libro.autores.all()
------------------------------------------------------------------------------------------------
combinacion de related y prefetch


libros= Libro.objetcs.select_related("editorial").prefetch_related("autores")
es decir: dame para cada libro su editorial y todos sus autores (las dos fk que tiene)

el prefetch te coge todos los datos de la tabla referenciada, puedo especificar la consulta sql 

editoriales= Editorial.objects.prefetch_related(
Prefetch(
"libros"
queryset=Libro.objects.filter(disponible=True).order_by("titulo))
etc etc etc
)

------------------------------------------------------------------------------------------------------
DIFERENCIAS:
SUSTITYYE AL FOR PARA HACER CONSULTAS MAS OPTIMAS
-annotate() -> añadir un cálculo a cada objeto individual(cuántos pasteles tiene cada sucursal)


-aggregate()-> como annotate pero en vez de dar un resultado por cada objeto, da un resultado global (cuántos pasteles
tienen todas las sucursales juntas)


SUSTITYE A AVG, COUNT SUM MAX LO PODRIA HACER EN PYTHON PERO LO HAGO CON SQL
-select_related() -> optimizar consultas cuando hay fk. (VENTAS relaciona SUCURSAL con PASTEL. Puedo coger todas las VENTAS
e i terar en cada venta para ir contando cuántos pastele en total ha vendido cada sucursal
o  hacer un JOIN de dame VENTA donde sucursal sea 'aeropuerto' y donde PASTEL.SABOR sea 'fresa')ç




-prefetch_related() -> 
# 1. Obtenemos todos los empleados de la base de datos.
# prefetch_related("sucursales") le dice a Django que también
# cargue las sucursales relacionadas con cada empleado.
# Así evitamos hacer una consulta por cada empleado al acceder a sus sucursales.

empleados = Empleado.objects.prefetch_related("sucursales")


# 2. Recorremos uno por uno todos los empleados obtenidos.
for empleado in empleados:

    # 3. Obtenemos todas las sucursales a las que pertenece este empleado.
    # Como hemos utilizado prefetch_related(), Django ya las ha cargado.
    sucursales = empleado.sucursales.all()

    # 4. Contamos cuántas sucursales tiene este empleado.
    # len() cuenta los elementos de la lista (QuerySet precargado).
    total = len(sucursales)

    # 5. Mostramos el nombre del empleado.
    print(empleado.nombre)

    # 6. Mostramos el número total de sucursales de ese empleado.
    print("Total de sucursales:", total)

    # 7. Recorremos todas las sucursales de este empleado.
    for sucursal in sucursales:

        # 8. Mostramos el nombre de cada sucursal.
        print(sucursal.nombre)

        
        --DEBERES USAR LO ANTEERIOR, META, STR




        Utiliza Prefetch para obtener solo los libros disponibles de cada editorial.
        solo los libros cuyo autor no este funado
    '''
