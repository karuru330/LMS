"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
	path('login',views.login),
	path('home', views.home),
	path('addCourse', views.addCourse),
	path('logout', views.logout),
	path('addTrack', views.addTrack),
	path('tracks/<int:id>', views.viewTrack),
	path('linkCourse/<int:id>', views.linkCourse),
	path('courses/<int:id>', views.viewCourse),
	path('addChapter/<int:id>', views.addChapter),
	path('courses/<int:course_id>/chapters/<int:chapter_id>', views.viewChapter),
	path('addConcept/<int:course_id>/<int:chapter_id>', views.addConcept),
	path('courses/<int:course_id>/chapters/<int:chapter_id>/concepts/<int:concept_id>', views.viewConcept),
	path('editConcept/<int:course_id>/<int:chapter_id>/<int:concept_id>', views.editConcept),
	path('addContent/<int:course_id>/<int:chapter_id>/<int:concept_id>', views.addContent),
	path('viewFullCourse/<int:course_id>', views.viewFullCourse),
	path('viewFullChapter/<int:course_id>/<int:chapter_id>', views.viewFullChapter),
	path('ide', views.ide),
	path('runcode', views.runcode),
	path('save_current_code', views.save_code),
	path('get_current_code', views.get_current_code)
]
