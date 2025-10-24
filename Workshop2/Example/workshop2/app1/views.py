from django.shortcuts import render

def index(request):
    context = {
        'username': 'Alice',
        'age': 25
    }
    return render(request, 'app1/index.html', context)