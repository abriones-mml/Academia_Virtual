from django.urls import path
from .views import detalle_curso, index, cursos, registro_tutor,\
registro_curso, lista_cursos, editar_curso, eliminar_curso, registro_usuario, login_user, logout_user

urlpatterns = [
    path('', index, name= "index"),
    path("cursos/", cursos, name= "cursos"),
    path("registro_curso/", registro_curso, name= "registro_curso"),
    path("lista_cursos/", lista_cursos, name= "lista_cursos"),
    path("detalle_curso/<int:pk>", detalle_curso, name= "detalle_curso"),
    path("registro_tutor/", registro_tutor, name= "registro_tutor"),
    path("editar_curso/<id>/", editar_curso, name= "editar_curso"),
    path("eliminar_curso/<id>/", eliminar_curso, name= "eliminar_curso"),
    path("registro_usuario/", registro_usuario, name= "registro_usuario"),
    path("login/", login_user, name= "login"),
    path('logout/', logout_user, name= 'logout'),
]