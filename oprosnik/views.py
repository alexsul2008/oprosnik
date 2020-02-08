from django.http import HttpResponse
from django.shortcuts import redirect

def redirect_question(request):
    return redirect('questions', permanent=True)