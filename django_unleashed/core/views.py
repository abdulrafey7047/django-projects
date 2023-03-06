import os
from django.http import FileResponse, HttpResponse


def home(request):
    return HttpResponse('This is Home page')


def resume(request):
    filepath = os.path.join('media', "resume.pdf")
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
