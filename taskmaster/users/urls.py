from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_users, name='user-list'),
    path('create/', views.create_user, name='user-create'),
    path('<int:user_id>/', views.detail_user, name='user-detail'),
    path('<int:user_id>/update/', views.update_user, name='user-update'),
    path('<int:user_id>/delete/', views.delete_user, name='user-delete'),
    path('<int:user_id>/reactivate_user//', views.reactivate_user, name='user-reactivate'),
    
    # Manejo de sesión
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]
