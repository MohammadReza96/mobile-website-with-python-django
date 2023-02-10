from django.shortcuts import render
from django.conf import settings

# for loading media anywhere & each time
#------------------------------------------
def media_admin(request):
    return {'media_url':settings.MEDIA_URL}