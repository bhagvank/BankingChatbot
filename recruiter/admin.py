from django.contrib import admin
 
# Register your models here.
#from .models import Note
from .models import RProfile
from .models import AIRecruiter
 
class AIRecruiterAdmin(admin.ModelAdmin):
    class Meta:
        model = AIRecruiter
        
class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = RProfile
 
admin.site.register(AIRecruiter,AIRecruiterAdmin)
admin.site.register(RProfile,ProfileAdmin)
