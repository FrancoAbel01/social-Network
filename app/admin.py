from django.contrib import admin
from .models import Profile,Post,Relationship,Comentario,CanalMensaje, CanalUsuario, Canal

# Register your models here.

class CanalMensajeInline(admin.TabularInline):
    model = CanalMensaje
    extra = 1

class CanalUsuarioInline(admin.TabularInline):
    model = CanalUsuario
    extra = 1

class CanalAdmin(admin.ModelAdmin):
    inlines = [CanalMensajeInline,CanalUsuarioInline]

    class Meta:
        model = Canal




admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Relationship)
admin.site.register(Comentario)
admin.site.register(CanalMensaje)
admin.site.register(CanalUsuario)
admin.site.register(Canal,CanalAdmin)






