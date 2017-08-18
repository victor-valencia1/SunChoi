# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView,FormView,ListView
from .forms import *
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from django.contrib.auth.models import User
from .models import *

#vistas generales
def login(request):
    if (request.method == 'POST'):
        tipologin=request.POST['tipologin']
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if(user.is_superuser and user.is_staff and tipologin=="admin"):
                auth_login(request, user)
                datosUsuario = Usuario.objects.get(usuario=user)
                return render(request,'SunChoi/menuGlobal.html',{'usuario': datosUsuario})
            elif((not user.is_superuser or  not user.is_staff) and tipologin=="empleado" ):
                auth_login(request, user)
                datosUsuario = Usuario.objects.get(usuario=user)
                return render(request,'SunChoi/menuempleado.html',{'usuario': datosUsuario})
            else:
                return render(request,'SunChoi/index.html',{'error':True})
        else:
            return render(request,'SunChoi/index.html',{'error':True})
    else:
        return render(request,'SunChoi/index.html',{'error':False})

def logout(request):
    auth_logout(request)
    return render(request,'SunChoi/logout.html')

def nopermitido(request):
    return render_to_response('SunChoi/nopermitido.html')

def MenuGlobal(request):
    if (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return render(request,'SunChoi/menuGlobal.html')
    else:
        return render_to_response('SunChoi/nopermitido.html')

def MenuEmpleado(request):
    if (request.user.is_authenticated and (not request.user.is_superuser or  not request.user.is_staff)):
        return render(request,'SunChoi/menuempleado.html')
    else:
        return render_to_response('SunChoi/nopermitido.html')

#vistas usuario
def Usuarios(request):
    if (request.user.is_authenticated):
        lista_usuarios = Usuario.objects.all()
        return render(request,'SunChoi/usuarios.html',{'lista_usuarios': lista_usuarios})
    else:
        return render_to_response('SunChoi/nopermitido.html')

def RegistrarUsuario(request):
    if (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        if request.method == 'POST':
            tipouser=request.POST['tipouser'] 
            form = UsuarioForm(request.POST) 
            if form.is_valid():
                nombre = request.POST['nombre']
                usuario = request.POST['username']
                apellido = request.POST['apellido']
                direccion=request.POST['direccion']
                telefono=request.POST['telefono']
                contrasena=request.POST['contrasena']
                correo=request.POST['correo']
                tipologin=request.POST['tipouser']
                if tipouser=="admin":
                    is_superuser=1 #con atributo is_superuser=1 para acceder a admin web 
                    is_staff=1     # para poder acceder a menu global
                else:
                    is_superuser=0 #con atributo is_superuser=1 para acceder a admin web 
                    is_staff=0     # para poder acceder a menu global
                user=User.objects.create_user(username=usuario, is_superuser=is_superuser,email=correo, password=contrasena,is_staff=is_staff)
                Usuario.objects.create(nombre=nombre,usuario=user,apellido=apellido,direccion=direccion,
                    telefono=telefono,correo=correo) 
                datosUsuario = Usuario.objects.get(usuario=user)
                users = authenticate(username=usuario, password=contrasena)
                auth_login(request, users)
                if tipouser=="admin":
                    return render(request,'SunChoi/menuGlobal.html')
                else:
                    return render(request,'SunChoi/menuempleado.html')
            else:
                form=UsuarioForm()
                return render(request,'SunChoi/registrarEmpleados.html',{'form': form, 'error':"no lleno correctamente la información"})
        else:
            form = UsuarioForm()    
            return render(request,'SunChoi/registrarEmpleados.html',{'form': form})
    else:
        return render(request,'SunChoi/nopermitido.html')

    #productos
def RegistrarProducto(request):
    if (request.user.is_authenticated):
        if request.method == 'POST': 
            form = ProductoForm(request.POST) 
            #valid
            if form.is_valid():
                nueva_producto= form.save() 
                return render(request,'SunChoi/menuGlobal.html')
        form = ProductoForm()
        return render(request,'SunChoi/registrarProducto.html', {'form': form})
    else:
        return render_to_response('SunChoi/nopermitido.html')

    #proveedores
def Proveedores(request):     
    if (request.user.is_authenticated):
        return render(request,'SunChoi/proveedores.html',{'mjsexitoso': "puede ingresar mas proveedores"})
    else:
        return render_to_response('SunChoi/nopermitido.html')

#operaciones
def RegistrarVenta(request):
    if (request.user.is_authenticated):
        if request.method == 'POST': 
            form = FacturaForm(request.POST) 
            form1 = FacturalineaForm(request.POST) 
            form2 = FacturalineaForm(request.POST) 
            #valid
            if form.is_valid() and form1.is_valid() and form2.is_valid():
                nueva_factura = form.save() 
                detalle_factura1 = form1.save() 
                detalle_factura2 = form2.save() 
                return render(request,'SunChoi/menuGlobal.html')
        form = FacturaForm()
        form1=FacturalineaForm() 
        form2=FacturalineaForm() 
        return render(request,'SunChoi/registrarVenta.html', {'form': form, 'form1': form1,'form2': form2})
    else:
        return render_to_response('SunChoi/nopermitido.html')

def Compras(request):
    if (request.user.is_authenticated):
        return render(request,'SunChoi/compras.html')
    else:
        return render_to_response('SunChoi/nopermitido.html')

def Cotizaciones(request):
    if (request.user.is_authenticated):
        return render(request,'SunChoi/cotizaciones.html')
    else:
        return render_to_response('SunChoi/nopermitido.html')

def ConsultaRapida(request):
    if request.GET.get('minimo'):
        minimo = request.GET['minimo']
        if minimo.isdigit():
            results = Producto.bajostock(minimo)
            return render(request,'SunChoi/consultaRapida.html',{'lista':results,"minimo": minimo})
        else:
            return render(request,'SunChoi/consultaRapida.html',{"minimo": minimo,"error": "debe ingresar un número válido por favor. Intente de nuevo"})
    else:
        return render(request,'SunChoi/consultaRapida.html')

#reportes
def Inventarios(request):
    if (request.user.is_authenticated):
        return render(request,'SunChoi/inventarios.html')
    else:
        return render_to_response('SunChoi/nopermitido.html')

#clientes
def RegistrarCliente(request):
    if (request.user.is_authenticated):
        if request.method == 'POST': 
            form = ClienteForm(request.POST) 
            if form.is_valid():
                #aun no lo guarda entonces se puede validar
                nc=form.save(commit=False)
                try:
                    Cliente.insertcliente(nc.dni,nc.nombre,nc.apellidos,nc.direccion,nc.telefono)
                    form=ClienteForm()
                    return render(request, 'SunChoi/registrocliente.html', {'form': form, 'mjs': "puede ingresar mas clientes"})
                except ValueError:
                    form=ClienteForm()
                    return render(request, 'SunChoi/registrocliente.html', {'form': form, 'mjs': "xcdv"})
        else:
            form = ClienteForm()
        return render(request, 'SunChoi/registrocliente.html', {'form': form})
    else:
        return render_to_response('SunChoi/nopermitido.html')

def VistaCliente(request):
    if request.user.is_authenticated:
            form = ClienteForm() 
            return render(request, 'SunChoi/vistacliente.html', {'form': form})
    else:
        return render_to_response('SunChoi/nopermitido.html')



def F(request):
    return render_to_response('SunChoi/Factura.html')




class ProductoListView(ListView):
    model = Producto