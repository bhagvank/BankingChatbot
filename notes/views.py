from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, render

from django.template import loader
from django.http import HttpResponse
from .models import AIRecruiterUser
from .models import Resume
#from .models import Note
from django.views import generic
#from .forms import NoteForm 
import os
import logging
import base64

# Create your views here.
class IndexView(generic.ListView):
   #model = Note  
   template_name = 'notes/index.html'
   
   def get_queryset(self):
    notes = Note.objects
    return notes; 


logger = logging.getLogger("ai_recruiter_logger")

def login(request):
    """
    login page call

    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """

    template_name = 'notes/login.html'
    return render(request, template_name)
def logout(request):
    """
    logout page call

    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """
    template_name = 'notes/login.html'

    return render(request, template_name)    


def home(request):
    #notes = Note.objects
    #template = loader.get_template('notes/main_job.html')
    #form = NoteForm(request.POST or None)
    #if form.is_valid():
    #    save_it = form.save(commit=False)
    #    save_it.save() 
    context = {}
    return render(request, 'notes/index.html', context) 

def main(request):
    #notes = Note.objects
    #template = loader.get_template('main.html')
    #form = ProfileForm(request.POST or None)
    #if form.is_valid():
    #    save_it = form.save(commit=False)
    #    save_it.save() 
    #context = {'notes': notes,'form': form}
    print(request.session['user_token'])
    try:
       profile = get_object_or_404(Profile, id= request.session['user_token'])
    
       print(profile.fname)
       context = {'first_name':profile.fname,
                  'last_name': profile.lname,
                  'country': profile.country,
                  'picture': profile.picture}
       return render(request, 'notes/main.html', context)

    except Exception as exception:
       context ={}
       return render(request, 'notes/main.html', context)

def resume(request):
    #notes = Note.objects
    #template = loader.get_template('upload_profile.html')
    #form = ProfileForm(request.POST or None)
    #if form.is_valid():
    #    save_it = form.save(commit=False)
    #    save_it.save() 
    #context = {'notes': notes,'form': form}
    
    context ={}
    return render(request, 'notes/upload_profile.html', context)

def signup(request):
    """
    sign up page call
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """

    template_name = 'notes/register.html'
    #context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name)  

def register(request):
    """
    sign in - sign up processing
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """
    username = request.POST['useremail']
    password = request.POST['password']
    confirmPassword = request.POST['confirmPassword']
    print("password, confirmPassword",password,confirmPassword)

 
    error_confirm_password = None
    error_username = None
    error_password = None
     #template_name = 'nlp/signup.html'

    error_username = _validate_username(username)
    error_password, error_confirm_password = _validate_password(password,confirmPassword)
       
    if error_username == None and error_password == None and error_confirm_password == None:
       if password == confirmPassword:
               #print("password is equal to confirmPassword") 
          user = AIRecruiterUser(username=username,password=password)
          user.save()

          template_name = 'notes/login.html'
       else :
               #error_confirm_password = "password and confirm password do not match"
          template_name = 'notes/register.html'
    else : 
          template_name = 'notes/register.html'     
      
    context = {'error_confirm_password': error_confirm_password,
                'error_useremail': error_username,
                'error_password': error_password
                }
    return render(request, template_name,context)


def authenticate(request):
    """
    page authentication
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """

    print("authenticating")
    username = request.POST['useremail']
    password = request.POST['password']

    
 
    logger.info("authenticate username "+username )

    error_password = None
    try:
       user = get_object_or_404(AIRecruiterUser, username=username)
    except Exception as exception:
        print(str(exception))
        template_name = 'notes/login.html'
        error_username = "Invalid username"
        context = {'error_useremail': error_username,
                'error_password': error_password}
        return render(request, template_name,context)   

    if user:
       check, error_username, error_password = user.authenticate(username, password)
       print(check,error_username,error_password)
       if check:
              request.session["user_token"] = user.id
              template_name = 'notes/index.html'
              logger.info("authenticated username "+username)
       else :
           print("setting template as login") 
           template_name = 'notes/login.html'
           logger.info("authenticate failure username "+username )
    else :
        print("setting template as login")
        template_name = 'notes/login.html'
        error_username = "Invalid username"
        logger.info("validation failure username "+username )
        
    context = {'error_useremail': error_username,
                'error_password': error_password}
    
    return render(request, template_name,context)    



def _validate_username(username):
    error_username = None    
    if username == None:
       error_username = "user email is blank"
        
    if "@" not in username or "." not in username :
       error_username = "user email is not valid"         
    return error_username



def _validate_password(password,confirm_password):
    error_password = None
    error_confirm_password = None
    if password == None:
       error_password = "password is blank"
    if confirm_password == None:
       error_confirm_password = "confirm password is blank"
    if password != None and confirm_password != None:
       if password == confirm_password:
          error_password = None
          error_confirm_password = None
       else :
          error_password = "password and confirm_password do not match"
          error_confirm_password = "password and confirm_password do not match"   
    return error_password, error_confirm_password 


from .forms import ProfileForm
from .models import Profile

def SaveProfile(request):
       
   saved = False
   
   if request.method == "POST":
      #Get the posted form
      MyProfileForm = ProfileForm(request.POST, request.FILES)
      print("this profile form is ",MyProfileForm.is_valid())
      if MyProfileForm.is_valid():
         profile = Profile()
         profile.fname = MyProfileForm.cleaned_data["fname"] 
         profile.lname = MyProfileForm.cleaned_data["lname"] 
         profile.country = MyProfileForm.cleaned_data["country"] 
         profile.picture = MyProfileForm.cleaned_data["picture"]
         print(request.session['user_token'] )
         user = get_object_or_404(AIRecruiterUser, id=int(request.session['user_token']))
         profile.userid = user 
         try:    
            profile.save()
            print("saving")
            saved = True
         except Exception as exception:
            print(str(exception))
      else:
        print("form is not valid")
        print(MyProfileForm.errors.as_text()) 
   else:
      MyProfileForm = Profileform()
        
   if saved:
      print("picture saved")
   else:
      print("Error in saving")
   #notes = Note.objects
   #template = loader.get_template('index.html')
   #form = NoteForm(request.POST or None)
   #if form.is_valid():
   #        save_it = form.save(commit=False)
   #        save_it.save() 
   #context = {'notes': notes,'form': form}
   context = {}
		
   return render(request, 'notes/index.html', context)



from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .parseprofile import Parse   

def UploadProfile(request):
        if request.method == 'POST':
            myfile = request.FILES['dbfile']
            print(myfile)
            fs = FileSystemStorage()
            filename = fs.save("documents/"+myfile.name, myfile)
            print(filename)
            uploaded_file_url = fs.url(filename)
            resume = Resume( )
            resume.resume = uploaded_file_url
            user = get_object_or_404(AIRecruiterUser, id=int(request.session['user_token']))
            resume.userid = user
            resume.save()
            Parse(filename)
            return render(request, 'notes/main_job.html', {
            'uploaded_file_url': uploaded_file_url
        })
        return render(request, 'notes/main_job.html')
