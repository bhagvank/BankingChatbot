from django import forms
#from .models import Note
 
#class NoteForm(forms.ModelForm):
#    class Meta:
#        model = Note
#        fields = '__all__'
        
class ProfileForm(forms.Form):
   fname = forms.CharField(max_length = 100)
   lname = forms.CharField(max_length = 100)
   country = forms.CharField(max_length = 100)    
   picture = forms.ImageField()
