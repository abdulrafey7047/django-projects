import os
import json
from pathlib import Path

from django.shortcuts import render
from django.http import FileResponse


def home(request):

    current_path = str(Path(__file__).resolve().parent.parent)
    with open(f'{current_path}/static/core/data/landing_page_data.json') as f:
        context = json.load(f)

    return render(request, 'core/index.html', context=context)


def resume(request):
    filepath = os.path.join('media', "resume.pdf")
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
