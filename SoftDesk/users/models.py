from django.contrib.auth.models import AbstractUser
from django.db import models


# On définit le modèle User qui hérite de la classe AbstractUser de Django
class User(AbstractUser):
	email = models.EmailField(unique=True)  # Le champ email est un champ unique

	# related_name personnalisé pour éviter les conflits
	groups = models.ManyToManyField(
		'auth.Group',  # On définit la relation avec la classe Group de Django
		verbose_name='groupes',
		blank=True,
		help_text='Les groupes auxquels l\'utilisateur appartient.',
		related_name='custom_user_set',
		related_query_name='custom_user'
	)

	user_permissions = models.ManyToManyField(
		'auth.Permission',  # On définit la relation avec la classe Permission de Django
		verbose_name='permissions',
		blank=True,
		help_text='Les permissions de l\'utilisateur.',
		related_name='custom_user_set',
		related_query_name='custom_user'
	)

	class Meta:
		verbose_name = 'Utilisateur'  # Nom au singulier pour les objets de ce modèle
		verbose_name_plural = 'Tous les utilisateurs'  # Nom au pluriel pour les objets de ce modèle
