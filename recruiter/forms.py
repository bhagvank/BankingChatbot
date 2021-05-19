from django import forms
 

        
class ProfileForm(forms.Form):
   fname = forms.CharField(max_length = 100)
   lname = forms.CharField(max_length = 100)
   country = forms.CharField(max_length = 100)    
   picture = forms.ImageField()
