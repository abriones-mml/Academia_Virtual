from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone

class Tutor(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Curso(models.Model):
    autores = ManyToManyField(Tutor)
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="cursos", null=True)
    video = models.FileField(upload_to="cursos", blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publicado', null=False, unique=True)
    publicado = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return self.titulo

class Capitulo(models.Model):
    curso = ForeignKey(Curso, on_delete=models.CASCADE, blank=True, null=True)
    numero_capitulo = models.IntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="capitulos", blank=True )
    video = models.FileField(upload_to="capitulos", blank=True)
    contenido = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Leccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE,blank=True, null=True)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE,blank=True, null=True)
    numero_leccion = models.IntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="lecciones", blank=True)
    video = models.FileField(upload_to="lecciones", blank=True)
    contenido = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo