from django.db import models  

class Photo(models.Model):     
	title = models.CharField(max_length=100)     
	image = models.ImageField(upload_to='uploads/')     
	uploaded_at = models.DateTimeField(auto_now_add=True)   
	   
	def __str__(self):         
		return self.title