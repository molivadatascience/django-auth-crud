from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, HijosForm, DetalleOportunidadForm
from .models import Task,Hijos, DetalleOportunidad
from django.utils import timezone
from django.contrib.auth.decorators import login_required #es para proteger los accesos al programa

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Cualquiera puede entrar a la APP para logearse
def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
         })
    else:
        if request.POST['password1'] ==request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST
                    ['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return  render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error":'User already exists'
            })
        return render(request, 'signup.html',{
                'form': UserCreationForm,
                "error":'Password do not match'
            })
    

@login_required #no cualquiera puede acceder a generar nuevos datos
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) #Me dara las tareas del usuario actual y que la fecha de completado sea nula es decir tareas pendientes
    return render(request, 'tasks.html',{'tasks': tasks})

@login_required #no cualquiera puede acceder a generar nuevos datos
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #Me dara las tareas del usuario actual y que la fecha de completado sea nula es decir tareas pendientes
    return render(request, 'tasks.html',{'tasks': tasks})

@login_required #no cualquiera puede acceder a generar nuevos datos
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            form= TaskForm(request.POST) #print(request.POST) para imprimir en consola el dato ingresado en el formulario
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error': 'Pleace provide valida data'
            })

@login_required #no cualquiera puede acceder a generar nuevos datos
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user) #user=request.user para que cada usuario actualice sus tareas
        form = TaskForm(instance=task)
        #form_hijos = HijosForm(instance=task)
        return render(request, 'task_detail.html',{'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user) #user=request.user para que cada usuario actualice sus tareas
            form = TaskForm(request.POST, instance=task)
            #form_hijos = HijosForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{'task': task, 'form': form, 'error': "Error updating task"})

@login_required #no cualquiera puede acceder a generar nuevos datos        
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save() 
        return redirect('tasks')   
    
@login_required #no cualquiera puede acceder a generar nuevos datos  
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')   

@login_required #no cualquiera puede acceder a generar nuevos datos 
def signout (request):
    logout(request)
    return redirect('home')

#no es necesario loguarse para entrar a esta sección
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
         })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
        })
        else:
            login(request, user)
            return redirect('tasks')

#@login_required #no cualquiera puede acceder a generar nuevos datos
#def task_detail(request):
#    tasks = Task.objects.all()
#    return render(request, 'task_detail.html', {'tasks': tasks})

  

#from .models import DetalleOportunidad
#from .forms import DetalleOportunidadForm

# OBSERVACIONESSSSSSS

# a lo mejor en return form ya existe antes que puedo hacer??
# crear crear_detalle_oportunidad.htm
# lista_detalles_oportunidad.html


def crear_detalle_oportunidad(request):
    if request.method == 'POST':
        form = DetalleOportunidadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_detalles_oportunidad')
    else:
        form = DetalleOportunidadForm()
    return render(request, 'crear_detalle_oportunidad.html', {'form': form})

def lista_detalles_oportunidad(request):
    detalles = DetalleOportunidad.objects.all()
    return render(request, 'lista_detalles_oportunidad.html', {'detalles': detalles})
   
    