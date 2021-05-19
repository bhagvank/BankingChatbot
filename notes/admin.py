from django.contrib import admin
 
# Register your models here.
#from .models import Note
from .models import Profile
 
#class NoteAdmin(admin.ModelAdmin):
#    class Meta:
#        model = Note
        
class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
 
#admin.site.register(Note,NoteAdmin)
admin.site.register(Profile,ProfileAdmin)
