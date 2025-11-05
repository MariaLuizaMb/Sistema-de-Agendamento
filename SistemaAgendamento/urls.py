"""
URL configuration for SistemaAgendamento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from agendamento import views
from agendamento.views import CustomLoginView, home


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),  # login na raiz
    path('register/', views.register_view, name='register'),
    path('home/', home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('agendamentos/', views.usuario_agendamentos, name='agendamentos'),
    path('criar_agendamento/', views.criar_agendamento, name='criar_agendamento'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('editar-perfil/<int:user_id>/', views.editar_perfil, name='editar_usuario_admin'),
    path('agendamento/<int:id>/', views.detalhes_agendamento, name='detalhes_agendamento'),
]
