from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse('<a href="http://127.0.0.1:8000/blog/">blog</a> <br>  <a '
    #                     'href="http://127.0.0.1:8000/shop">shop</a>')
    return render(request, 'index.html')