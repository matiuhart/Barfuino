from django.contrib import admin
from tempcontrol.models import *


class FermentadoresAdmin(admin.ModelAdmin):
	list_display = ('nombre','activo') # Autores redefinida en modelo por se ManyToMany
	list_filter = ('activo','nombre')
	ordering = ('nombre',)
	fields = ('nombre','activo') #Cambia orden y campos mostrados en edicion
	#filter_horizontal = ('autores',) # Solo trabajan con campos ManyToMany
	#filter_vertical = ('autores',)
	#raw_id_fields = ('editores',) # Seleccion con id


class SensoresAdmin(admin.ModelAdmin):
	list_display = ('nombre','fermentador','mac','activo') # Autores redefinida en modelo por se ManyToMany
	list_filter = ('nombre','fermentador','activo')
	ordering = ('nombre',)
	fields = ('nombre','fermentador','mac','activo') #Cambia orden y campos mostrados en edicion
	#filter_horizontal = ('autores',) # Solo trabajan con campos ManyToMany
	#filter_vertical = ('autores',)
	#raw_id_fields = ('fermentador',) # Seleccion con id


class ControlProcesosAdmin(admin.ModelAdmin):
	list_display = ('coccionNum','fermentador','sensor','temperaturaPerfil','fechaInicio',
	'fermentado1Fin','fermentado2Fin','maduradoFin','clarificadoFin','activo') # Autores redefinida en modelo por se ManyToMany
	list_filter = ('coccionNum','fermentador','sensor','temperaturaPerfil','activo')
	ordering = ('coccionNum',)
	fields = ('coccionNum','fermentador','sensor','temperaturaPerfil','fechaInicio',
	'fermentado1Fin','fermentado2Fin','maduradoFin','clarificadoFin','activo') #Cambia orden y campos mostrados en edicion
	#filter_horizontal = ('autores',) # Solo trabajan con campos ManyToMany
	#filter_vertical = ('autores',)
	#raw_id_fields = ('fermentador',) # Seleccion con id

class TemperaturasPerfilesAdmin(admin.ModelAdmin):
	list_display = ('nombre','diasFermentado1','diasFermentado2','diasMadurado','diasclarificado',
	'temperaturas','descripcion') # Autores redefinida en modelo por se ManyToMany
	list_filter = ('diasFermentado1','diasFermentado2','diasMadurado','diasclarificado')
	ordering = ('nombre',)
	#fields = ('coccionNum','fermentador','sensor','temperaturaPerfil','activo')

class TemperaturasHistorialAdmin(admin.ModelAdmin):
	list_display = ('coccionNumero','fermentador','sensorId','temperatura','fechaSensado') # Autores redefinida en modelo por se ManyToMany
	list_filter = ('coccionNumero','fermentador','sensorId','temperatura','fechaSensado',)
	ordering = ('coccionNumero','fermentador',)
	raw_id_fields = ('coccionNumero',)

# Register your models here.

admin.site.register(Fermentadores,FermentadoresAdmin)
admin.site.register(Sensores,SensoresAdmin)
admin.site.register(TemperaturasHistorial,TemperaturasHistorialAdmin)
admin.site.register(TemperaturasPerfiles,TemperaturasPerfilesAdmin)
admin.site.register(ControlProcesos,ControlProcesosAdmin)
