"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'), #para mostrar las tareas completadas
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('tasks/<int:task_id>/crear_detalle_oportunidad/', views.crear_detalle_oportunidad, name='crear_detalle_oportunidad'),
    path('lista_detalles_oportunidad/', views.lista_detalles_oportunidad, name='lista_detalles_oportunidad'),

# Nuevas rutas para editar, actualizar y eliminar tareas, detalles de oportunidad y costeos
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'),
    path('update_task/<int:id>/', views.update_task, name='update_task'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('edit_detalle/<int:id>/', views.edit_detalle, name='edit_detalle'),
    path('update_detalle/<int:id>/', views.update_detalle, name='update_detalle'),
    path('delete_detalle/<int:id>/', views.delete_detalle, name='delete_detalle'),
    path('edit_costeo/<int:id>/', views.edit_costeo, name='edit_costeo'),
    path('update_costeo/<int:id>/', views.update_costeo, name='update_costeo'),
    path('delete_costeo/<int:id>/', views.delete_costeo, name='delete_costeo'),
    path('create_task/', views.create_task, name='create_task'),
    path('edit_task/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
    #path('create_costeo/', views.create_costeo, name='create_costeo'),
    path('create_costeo/<int:detalle_oportunidad_id>/', views.create_costeo, name='create_costeo'),
    path('edit_costeo/<int:costeo_id>/', views.edit_costeo, name='edit_costeo'),
    path('delete_costeo/<int:costeo_id>/', views.delete_costeo, name='delete_costeo'),
]

