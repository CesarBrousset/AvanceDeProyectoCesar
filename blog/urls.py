from django.urls import path
from blog import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", views.inicio, name="Inicio"),
    path("articulos/", views.articulos, name="Articulos"),
    path("categoria/", views.categoria, name="Categoria"),
    path("comentarios/", views.comentarios, name="Comentarios"),
    path("respuesta_buscar/", views.respuestaBuscar, name="RespuestaBuscar"),
    path("buscar/", views.buscar, name="Buscar"),
    path("comentarios-lista/", views.listar_comentarios),
    path("comentario/list", views.ComentarioList.as_view(), name="ComentarioList"),
    path(
        "r'(?P<pk>\d+)^$'", views.ComentarioDetalle.as_view(), name="ComentarioDetail"
    ),
    # Porque sorete no me importa estas clases desde las views!!???
    path("comentario-nuevo/", views.ComentarioCreacion.as_view(), name="ComentarioNew"),
    path("editar/<pk>", views.ComentarioUpdateView.as_view(), name="ComentarioUpdate"),
    path("borrar/<pk>", views.ComentarioDelete.as_view(), name="ComentarioDelete"),
    path("login", views.login_request, name="login"),
    path("register/", views.register, name="Register"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="Logout"),
]
