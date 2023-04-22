from django.db import models
from users.models import User


# Create your models here.
class Project(models.Model):
	TYPE_CHOICES = (
		('BACK_END', 'Backend'),
		('FRONT_END', 'Frontend'),
		('fullstack', 'Full Stack'),
		('IOS', "iOS"),
		('ANDROID', "Android"),
		
	)

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	# Champ pour l'auteur du projet, avec une relation ForeignKey vers le modèle User
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Projet'
		verbose_name_plural = 'Tous les projets'


class Issue(models.Model):
	PRIORITY_CHOICES = (
		('low', 'Low'),
		('medium', 'Medium'),
		('high', 'High'),
	)
	STATUS_CHOICES = (
		('open', 'Open'),
		('in_progress', 'In Progress'),
		('closed', 'Closed'),
	)

	TAG_CHOICES = (
		('bug', 'Bug'),
		('task', 'Task'),
		('improvement', 'Improvement'),
	)

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
	project = models.ForeignKey(Project, on_delete=models.CASCADE) # Projet auquel le problème est associé
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_issues')
	assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_issues', null=True, blank=True) # Personne assignée pour résoudre le problème
	created_time = models.DateTimeField(auto_now_add=True)
	tags = models.CharField(max_length=100, blank=True) # Tags associés au problème

	class Meta:
		verbose_name = 'Problème'
		verbose_name_plural = 'Tous les problèmes'


class Comment(models.Model):
	description = models.CharField(max_length=500)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Commentaire'
		verbose_name_plural = 'Tous les commentaires'

	def __str__(self):
		return self.description


class Contributor(models.Model):
	PERMISSION_CHOICES = (
		('read', 'Read'),
		('write', 'Write'),
		('admin', 'Admin'),
	)
	ROLE_CHOICES = (
		('developer', 'Developer'),
		('tester', 'Tester'),
		('manager', 'Manager'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
	permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES)

	class Meta:
		verbose_name = 'Contributeur'
		verbose_name_plural = 'Tous les contributeurs'