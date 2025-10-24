from django.shortcuts import render  

def index(request,role):     
	return render(request, 'app2/index.html',{
		"role":role})