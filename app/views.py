from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import *
import subprocess
import os, sys, stat
import json

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect("/home")
	return render(request,'login.html')
	
def login(request):
	if request.method == "GET":
		return redirect('')
	else:
		username = request.POST['username']
		password = request.POST['password']
		
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request,user)
			return redirect("/home")
		else:
			messages.info(request,"Invalid credentials")
			return redirect('/')
			
def home(request):
	if request.user.is_authenticated:
		courses = Course.objects.all()
		tracks = Track.objects.all()
		return render(request, "home.html",{"courses":courses,"tracks":tracks})
	else:
		return redirect("/")
		
def addCourse(request):
	if request.user.is_authenticated:
		if request.method == "GET":
			return render(request, "add_course.html")
		else:
			form = CourseForm(request.POST, request.FILES)
			#print(form.is_valid())
			#print(form)
			if form.is_valid():
				form.save()
				return redirect("/home")
			return HttpResponse(form)
	else:
		return redirect("/")
		
def addTrack(request):
	if request.user.is_authenticated:
		if request.method == "GET":
			return render(request, "add_track.html")
		else:
			form = TrackForm(request.POST, request.FILES)
			#print(form.is_valid())
			#print(form)
			if form.is_valid():
				form.save()
				return redirect("/home")
			return HttpResponse(form)
	else:
		return redirect("/")

def viewTrack(request, id):
	if request.user.is_authenticated:
		if request.method == "GET":
			track = Track.objects.get(id=id)
			track_courses = CourseTrackMapping.objects.filter(track_name=track.name)
			courses = []
			for course in track_courses:
				obj = Course.objects.get(name=course.course_name)
				courses.append(obj)
			#print(courses)
			return render(request, "view_track.html",{"track":track, "courses":courses})
	else:
		return redirect("/")
		
def viewCourse(request, id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=id)
			chapters = Chapter.objects.filter(course_name=course.name)
			return render(request, "view_course.html",{"course":course, "chapters":chapters})
	else:
		return redirect("/")
		
def addChapter(request, id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=id)
			return render(request, "add_chapter.html",{"course":course})
		else:
			chapter_name = request.POST["chapter"]
			course_name = Course.objects.get(id=id).name
			obj = Chapter(course_name=course_name, chapter_name=chapter_name)
			obj.save()
			return redirect("/courses/"+str(id))
	else:
		return redirect("/")
		
def linkCourse(request, id):
	if request.user.is_authenticated:
		if request.method == "GET":
			track = Track.objects.get(id=id)
			courses = Course.objects.all()
			return render(request, "link_course.html",{"courses":courses,"track":track})
		else:
			course_name = request.POST["course"]
			track_name = Track.objects.get(id=id).name
			obj = CourseTrackMapping(course_name=course_name, track_name=track_name)
			obj.save()
			return redirect("/tracks/"+str(id))
	else:
		return redirect("/")
		
def viewChapter(request, course_id, chapter_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=course_id)
			chapter = Chapter.objects.get(id=chapter_id)
			concepts = Concept.objects.filter(course_name=course.name, chapter_name=chapter.chapter_name)
			return render(request, "view_chapter.html",{"course":course, "chapter":chapter, "concepts":concepts})
	else:
		return redirect("/")
		
def addConcept(request, course_id, chapter_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=course_id)
			chapter = Chapter.objects.get(id=chapter_id)
			return render(request, "add_concept.html",{"course":course, "chapter":chapter})
		else:
			concept_name = request.POST["concept_name"]
			content = request.POST["content"]
			course_name = Course.objects.get(id=course_id).name
			chapter_name = Chapter.objects.get(id=chapter_id).chapter_name
			file_path = "C:\\Users\\dilli\\Desktop\\dilli\\Contents\\"+course_name+"_"+chapter_name+"_"+concept_name+".txt"
			f = open(file_path, "w")
			f.write(content)
			f.close()
			obj = Concept(course_name=course_name, chapter_name=chapter_name, concept_name=concept_name, content_file_path=file_path)
			obj.save()
			return redirect("/courses/"+str(course_id)+"/chapters/"+str(chapter_id))
	else:
		return redirect("/")
		
		
def viewConcept(request, course_id, chapter_id, concept_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=course_id)
			chapter = Chapter.objects.get(id=chapter_id)
			concept = Concept.objects.get(id=concept_id)
			file = open(concept.content_file_path, "r")
			content = file.read()
			file.close()
			#print(content)
			return render(request, "view_concept.html",{"course":course, "chapter":chapter, "concept":concept, "content":content})
	else:
		return redirect("/")
		
def editConcept(request, course_id, chapter_id, concept_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=course_id)
			chapter = Chapter.objects.get(id=chapter_id)
			concept = Concept.objects.get(id=concept_id)
			file = open(concept.content_file_path, "r")
			content = file.read()
			file.close()
			return render(request, "edit_concept.html",{"course":course, "chapter":chapter, "concept":concept, "content":content})
		else:
			concept_name = request.POST["concept_name"]
			content = request.POST["contents"]
			course_name = Course.objects.get(id=course_id).name
			chapter_name = Chapter.objects.get(id=chapter_id).chapter_name
			file_path = "C:\\Users\\dilli\\Desktop\\dilli\\Contents\\"+course_name+"_"+chapter_name+"_"+concept_name+".txt"
			f = open(file_path, "w")
			f.write(content)
			f.close()
			return redirect("/courses/"+str(course_id)+"/chapters/"+str(chapter_id))
	else:
		return redirect("/")
		
