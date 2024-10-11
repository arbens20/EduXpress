from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from django.core.mail import send_mail

class UserManager(BaseUserManager):
    def create_user(self, email, prenom, nom, password=None, **extra_fields):
        if not email:
            raise ValueError("L'e-mail doit être renseigné")
        email = self.normalize_email(email)
        user = self.model(email=email, prenom=prenom, nom=nom, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, prenom, nom, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, prenom, nom, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    numero = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # L'email est utilisé comme champ d'authentification principal
    REQUIRED_FIELDS = ['prenom', 'nom']  # Pas besoin de username

    groups = models.ManyToManyField(Group, related_name='utilisateur_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='utilisateur_permissions', blank=True)

    def __str__(self):
        return f'{self.prenom} {self.nom}'

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_role(self):
        """Retourne le rôle en fonction du modèle associé"""
        if hasattr(self, 'enseignant'):
            return 'Enseignant'
        elif hasattr(self, 'tuteur'):
            return 'Tuteur'
        elif hasattr(self, 'etudiant'):
            return 'Etudiant'
        elif hasattr(self, 'entreprise'):
            return 'Entreprise'
        return 'Utilisateur'  # Valeur par défaut si aucun rôle spécifique


##############################################################################################################
############################################## MODELE ENSEIGNANT #############################################

class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enseignant')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Enseignant: {self.user.prenom} {self.user.nom}'

##############################################################################################################
############################################## MODELE TUTEUR #################################################

class Tuteur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tuteur')

    def __str__(self):
        return f'Tuteur: {self.user.prenom} {self.user.nom}'

##############################################################################################################
############################################## MODELE ETUDIANT ###############################################

class Etudiant(models.Model):
    ETUDIANT_TYPE_CHOICES = [
        ('classic', 'Classique'),
        ('university', 'Universitaire'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='etudiant')
    etudiant_type = models.CharField(max_length=15, choices=ETUDIANT_TYPE_CHOICES)
    enrolled_by_tuteur = models.ForeignKey(Tuteur, on_delete=models.SET_NULL, null=True, blank=True) 
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f'Etudiant: {self.user.prenom} {self.user.nom}'

##############################################################################################################
############################################## MODELE ENTREPRISE #############################################

class Entreprise(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='entreprise')
    bio = models.TextField(blank=True)
    supervised_etudiants = models.ManyToManyField('Etudiant', limit_choices_to={'etudiant_type': 'university'}, blank=True)

    def __str__(self):
        return f'Entreprise: {self.user.nom}'

##############################################################################################################
############################################## MODELE COURSE #################################################


    
    
    
    

# Modèle pour les cours
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    students = models.ManyToManyField(Etudiant, through='Enrollment')

    def __str__(self):
        return self.title

# Modèle intermédiaire pour les inscriptions aux cours
class Enrollment(models.Model):
    student = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.prenom} - {self.course.title}'


class Chapitre(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    # student = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    nom_chapitre = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    
    
class Video(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    titre = models.CharField(max_length=500)
    contenu = models.FileField(upload_to='videos/')  
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Audio(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    titre = models.CharField(max_length=500)
    contenu = models.FileField(upload_to='audios/')  
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Texte(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    titre = models.CharField(max_length=500)
    contenu = models.TextField()  
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    




#######################################################################################################



class Quiz(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.IntegerField(default=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
