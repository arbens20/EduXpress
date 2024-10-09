from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Enseignant, Tuteur, Entreprise, Etudiant

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'numero', 'password1', 'password2']

class EnseignantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['bio']

class TuteurRegistrationForm(forms.ModelForm):
    class Meta:
        model = Tuteur
        fields = []

class EntrepriseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['bio']

class EtudiantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['etudiant_type', 'enrolled_by_tuteur']
