from django.http import HttpResponse


def hello_view(request):
    return HttpResponse("Hello, World!")

def personal_greeting(request, name):
    greeting = request.GET.get('greet', 'Hello')  # Default to "Hello" if no 'greet' parameter
    return HttpResponse(f"{greeting}, {name}!")
