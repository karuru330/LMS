from django import forms
from .models import *
  
class CourseForm(forms.ModelForm):
  
    class Meta:
        model = Course
        fields = ['name', 'course_Img']
		
class TrackForm(forms.ModelForm):
  
    class Meta:
        model = Track
        fields = ['name', 'track_Img']
		