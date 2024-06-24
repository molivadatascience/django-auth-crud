from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, DetalleOportunidadForm, ArchivoAdjuntoFormSet,ArchivoAdjuntoForm
from .models import Task, DetalleOportunidad,ArchivoAdjunto
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        detalle_oportunidad_form = DetalleOportunidadForm(request.POST)
        formset = ArchivoAdjuntoFormSet(request.POST, request.FILES, queryset=ArchivoAdjunto.objects.none())
        
        if task_form.is_valid() and detalle_oportunidad_form.is_valid() and formset.is_valid():
            task_instance = task_form.save(commit=False)
            task_instance.user = request.user
            task_instance.save()

            detalle_oportunidad_instance = detalle_oportunidad_form.save(commit=False)
            detalle_oportunidad_instance.task = task_instance
            detalle_oportunidad_instance.save()

            for form in formset:
                if form.cleaned_data.get('archivo'):
                    archivo_adjunto = form.save(commit=False)
                    archivo_adjunto.detalle_oportunidad = detalle_oportunidad_instance
                    archivo_adjunto.save()

            return redirect('dashboard')  # Redirige a donde necesites después de guardar

    else:
        task_form = TaskForm()
        detalle_oportunidad_form = DetalleOportunidadForm()
        formset = ArchivoAdjuntoFormSet(queryset=ArchivoAdjunto.objects.none())

    context = {
        'task_form': task_form,
        'detalle_oportunidad_form': detalle_oportunidad_form,
        'formset': formset,
    }

    return render(request, 'create_task.html', context)


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