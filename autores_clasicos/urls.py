from django.urls import path
from . import views

urlpatterns= [
    path('', views.funcion_principal, name='inicio'),
    path('detalle/<int:id>/', views.detalle_autor, name='detalle_autor'),
    path('descripcion/', views.descripcion_web, name='descripcion'),
    path('contacto/', views.contacto_empresa, name='contacto'),
    path('libros/<int:id>', views.libros_autor, name='libros_autor_actual')
]   