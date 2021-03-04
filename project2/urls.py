from django.contrib import admin
from django.urls import path
import jobs.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	
	path('', jobs.views.home,name='home'),
	path('admin/', admin.site.urls),
	path('main/', jobs.views.main,name='main'),
    path('audio/', jobs.views.audio,name='audio'),
	path('video/', jobs.views.video,name='video'),
    path('signup/', jobs.views.signup,name='signup'),
    path('login/', jobs.views.login,name='login'),
    path('logout/', jobs.views.logout,name='logout'),
    path('result/', jobs.views.result,name='result'),
]

if settings.DEBUG:
	urlpatterns==static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)