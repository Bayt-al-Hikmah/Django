from django.shortcuts import render  

def index(request):     
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry', 'Mango', 'Orange']
    }
    return render(request, 'app3/index.html', context)