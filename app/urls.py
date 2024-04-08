from django.urls import path 
from . import views
from .views import DetailMs,Inbox
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('inicio/',views.inicio, name = 'inicio'),

	path('register/', views.register, name='register'),
	path('',LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/',LogoutView.as_view(), name='logout'),
	path('delete/<int:post_id>', views.delete,name='delete'),
	path('deleteComent/<int:post_id>', views.deleteComent,name='deleteComent'),
	path('like/<int:post_id>', views.like,name='like'),
	path('likeComentario/<int:comentario_id>', views.likeComentario,name='likeComentario'),
	path('comentario/<int:post_id>', views.comentario,name='comentario'),
	
	path('editarPost/<int:pk>',views.editarPost,name='editarPost'),
	path('profile/<str:username>',views.profile,name='profile'),
	path('editar/',views.editar,name='editar'),
	path('follow/<str:username>',views.follow,name='follow'),
	path('unfollow/<str:username>',views.unfollow,name='unfollow'),
	path('Buscar/',views.Buscar,name='Buscar'),
	path('Busqueda/',views.Busqueda,name='Busqueda'),

	
	path('ms/<str:username>',DetailMs.as_view(),name='detailMs'),
	path('',Inbox.as_view(),name="inbox"),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)








'''
Para hacer el login solo hay que importar las vistas y 
crear las urls y nos digirimos a settings y se llaman las urls

59895009508
'''
