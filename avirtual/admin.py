from django.contrib import admin
from .models import Tutor, Curso, Capitulo, Leccion, Mensaje, MisCursos

admin.site.register(Tutor)
admin.site.register(Curso)
admin.site.register(Capitulo)
admin.site.register(Leccion)
admin.site.register(Mensaje)
admin.site.register(MisCursos)
