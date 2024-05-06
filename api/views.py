from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    response    = requests.get('https://jsonplaceholder.typicode.com/todos')
    data        = response.json()

    return render(request, 'api/index.html', {'data': data[:10] })
    


