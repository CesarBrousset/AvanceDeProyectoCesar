from contextlib import ContextDecorator
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from blog.forms import articuloFormulario, categoriaFormulario, comentarioFormulario
from blog.models import Articulo, Categoria, Comentario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from blog.forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from primeraentregablog.primeraentrega.blog.models import Avatar


# inicio
@login_required
def inicio(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    urls = {"Categoria", "Articulos", "Comentarios"}
    titulo = "Formularios"
    contenido = {"urls": urls, "titulo": titulo}
    return render(request, "index.html", contenido, {"url": avatares[0].imagen.url})


def categoria(request):
    titulo = "Categoria"
    if request.method != "POST":
        formulario = categoriaFormulario()
    else:
        formulario = categoriaFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            articulo = Categoria(nombre=informacion["nombre"])
            articulo.save()
            return render(request, "respuesta.html", {"titulo": titulo})
    contenido = {"formulario": formulario, "titulo": titulo}
    return render(request, "categoria.html", contenido)


def articulos(request):
    titulo = "Articulos"
    if request.method != "POST":
        formulario = articuloFormulario()
    else:
        formulario = articuloFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            articulo = Articulo(
                titulo=informacion["titulo"],
                texto=informacion["texto"],
                fecha=informacion["fecha"],
                estado=informacion["estado"],
            )
            articulo.save()
            return render(request, "respuesta.html", {"titulo": titulo})
    contenido = {"formulario": formulario, "titulo": titulo}
    return render(request, "articulos.html", contenido)


def comentarios(request):
    titulo = "Comentarios"
    if request.method != "POST":
        formulario = comentarioFormulario()
    else:
        formulario = comentarioFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            articulo = Comentario(
                comentario=informacion["comentario"],
                nombre=informacion["nombre"],
                apellido=informacion["apellido"],
                email=informacion["email"],
                fecha=informacion["fecha"],
                estado=informacion["estado"],
            )
            articulo.save()
            return render(request, "respuesta.html", {"titulo": titulo})
    contenido = {"formulario": formulario, "titulo": titulo}
    return render(request, "comentarios.html", contenido)


def buscar(request):
    titulo = "Buscar"
    return render(request, "buscar.html", {"titulo": titulo})


def respuestaBuscar(request):
    titulo = "Resultado de Busqueda"
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        filtro = Comentario.objects.filter(nombre__icontains=nombre)
        contenido = {"filtro": filtro, "titulo": titulo, "buscando": nombre}
        return render(request, "respuesta_busqueda.html", contenido)
    else:
        respuesta = "No enviaste datos"
        return render(
            request,
            "respuesta_busqueda.html",
            {"respuesta": respuesta, "titulo": titulo},
        )


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


from django.urls import reverse


class ComentarioList(ListView):
    model = Comentario
    template_name = "comentarios_list.html"


def listar_comentarios(request):
    todos_los_comentarios = Comentario.objects.all()
    contexto = {"comentarios_encontrados": todos_los_comentarios}
    return render(request, "comentarios_list.html", contexto)


class ComentarioDetalle(DetailView):
    model = Comentario
    template_name = "comentario_detalle.html"


class ClaseQueNecesitaLogin1(LoginRequiredMixin):
    class ComentarioCreacion(CreateView):
        model = Comentario
        fields = ["comentario", "nombre", "apellido", "email", "fecha"]

        def get_success_url(self):
            return reverse("ComentarioList")


class ClaseQueNecesitaLogin2(LoginRequiredMixin):
    class ComentarioUpdateView(UpdateView):
        model = Comentario
        success_url = "comentario/list"
        fields = ["comentario", "nombre", "apellido", "email", "fecha"]


class ClaseQueNecesitaLogin3(LoginRequiredMixin):
    class ComentarioDelete(DeleteView):

        model = Comentario
        success_url = "comentario/list"


def busqueda_de_comentario(request):
    return render(request, "buscar.html")


def buscar_comentario(request):
    if not request.GET["nombre"]:
        return HttpResponse("No enviaste datos")
    else:
        nombre_a_buscar = request.GET["nombre"]
        comentarios = Comentario.objects.filter(nombre=nombre_a_buscar)

        contexto = {"nombre": nombre_a_buscar, "comentarios_encontrados": comentarios}

        return render(request, "resultado_busqueda.html", contexto)


def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario, password=contra)

            if user is not None:
                login(request, user)

                return render(
                    request, "index.html", {"mensaje": f"Bienvenido {usuario}"}
                )
            else:

                return render(
                    request,
                    "index.html",
                    {"mensaje": "Error, datos incorrectos"},
                )

        else:

            return render(
                request, "index.html", {"mensaje": "Error, formulario erroneo"}
            )

    form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username_capturado = form.cleaned_data["username"]
            form.save()

            return render(
                request, "index.html", {"mensaje": f"Usuario: {username_capturado}"}
            )

    else:
        form = UserRegisterForm()

    return render(request, "registro.html", {"form": form})


@login_required
def editarPerfil(request):
    usuario = request.user

    if request.method == "POST":
        miFormulario = UserEditForm(request.POST)
        if miFormulario.is_valid:

            informacion = miFormulario.cleaned_data

            usuario.email = informacion["email"]
            usuario.password1 = informacion["password1"]
            usuario.password2 = informacion["password1"]
            usuario.save()

            return render(request, "index.html")

    else:

        miFormulario = UserEditForm(initial={"email": usuario.email})

    return render(request, "editarPerfil.html", {"miFormulario": miFormulario})


@login_required
def agregarAvatar(request):
    if request.method == "POST":

        miFormulario = AvatarFormulario(request.POST, request.FILES)

        if miFormulario.is_valid:

            u = User.objects.get(username=request.user)
            avatar = Avatar(user=u, imagen=miFormulario.cleaned_data["imagen"])
            avatar.save()
            return render(request, "index.html")

    else:

        miFormulario = AvatarFormulario()

    return render(request, "agregarAvatar.html", {"miFormulario": miFormulario})
