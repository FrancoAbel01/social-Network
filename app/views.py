from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Post,Relationship,Comentario,CanalMensaje, CanalUsuario, Canal
from .forms import UserRegisterForm, PostForm,ProfileUpdateForm,FormMensajes, UserUpdateForm,ComentsForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import os
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, JsonResponse

from django.views.generic.edit import FormMixin
# Create your views here.

@login_required
def inicio(request):
	posts = Post.objects.all()
	usuar = request.user.profile.following()
	form = PostForm()
	# publicar el post
	if request.method == 'POST':	
		form = PostForm(request.POST, request.FILES)
		if form.is_valid() :
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('inicio')
	return render(request,'inicio.html',{'posts':posts,'form':form,'usuar':usuar})

def login(request):
	return render(request,'login.html')



#registrar un usuario
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = UserRegisterForm()
	context = {'form':form}
	return render(request,'register.html',context)


@login_required
#borrar
def delete(request,post_id):
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('inicio')

@login_required
def deleteComent(request,post_id):
	post = Comentario.objects.get(id=post_id)
	post.delete()
	return redirect('inicio')

@login_required
def like(request,post_id):

	post = get_object_or_404(Post, id=post_id)
	if request.user in post.likes.all():
		post.likes.remove(request.user)
		
	else:
		post.likes.add(request.user)
		
	return redirect('inicio') 

def likeComentario(request,comentario_id):

	coment = get_object_or_404(Comentario, id=comentario_id)
	if request.user in coment.likes.all():
		coment.likes.remove(request.user)
		comentar(comentario_id)
		
	else:
		coment.likes.add(request.user)
		
	return redirect('inicio') 



def comentar(id):
	return comentario(id)



	


@login_required
def comentario(request,post_id):

	post = get_object_or_404(Post, id=post_id)
	
	#con = post.postCom
	coment = Comentario.objects.all()

	form = ComentsForm()

	# publicar el post
	if request.method == 'POST':
		
		form = ComentsForm(request.POST)

		if form.is_valid() :
			posts = form.save(commit=False)
			posts.user = request.user
			posts.postCom = post
			posts.save()
			return redirect('inicio')
	
	context = {'post':post,'form':form,'coment':coment}
	return render(request,'comentario.html',context)



@login_required
def editarPost(request,pk):
	post = Post.objects.get(id=pk)
	form = PostForm(instance=post)
	if request.method == 'POST':

		form = PostForm(request.POST, request.FILES, instance=post)

		if form.is_valid() :
			post = form.save()
			return redirect('inicio')
		
	return render(request,'post.html',{'form':form})



@login_required
def profile(request,username):
	user = User.objects.get(username=username)#obtenermos el usuario
	posts = user.posts.all()
	form = PostForm()
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('inicio')
		
	context = {'user':user,'posts':posts,'form':form}
	return render(request, 'perfil.html',context)



@login_required
def editar(request):
	
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('inicio')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm()

	context = {'u_form':u_form,'p_form':p_form}
	return render(request, 'editar.html ',context)

# hora del video 1:05



def follow(request,username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user,to_user=to_user_id)
	rel.save()
	
	return redirect('inicio')



def unfollow(request,username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	
	return redirect('inicio')


@login_required
def Buscar(request):
	'''
	nombre = request.GET.get('Buscar')
	user = User.objects.filter(Q(username__icontains=nombre))
	paginator = Paginator(user,100)
	page = request.GET.get('page')
	user = paginator.get_page(page)
	return render(request,'Buscar.html',{'user':user})

'''
	return render(request,'Buscar.html')


@login_required
def Busqueda(request):
	nombre = request.GET.get('Busqueda')
	user = User.objects.filter(Q(username__icontains=nombre))
	paginator = Paginator(user,5)
	page = request.GET.get('page')
	user = paginator.get_page(page)
	return render(request,'Busqueda.html',{'user':user})


#************  Mensajes  **********************

class Inbox(View):
	def get(self,request):
		inbox = Canal.objects.filter(canalusuario__usuario__in=[request.user.id])

		context = {

			"inbox":inbox
		}
		return render(request,'mensaje.html',context)



class CanalFormMixin(FormMixin):
	form_class = FormMensajes
	success_url = "./"
	def get_success_url(self):
		return self.request.path

	def post(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			raise PermissionDenied

		form = self.get_form()
		if form.is_valid():
			canal = self.get_object()
			usuario = self.request.user
			mensaje = form.cleaned_data.get("mensaje")
			canal_obj = CanalMensaje.objects.create(canal=canal,usuario=usuario,texto=mensaje)
			
			
			return super().form_valid(form)
		else:
			
			return super().form_invalid(form)
	



class DetailMs(LoginRequiredMixin,CanalFormMixin, DetailView):
 	template_name='mensaje.html'

 	def get_object(self,*args,**kwargs):
 		username = self.kwargs.get("username")
 		mi_username = self.request.user.username
 		canal, _ = Canal.objects.obtener_crear_canal_mensaje(mi_username,username)

 		if username == mi_username:
 			mi_canal, _ = Canal.objects.canal_usuario_actual(self.request.user)
 			return mi_canal

 		if canal == None:
 			raise Http404
 		return canal









# def mensajes_privados(request,username,*args,**kwargs):

# 	if not request.user.is_authenticated:
# 		return HttpResponse("Prohibido")
	
# 	mi_username = request.user.username
# 	canal, created = Canal.objects.obtener_crear_canal_mensaje(mi_username,username) 

# 	if created:
# 		print("Si, fue creado")

# 	usuario = canal.canalusuario_set.all().values("usuario__username")
# 	mensaje = canal.canalmensaje_set.all()

# 	if username == mi_username:
# 		mi_canal= Canal.objects.canal_usuario_actual(request.user)
# 		usuario = username
		
# 	form_class = FormMensajes()
# 	context = {'form_class':form_class}
# 	return render(request,'mensaje.html',{'usuario':usuario,'mensaje':mensaje,'context':context})



# class CanalFormMixin(FormMixin):
# 	form_class = FormMensajes
# 	success_url = "./"


# def post(self, request,*args,**kwargs):

# 		if not request.user.is_authenticated:
# 			raise PermissionDenied

# 		form = self.get_form()
# 		if form.is_valid():
# 			canal = self.get_object()
# 			usuario = self.request.user
# 			mensaje = form.cleaned_data.get("mensaje")
# 			canal_obj = CanalMensaje.object.create(canal=canal,usuario=usuario,texto=texto)













