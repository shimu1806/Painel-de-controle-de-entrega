import requests
from .models import Todo
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):    
    data = Todo.objects.all()    
    return render(request, 'api/index.html', {'data': data})

def fetch_data(request):
    # Fetch 'data' do endpoint
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    queryset_response = response.json()
    aux = []

    for todo in queryset_response:
        obj = Todo(            
            userId=todo['userId'],            
            id=todo['id'],            
            title=todo['title'],            
            completed=todo['completed']        
            )
        aux.append(obj)

    Todo.objects.bulk_create(aux)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return render(request, 'api/index.html')
        else:
            return render(request, 'api/login.html')
    else:
        return render(request, 'api/login.html')
    