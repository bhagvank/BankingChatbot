from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from todo import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/',include('notes.urls')),
    path('recruiter/',include('recruiter.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
