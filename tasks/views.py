from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, DetalleOportunidadForm, CosteoForm
from .models import Task, DetalleOportunidad, Costeo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
#from django.forms import modelformset_factory
from django.forms import modelformset_factory


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'User already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Passwords do not match'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        task_form = TaskForm()
        detalle_oportunidad_form = DetalleOportunidadForm()
        costeo_form = CosteoForm()
        return render(request, 'create_task.html', {
            'task_form': task_form,
            'detalle_oportunidad_form': detalle_oportunidad_form,
            'costeo_form': costeo_form,
        })
    elif request.method == 'POST':
        task_form = TaskForm(request.POST)
        detalle_oportunidad_form = DetalleOportunidadForm(request.POST, request.FILES)
        costeo_form = CosteoForm(request.POST)
        
        if task_form.is_valid() and detalle_oportunidad_form.is_valid() and costeo_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            
            new_detalle = detalle_oportunidad_form.save(commit=False)
            new_detalle.task = new_task
            new_detalle.save()
            
            new_costeo = costeo_form.save(commit=False)
            new_costeo.detalle_oportunidad = new_detalle
            new_costeo.save()
            
            return redirect('tasks')
        else:
            return render(request, 'create_task.html', {
                'task_form': task_form,
                'detalle_oportunidad_form': detalle_oportunidad_form,
                'costeo_form': costeo_form,
                'error': 'Please provide valid data'
            })



@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        detalle_form = DetalleOportunidadForm()
        detalles = DetalleOportunidad.objects.filter(task=task)
        return render(request, 'task_detail.html', {
            'task': task, 
            'form': form, 
            'detalles': detalles, 
            'detalle_form': detalle_form
        })
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task_detail', task_id=task.id)
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': "Error updating task"
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def crear_detalle_oportunidad(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = DetalleOportunidadForm(request.POST, request.FILES)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.task = task
            detalle.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = DetalleOportunidadForm()
    return render(request, 'crear_detalle_oportunidad.html', {'form': form, 'task': task})

@login_required
def lista_detalles_oportunidad(request):
    detalles = DetalleOportunidad.objects.all()
    return render(request, 'lista_detalles_oportunidad.html', {'detalles': detalles})