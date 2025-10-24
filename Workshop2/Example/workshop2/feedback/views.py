from django.shortcuts import render, redirect
from .forms import FeedbackForm
from django.urls import reverse
feedbacks = []
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedbacks.append(form.cleaned_data)
            return redirect(reverse('feedbacks'))
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/form.html', {'form': form})

def feedback_list(request):
    return render(request, 'feedback/feedbacks.html', {'feedback_list': feedbacks})