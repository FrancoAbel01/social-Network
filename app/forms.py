from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Profile,Post, Comentario


#formulario de registro usando el user
class UserRegisterForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['username','password1','password2']



class PostForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100',
				'id':'contentsBox','rows':'1','placeholder':'Escribe tu idea '}))

	

	def __init__(self,*args,**kwargs):
		super(self.__class__,self).__init__(*args,**kwargs)
		self.fields['image'].required = True



	def __init__(self,*args,**kwargs):
		super(self.__class__,self).__init__(*args,**kwargs)
		self.fields['content'].required = False
		
	class Meta:
		model = Post
		fields = ['content','image']




# comentarios ************************************************************************************

class ComentsForm(forms.ModelForm):
	contenido = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100',
				'id':'contentsBox','rows':'3','placeholder':'Escribe tu comentario '}))


	def __init__(self,*args,**kwargs):
		super(self.__class__,self).__init__(*args,**kwargs)
		self.fields['contenido'].required = True
		
	class Meta:
		model = Comentario
		fields = ['contenido']




#para editar el perfil trabajamos con el user y despues con el profile
class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username']




class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['bio','telefono','image','pais','city']



class FormMensajes(forms.Form):
	mensaje = forms.CharField(widget = forms.Textarea(attrs={
		'class':'form-control w-100',
				'rows':'1','placeholder':'Escribe tu Mensaje '
	}))
