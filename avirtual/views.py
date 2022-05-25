from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso
from .forms import TutorForm, CursoForm, CustomUserCreationForm
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

@login_required
def detalle_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    data = {
        "curso": curso
    }
    return render(request, 'avirtual/curso/detalle_curso.html', data)

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