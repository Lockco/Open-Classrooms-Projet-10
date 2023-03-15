from rest_framework import serializers
from django.contrib.auth import get_user_model

# Obtient le modèle User configuré dans les paramètres
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	# En spécifiant que le champ password ne peut être lu que lorsqu'il est écrit, cela le rend accessible uniquement
	# lors de la création et de la modification d'un utilisateur.
	password = serializers.CharField(write_only=True)

	# La méthode create est appelée lorsque l'API doit créer une instance de User à partir des données validées
	def create(self, validated_data):
		# Crée un utilisateur en utilisant la méthode create_user fournie par le modèle User.
		# L'attribut password est crypté lorsqu'il est stocké dans la base de données.
		user = User.objects.create_user(
			username=validated_data['username'],
			email=validated_data['email'],
			password=validated_data['password']
		)
		return user

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError("Cette adresse e-mail est déjà associée à un compte existant.")
		return value

	# La classe Meta spécifie les champs de User qui doivent être inclus dans la sérialisation.
	# Dans ce cas, les champs id, username, email et password sont inclus.
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'password')
