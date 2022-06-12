from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

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
    
    def get_absolute_url(self):
        return f"/detalle_curso/{self.slug}"
    

class Capitulo(models.Model):
    curso = ForeignKey(Curso, on_delete=models.CASCADE, blank=True, null=True)
    numero_capitulo = models.IntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="capitulos", blank=True )
    video = models.FileField(upload_to="capitulos", blank=True)
    contenido = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return f"/detalle_capitulo/{self.curso.slug}/{self.numero_capitulo}"

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
    
    def get_absolute_url(self):
        return f"/detalle_leccion/{self.capitulo.curso.slug}/{self.capitulo.numero_capitulo}/{self.numero_leccion}"
    
class Mensaje(models.Model):
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    mensaje = models.TextField()
    
    def __str__(self): 
        return f"{self.nombre} {self.apellido}"

class MisCursos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    curso = ManyToManyField(Curso)
    inscripcion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ["-inscripcion"]
    
    def __str__(self):
        return self.usuario.email
    
    def get_absolute_url(self):
        return f"/detalle_curso/{self.curso.slug}"
    
    
    """
    @property
    def is_active(self):
        return self.estado == "activo" or self.estado == "inactivo"
    """