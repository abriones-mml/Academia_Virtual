from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Capitulo, Leccion, Mensaje, MisCursos
from .forms import TutorForm, CursoForm, CustomUserCreationForm, MensajeForm, MisCursosForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Has iniciado sesión, ¡ Bienvenido {username}!")
                return redirect('index')
        else:
            messages.error(request,"Nombre o contraseña no válidos.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html',context={"login_form":form})

def logout_user(request):
    logout(request)
    messages.success(request, "Haz cerrado sesión exitosamente.") 
    return redirect('index')

def index(request):
    return render(request, "avirtual/index.html")

def cursos(request):
    cursos = Curso.objects.all() # realiza la consulta
    data = {
        "cursos": cursos
    }
    return render(request, "avirtual/curso/cursos.html", data)


""" inicialmente tenia solo esto :D 
@login_required
def detalle_curso(request, slug):
    # obtengo el curso
    curso = get_object_or_404(Curso, slug=slug)  #  ok  1
    
    # filtrar el numero de capitulos que tiene un curso

    capitulo = Capitulo.objects.filter(curso=curso) # lista de capitulos  3
    
    leccion = Leccion.objects.filter(capitulo=capitulo)
    
    # filtrar el numero de lecciones que tiene el capitulo

    data = {
        "curso": curso, # estoy mandando un dato
        "capitulo": capitulo, # estoy mandando una lista
        "leccion": leccion
    }
    return render(request, 'avirtual/curso/detalle_curso.html', data)
"""
@login_required
def detalle_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    data ={
        "curso": curso
    }
    return render(request, 'avirtual/curso/detalle_curso.html', data)

@login_required
def detalle_capitulo(request, slug, numero_capitulo):
    curso = get_object_or_404(Curso, slug = slug)
    capitulo_qs = Capitulo.objects.filter(curso__slug=slug).filter(numero_capitulo=numero_capitulo)
    capitulo = capitulo_qs[0]
    data = {
        "curso": curso,
        "capitulo": capitulo
    }
    return render(request, "avirtual/curso/detalle_capitulo.html", data)

@login_required
def detalle_leccion(request, slug, numero_capitulo, numero_leccion):
    curso = get_object_or_404(Curso, slug = slug)
    capitulo_qs = Capitulo.objects.filter(curso__slug=slug).filter(numero_capitulo=numero_capitulo)
    capitulo = capitulo_qs[0]
    leccion_qs = Leccion.objects \
        .filter(capitulo__curso__slug=slug) \
        .filter(capitulo__numero_capitulo=numero_capitulo) \
        .filter(numero_leccion=numero_leccion)
    leccion = leccion_qs[0]
    data = {
        "curso": curso,
        "capitulo": capitulo,
        "leccion": leccion
    }
    return render(request, "avirtual/curso/detalle_leccion.html", data)

@permission_required("avirtual.add_curso")
def registro_curso(request):
    data = {
        "form": CursoForm()
    }
    if request.method == "POST":
        formulario = CursoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Curso registrado exitosamente")
        else:
            data["form"] = formulario
    return render(request, "avirtual/curso/registro_curso.html", data)

@permission_required("avirtual.view_curso")
def lista_cursos(request):
    
    cursos = Curso.objects.all() # realiza la consulta
    data = {
        "cursos": cursos
    }
    return render(request, "avirtual/curso/lista_cursos.html", data)

@permission_required("avirtual.change_curso")
def editar_curso(request, id):
    
    curso = get_object_or_404(Curso, id=id)
    data = {
        "form": CursoForm(instance=curso)
    }
    if request.method == "POST":
        formulario = CursoForm(data=request.POST, instance=curso, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Curso editado exitosamente!")
            return redirect(to="lista_cursos")
        data["form"] = formulario
    return render(request, "avirtual/curso/editar_curso.html", data)

@permission_required("avirtual.delete_curso")
def eliminar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    curso.delete()
    messages.success(request, "Curso Eliminado")
    return redirect(to="lista_cursos")


@permission_required("avirtual.add_tutor")
def registro_tutor(request):
    data = {
        "form": TutorForm()
    }
    if request.method == "POST":
        formulario = TutorForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Tutor Registrado Correctamente!")
        else:
            data["form"] = formulario
    return render(request, "avirtual/tutor/registro_tutor.html", data)

def registro_usuario(request):
    data = {
        "form": CustomUserCreationForm()
    }
    if request.method == "POST":
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Has registrado tus datos correctamente")
            return redirect(to="index")
        data["form"] = formulario
    return render(request, "registration/registro.html", data)

def inbox(request):
    
    email = request.user.email
    mensaje = Mensaje.objects.filter(email=email).all()

    data = { 
            'comentarios': mensaje,
    } 
    return render(request,'avirtual/mensajes/inbox.html', data)

def mensaje(request):
    data = {
        "mensaje": MensajeForm()
    }
    if request.method == "POST":
        formulario = MensajeForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Mensaje enviado exitosamente")
        else:
            data["mensaje"] = formulario
    return render(request, "avirtual/mensajes/mensaje.html", data)

def mis_cursos(request):
    id_usuario = request.user.id
    cursos = MisCursos.objects.filter(usuario_id=id_usuario).all()

    data = { 
            'cursos': cursos,
    } 
    return render(request,'avirtual/curso/mis_cursos.html', data)

def inscripcion(request):
    data = {
        "form": MisCursosForm()
    }
    if request.method == "POST":
        formulario = MisCursosForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Curso Inscrito Exitosamente!")
        else:
            data["form"] = formulario
    return render(request, "avirtual/curso/inscripcion.html", data)