def addContent(request, course_id, chapter_id, concept_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=course_id)
			chapter = Chapter.objects.get(id=chapter_id)
			concept = Concept.objects.get(id=concept_id)
			file = open(concept.content_file_path, "r")
			content = file.read()
			file.close()
			return render(request, "add_content.html",{"course":course, "chapter":chapter, "concept":concept, "content":content})
		else:
			concept_name = request.POST["concept_name"]
			content = request.POST["contents"]
			course_name = Course.objects.get(id=course_id).name
			chapter_name = Chapter.objects.get(id=chapter_id).chapter_name
			file_path = "C:\\Users\\dilli\\Desktop\\dilli\\Contents\\"+course_name+"_"+chapter_name+"_"+concept_name+".txt"
			f = open(file_path, "r")
			old_content = f.read()
			f.close()
			f = open(file_path, "w")
			content = old_content +"<br>" + content
			f.write(content)
			f.close()
			return redirect("/courses/"+str(course_id)+"/chapters/"+str(chapter_id))
	else:
		return redirect("/")
		
def viewFullCourse(request, course_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=course_id)
			chapters = Chapter.objects.filter(course_name=course.name)
			content = ""
			for chapter in chapters:
				concepts = Concept.objects.filter(chapter_name=chapter.chapter_name, course_name=course.name)
				for concept in concepts:
					file = open(concept.content_file_path, "r")
					content += file.read()
					file.close()
			return render(request, "view_full_course.html",{"course":course, "content":content})
	else:
		return redirect("/")
		
def viewFullChapter(request, course_id, chapter_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			course = Course.objects.get(id=course_id)
			chapter = Chapter.objects.get(id=chapter_id)
			content = ""
			concepts = Concept.objects.filter(chapter_name=chapter.chapter_name, course_name=course.name)
			for concept in concepts:
				file = open(concept.content_file_path, "r")
				content += file.read()
				file.close()
			return render(request, "view_full_chapter.html",{"course":course, "chapter":chapter, "content":content})
	else:
		return redirect("/")
		
def ide(request):
	if request.user.is_authenticated:
		if request.method == "GET":
			try:
				file = open("C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE\\python_code.py", "r")
				code = file.read()
				file.close()
			except Exception as e:
				code = ""
			return render(request, "ide.html", {"code":code})
			
def runcode(request):
	code = request.POST["source"]
	lang = request.POST["lang"]

	input = request.POST["input"]
	file = open("C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE\\input.txt", "w")
	file.write(input)
	file.close()

	if lang == "Python":
		file = open("C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE\\python_code.py", "w")
		file.write(code)
		file.close()
		
		execution_path = "C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE"
		
		fd = open(execution_path+"\\"+"input.txt","r")

		
		command = "python python_code.py"
		proc = subprocess.Popen("cd \""+execution_path+"\" && "+command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

		testcase_input = str(fd.read())
		
		try:
			o, e = proc.communicate(str(testcase_input).encode('utf-8'), timeout=5)
			output = (o.decode('utf-8')).strip("\n")

			result = ""
			if len(e) != 0:
				result = str(e)
			else:
				result = output

		except subprocess.TimeoutExpired or subprocess.CalledProcessError as e:

			result = "Time Limit Exceeded"
			print("*** TIMEOUT, killing process... ***")
			if proc is not None:
					proc.kill()
		except Exception as e:
			result = str(e)
			
		fd.close()
	
	else:

		file = open("C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE\\java_code.java", "w")
		file.write(code)
		file.close()

		command = "javac java_code.java"

		execution_path = "C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE"
		
		fd = open(execution_path+"\\"+"input.txt","r")
			
		proc = subprocess.Popen("cd \""+execution_path+"\" && "+command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

		err = str(proc.stderr.read())

		if "error" in err:

			data = {"compile_status":err}
		
			result = err
		else:

			testcase_input = str(fd.read())

			command = "java Example"
			proc = subprocess.Popen("cd \""+execution_path+"\" && "+command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
			
			try:
				o, e = proc.communicate(str(testcase_input).encode('utf-8'), timeout=5)
				output = (o.decode('utf-8')).strip("\n")

				result = ""
				if len(e) != 0:
					result = str(e)
				else:
					result = output

			except subprocess.TimeoutExpired or subprocess.CalledProcessError as e:

				result = "Time Limit Exceeded"
				print("*** TIMEOUT, killing process... ***")
				if proc is not None:
						proc.kill()
			except Exception as e:
				result = str(e)
				
			fd.close()
	
	result = str(result)
	
	#print(result)
	
	temp = '<div class="row"><div class="col-sm-12">'
	
	temp = temp +"<h5><b>Your Output (stdout)</b></h5>"

	temp = temp +"<pre>"+ result +"</pre>"

	temp = temp + "</div>"
	
	data = {"compile_status":"OK","result":temp}

	data = json.dumps(data)


	return HttpResponse(data, content_type="application/json")

def save_code(request):
	code = request.POST["code"]
	lang = request.POST["lang"]
	filename = ""
	if lang == "Java":
		filename = "java_code.java"
	else:
		filename = "python_code.py"
	file = open("C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE\\"+filename, "w")
	file.write(code)
	file.close()
	#print("saving code\n"+code)
	
	return HttpResponse("Saved")

def get_current_code(request):
	lang = request.POST["lang"]
	print(lang)
	if lang == "Java":
		filename = "java_code.java"
	else:
		filename = "python_code.py"
	
	try:
		file = open("C:\\Users\\dilli\\Desktop\\dilli\\Code\\IDE\\"+filename, "r")
		code = file.read()
		file.close()
	except Exception as e:
		print(e)
		code = ""
	#print("saving code\n"+code)
	
	print(code)
	return HttpResponse(code, content_type="application/json")
	
def logout(request):
	auth.logout(request)
	return redirect('/')