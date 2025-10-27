from django.shortcuts import render, redirect 
from .models import Photo 
from .forms import PhotoForm 
from django.urls import reverse  

def gallery(request):     
	photos = Photo.objects.all().order_by('-uploaded_at')     
	return render(request, 'image_share/gallery.html', {'photos': photos})  

def upload_photo(request):     
	if request.method == 'POST':         
		form = PhotoForm(request.POST, request.FILES)         
		if form.is_valid():             
			form.save()             
			return redirect(reverse('gallery'))     
	else:         
		form = PhotoForm()     
	return render(request, 'image_share/upload.html', {'form': form})