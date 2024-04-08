from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
import os
import uuid
from django.db.models import Count
from django.apps import apps
from django.conf import settings
# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	bio = models.CharField(default='Hola Fox', max_length = 20)
	telefono = models.IntegerField(null=True)
	image = models.ImageField(default='imag.png')
	pais = models.CharField(null = True,max_length = 20)
	city = models.CharField(null = True,max_length = 20)

	def __str__(self):
		return f'{self.user.username}'
		
	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user)\
							.values_list('to_user_id',flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user)\
							.values_list('from_user_id',flat=True)
		return User.objects.filter(id__in=user_ids)

	

class Post(models.Model):
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.CharField(null=True, blank=True, max_length=30)
	image = models.ImageField()
	likes = models.ManyToManyField(User, related_name="likes")
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')

	def delete(self,*args,**kwargs):
		if os.path.isfile(self.image.path):
			os.remove(self.image.path)
		super(Post,self).delete(*args, **kwargs)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f'{self.content } -  - -  {self.user}'


#comentarios
class Comentario(models.Model):
	hora = models.DateTimeField(default=timezone.now)
	contenido = models.CharField( max_length=150)
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comentario')
	postCom = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='postCom')
	likes = models.ManyToManyField(User, related_name="likesComentario")

	class Meta:
		ordering = ['-hora']

	def __str__(self):
		return f'{self.contenido }'




class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationship', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} a {self.to_user}'

	class Meta:
		indexes = [
		models.Index(fields=['from_user','to_user',]),
		]




#funcion para cuando se cree un usuario crear un perfil(signals)
def crear_perfil(sender, instance, created,**kwargs):
	if created:
		Profile.objects.create(user=instance)

post_save.connect(crear_perfil,sender=User)



#chat ***************************************


class ModelBase(models.Model):
	id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False)
	tiempo = models.DateTimeField(auto_now_add=True)
	actualizar = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		abstract = True


class CanalMensaje(ModelBase):
	canal = models.ForeignKey("Canal", on_delete=models.CASCADE)
	usuario = models.ForeignKey(User,on_delete=models.CASCADE)
	texto = models.TextField()

class CanalUsuario(ModelBase):
	canal = models.ForeignKey("Canal",null=True, on_delete=models.SET_NULL)
	usuario = models.ForeignKey(User,on_delete=models.CASCADE)


class CanalQuerySet(models.QuerySet):

	def solo_dos(self):
		return self.annotate(num_usuarios = Count("usuarios")).filter(num_usuarios=2)

	def solo_uno(self):
		return self.annotate(num_usuarios = Count("usuarios")).filter(num_usuarios=1)

	def filtrar_por_username(self,username):
		return self.filter(canalusuario__usuario__username=username)

class CanalManager(models.Manager):
	
	def get_queryset(self,*args,**kwargs):
		return CanalQuerySet(self.model, using=self._db)

	def filtrar_ms_por_privado(self,username_a,username_b):
		return self.get_queryset().solo_dos().filtrar_por_username(username_a).filtrar_por_username(username_b)


	def canal_usuario_actual(self, user):
		qs = self.get_queryset().solo_uno().filtrar_por_username(user.username)
		if qs.exists():
			return qs.order_by("tiempo").first,False

		canal_obj = Canal.objects.create()
		CanalUsuario.objects.create(usuario=user, canal=canal_obj)
		return canal_obj, True

	def obtener_crear_canal_mensaje(self,username_a,username_b):
		qs = self.filtrar_ms_por_privado(username_a,username_b)
		if qs.exists():
			return qs.order_by("tiempo").first(), False

		User = apps.get_model("auth",model_name="User")
		usuario_a, usuario_b = None, None

		try:
			usuario_a = User.objects.get(username=username_a)

		except User.DoesNotExits:
			return None, False
		
		try:
			usuario_b = User.objects.get(username=username_b)

		except User.DoesNotExits:
			return None, False

		if usuario_a == None or usuario_b == None:
			return None, False

		obj_canal = Canal.objects.create()
		User = apps.get_model("auth", model_name='User')
		canal_usuario_a = CanalUsuario(usuario=User.objects.get(username=username_a),canal=obj_canal)
		canal_usuario_b = CanalUsuario(usuario=User.objects.get(username=username_b),canal=obj_canal)
		CanalUsuario.objects.bulk_create([canal_usuario_a,canal_usuario_b])
		return obj_canal,True

class Canal(ModelBase):
	usuarios = models.ManyToManyField(User,blank = True, through=CanalUsuario)
	objects = CanalManager()












