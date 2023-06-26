from django.db import models

# Create your models here.
class Course(models.Model):
	name = models.CharField(max_length=50)
	course_Img = models.ImageField(upload_to='images')
	
class Track(models.Model):
	name = models.CharField(max_length=50)
	track_Img = models.ImageField(upload_to='images')
	
class CourseTrackMapping(models.Model):
	course_name = models.CharField(max_length=50)
	track_name = models.CharField(max_length=50)
	
class Chapter(models.Model):
	chapter_name = models.CharField(max_length=50)
	course_name = models.CharField(max_length=50)
	
class Concept(models.Model):
	chapter_name = models.CharField(max_length=50)
	course_name = models.CharField(max_length=50)
	concept_name = models.CharField(max_length=5000)
	content_file_path =  models.CharField(max_length=5000)

class Problem(models.Model):
	problem_name = models.CharField(max_length=500)
	chapter_name = models.CharField(max_length=50)
	course_name = models.CharField(max_length=50)
	content_file_path =  models.CharField(max_length=5000)