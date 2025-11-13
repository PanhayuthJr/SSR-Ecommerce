from django.http import HttpResponse
from django.shortcuts import render
from django.utils.text import re_newlines


# Create your views here.py

def home(request):
    data = {"name":"Coca"}
    return render(request, template_name='index.html', context=data)
def find_by_id(request, id):
    return HttpResponse(f"id{id }")
def content(request):
    return render(request, "pages/content.html")