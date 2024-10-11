from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login

from EduXplore import settings
from .forms import UserRegistrationForm, EnseignantRegistrationForm, TuteurRegistrationForm, EntrepriseRegistrationForm, EtudiantRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from utilisateurs.models import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.http import Http404
from socket import gaierror
from ssl import SSLEOFError
from .tokens import generateToken
from django.core.mail import send_mail, EmailMessage
from . tokens import generateToken
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from utilisateurs.models import *
from django.http import HttpResponse
from .models import Course, Enrollment, Chapitre, Video, Audio, Texte, Etudiant, Enseignant



def home(request):
    return render(request, 'home.html')


# def dashboard_enseignant(request):
#     user = request.user
#     if hasattr(user, 'enseignant'):
#         # C'est un enseignant
#         context = {'role': 'Enseignant', 'user_info': user.enseignant}
#     else:
#         context = {'role': 'Utilisateur inconnu'}
#     return render(request, 'Enseignant/dashboard_enseignant.html', context)


def dashboard_enseignant(request):
    user = request.user
    if hasattr(user, 'enseignant'):
        # Récupérer les cours et chapitres créés par l'enseignant
        cours = Course.objects.filter(teacher=user.enseignant)
        chapitres = Chapitre.objects.filter(cours__teacher=user.enseignant)

        context = {
            'role': 'Enseignant',
            'user_info': user.enseignant,
            'cours': cours,
            'chapitres': chapitres,
        }
    else:
        context = {'role': 'Utilisateur inconnu'}

    return render(request, 'Enseignant/dashboard_enseignant.html', context)


def register_enseignant(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        enseignant_form = EnseignantRegistrationForm(request.POST)
        if user_form.is_valid() and enseignant_form.is_valid():
            user = user_form.save(commit=False)
            user.is_staff = True  # Facultatif pour accorder des privilèges d'accès
            user.save()
            enseignant = enseignant_form.save(commit=False)
            enseignant.user = user
            enseignant.save()
            login(request, user)
            return redirect('dashboard_enseignant')  # Rediriger vers une page après l'inscription
    else:
        user_form = UserRegistrationForm()
        enseignant_form = EnseignantRegistrationForm()

    return render(request, 'register_enseignant.html', {'user_form': user_form, 'enseignant_form': enseignant_form})

def register_tuteur(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        tuteur_form = TuteurRegistrationForm(request.POST)
        if user_form.is_valid() and tuteur_form.is_valid():
            user = user_form.save()
            tuteur = tuteur_form.save(commit=False)
            tuteur.user = user
            tuteur.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = UserRegistrationForm()
        tuteur_form = TuteurRegistrationForm()

    return render(request, 'register_tuteur.html', {'user_form': user_form, 'tuteur_form': tuteur_form})


# Vue pour enregistrer un étudiant
def register_etudiant(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        etudiant_form = EtudiantRegistrationForm(request.POST)
        if user_form.is_valid() and etudiant_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # L'utilisateur doit activer son compte
            user.set_password(user_form.cleaned_data['password2'])  # Hachage du mot de passe
            user.save()

            etudiant = etudiant_form.save(commit=False)
            etudiant.user = user
            etudiant.save()

            messages.add_message(request, messages.SUCCESS, 'Votre compte a été créé avec succès. Un e-mail de confirmation vous a été envoyé.')

            # Envoyer un seul email de bienvenue
            subject = "Bienvenue sur EduXplore"
            message = f"Bienvenue {user.prenom} {user.nom},\nMerci d'avoir choisi notre plateforme.\nPour vous connecter, veuillez confirmer votre adresse e-mail.\nCordialement,\nL'équipe EduXplore"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]

            try:
                send_mail(subject, message, from_email, to_list, fail_silently=False)

                # Envoi de l'email d'activation
                current_site = get_current_site(request)
                email_subject = "Confirmez votre adresse e-mail pour EduXplore"
                message_confirm = render_to_string("activation_email.html", {
                    'name': user.prenom,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generateToken.make_token(user)
                })
                
                # Envoyer l'email d'activation
                email = EmailMessage(
                    email_subject,
                    message_confirm,
                    from_email,
                    to_list
                )
                email.fail_silently = False
                email.send()

                # Redirection après succès
                return render(request, 'login.html', {'messages': messages.get_messages(request)})

            except (gaierror, SSLEOFError) as e:
                # Gérer l'erreur de connexion Internet ici
                messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'envoi des e-mails. Veuillez vérifier votre connexion Internet.")
                return render(request, '404.html')

    else:
        user_form = UserRegistrationForm()
        etudiant_form = EtudiantRegistrationForm()

    return render(request, 'register_etudiant.html', {'user_form': user_form, 'etudiant_form': etudiant_form})





def home_etudiant(request):
    user = request.user
    if hasattr(user, 'etudiant'):
        # C'est un enseignant
        context = {'role': 'Etudiant', 'user_info': user.etudiant}
    else:
        context = {'role': 'Utilisateur inconnu'}
    return render(request, 'home_etudiant.html', context)













# Vue d'activation du compte


def activate(request, uidb64, token):
    if request.method != 'GET':
        return HttpResponse("Méthode non autorisée.", status=405)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Votre compte a été activé avec succès.')
        return redirect('login_view')  # Change en 'login_view' si nécessaire
    else:
        messages.add_message(request, messages.ERROR, 'Le lien d\'activation est invalide.')
        return redirect('login_view')  # Change en 'login_view' si nécessaire


# Vue pour la connexion


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"DEBUG: email = {email}, password = {password}")

        user = None

        # Chercher l'utilisateur par email
        try:
            print(f"DEBUG: Tentative de recherche par email: {email}")
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print(f"DEBUG: Aucun utilisateur trouvé avec cet email: {email}")
            user = None

        if user is not None:
            print(f"DEBUG: Utilisateur trouvé: {user.email}, tentative d'authentification...")
            # On utilise authenticate pour vérifier le mot de passe
            user = authenticate(request, email=email, password=password)
            print(f"DEBUG: Résultat de l'authentification: {user}")
        else:
            print("DEBUG: Utilisateur non trouvé, impossible de procéder à l'authentification.")

        if user is not None:
            if user.is_active:
                print(f"DEBUG: Utilisateur {user.email} est actif, connexion...")
                login(request, user)
                return redirect('index')  # Redirection après connexion réussie
            else:
                print("DEBUG: Utilisateur trouvé, mais compte inactif.")
                messages.error(request, 'Vous devez confirmer votre e-mail pour activer votre compte.')
                return render(request, 'login.html', {'messages': messages.get_messages(request)})
        else:
            print("DEBUG: Authentification échouée, identifiants invalides.")
            messages.error(request, "Identifiants invalides. Veuillez vérifier vos informations.")
            return render(request, 'login.html', {'messages': messages.get_messages(request)})

    return render(request, 'login.html')

# def login_view(request):
#     user = authenticate(request, email='carlobeddorvil20@gmail.com', password='Arian237')

#     if user is not None:
#         # Connexion réussie
#         login(request, user)
#         return redirect('index')
#     else:
#         # Échec de la connexion
#         messages.error(request, "Identifiants invalides. Veuillez vérifier vos informations.")
#         return render(request, 'login.html', {'messages': messages.get_messages(request)})


def index(request):
    user = request.user
    if hasattr(user, 'enseignant'):
        # C'est un enseignant
        context = {'role': 'Enseignant', 'user_info': user.enseignant}
    elif hasattr(user, 'tuteur'):
        # C'est un tuteur
        context = {'role': 'Tuteur', 'user_info': user.tuteur}
    elif hasattr(user, 'entreprise'):
        # C'est une entreprise
        context = {'role': 'Entreprise', 'user_info': user.entreprise}
    elif hasattr(user, 'etudiant'):
        # C'est un étudiant
        context = {'role': 'Etudiant', 'user_info': user.etudiant}
    else:
        context = {'role': 'Utilisateur inconnu'}

    return render(request, 'index.html', context)

def logout_view(request):
    logout(request) 
    return redirect('login_view')  








# Partie View Concernant les Enseignant##########################################################################################




@login_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        teacher = request.user.enseignant 
        
        Course.objects.create(title=title, description=description, teacher=teacher)
        return redirect('course_list')  
    
    return render(request, 'Enseignant/create_course.html')

@login_required
def course_list(request):
    courses = Course.objects.filter(teacher=request.user.enseignant)
    return render(request, 'Enseignant/course_list.html', {'courses': courses})

@login_required
def create_chapitre(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        nom_chapitre = request.POST.get('nom_chapitre')
        description = request.POST.get('description')
        
        Chapitre.objects.create(cours=course, nom_chapitre=nom_chapitre, description=description)
        return redirect('chapter_list', course_id=course.id)  # Rediriger vers la liste des chapitres
    
    return render(request, 'Enseignant/create_chapitre.html', {'course': course})

@login_required
def chapter_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapitres = Chapitre.objects.filter(cours=course)
    return render(request, 'Enseignant/chapter_list.html', {'chapitres': chapitres, 'course': course})

@login_required
def create_video(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.FILES.get('contenu')
        
        Video.objects.create(chapitre=chapitre, titre=titre, contenu=contenu)
        return redirect('chapter_list', course_id=chapitre.cours.id)
    
    return render(request, 'Enseignant/create_video.html', {'chapitre': chapitre})

@login_required
def create_audio(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.FILES.get('contenu')
        
        Audio.objects.create(chapitre=chapitre, titre=titre, contenu=contenu)
        return redirect('chapter_list', course_id=chapitre.cours.id)
    
    return render(request, 'Enseignant/create_audio.html', {'chapitre': chapitre})

@login_required
def create_texte(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        
        Texte.objects.create(chapitre=chapitre, titre=titre, contenu=contenu)
        return redirect('chapter_list', course_id=chapitre.cours.id)
    
    return render(request, 'Enseignant/create_texte.html', {'chapitre': chapitre})

@login_required
def create_quiz(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        quiz = Quiz.objects.create(chapitre=chapitre, title=title, teacher=request.user.enseignant)
        return redirect('create_question', quiz_id=quiz.id)
    
    return render(request, 'Enseignant/create_quiz.html', {'chapitre': chapitre})

@login_required
def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        points = request.POST.get('points')
        question = Question.objects.create(quiz=quiz, text=text, points=points)
        
        # Ajouter les choix
        for i in range(int(request.POST.get('num_choices', 0))):
            choice_text = request.POST.get(f'choice_text_{i}')
            is_correct = request.POST.get(f'is_correct_{i}') == 'on'
            Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
        
        return redirect('chapter_list', course_id=quiz.chapitre.cours.id)
    
    return render(request, 'Enseignant/create_question.html', {'quiz': quiz})

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(teacher=request.user.enseignant)
    return render(request, 'Enseignant/quiz_list.html', {'quizzes': quizzes})



@login_required
def chapitre_detail(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    videos = Video.objects.filter(chapitre=chapitre)
    audios = Audio.objects.filter(chapitre=chapitre)
    textes = Texte.objects.filter(chapitre=chapitre)
    quizzes = Quiz.objects.filter(chapitre=chapitre)

    context = {
        'chapitre': chapitre,
        'videos': videos,
        'audios': audios,
        'textes': textes,
        'quizzes': quizzes,
    }
    
    return render(request, 'Enseignant/chapitre_detail.html', context)



def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'Enseignant/quiz_detail.html', context)





def chapitre_detail_global(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    videos = chapitre.video_set.order_by('date_added')  
    audios = chapitre.audio_set.order_by('date_added')
    textes = chapitre.texte_set.order_by('date_added')

    context = {
        'chapitre': chapitre,
        'videos': videos,
        'audios': audios,
        'textes': textes,
    }
    return render(request, 'Enseignant/chapitre_detail_global.html', context)







# Fin Partie View Concernant les Enseignant##########################################################################################









# Debut Partie View Concernant les Enseignant##########################################################################################




# @login_required
# def available_courses_student(request):
#     """Afficher les cours disponibles pour l'étudiant."""
#     user = request.user
#     if hasattr(user, 'etudiant'):
#         courses = Course.objects.all()  # Tous les cours disponibles
#         return render(request, 'Etudiant/available_courses.html', {'courses': courses})
#     return redirect('login')


@login_required
def available_courses(request):
    etudiant = request.user.etudiant

    # Cours auxquels l'étudiant n'est pas encore inscrit
    available_courses = Course.objects.exclude(students=etudiant)

    return render(request, 'Etudiant/available_courses.html', {
        'available_courses': available_courses,
    })

    
@login_required   
def enrolled_courses(request):
    etudiant = request.user.etudiant

    # Cours auxquels l'étudiant est dja inscrit
    enrolled_courses = Course.objects.filter(students=etudiant)

    return render(request, 'Etudiant/enrolled_courses.html', {
        'enrolled_courses': enrolled_courses,
    })

def enroll_in_course(request, course_id):
    etudiant = request.user.etudiant
    course = get_object_or_404(Course, id=course_id)
    
    # Ajouter l'étudiant au cours sil pa inscrit
    if etudiant not in course.students.all():
        course.students.add(etudiant)

    return redirect('enrolled_courses')




@login_required
def enroll_in_course_student(request, course_id):
    """Inscrire un étudiant dans un cours."""
    user = request.user
    student = user.etudiant
    course = get_object_or_404(Course, id=course_id)

    # Créer une inscription
    Enrollment.objects.get_or_create(student=student, course=course)
    return redirect('student_courses')

@login_required
def student_courses_student(request):
    """Afficher les cours auxquels l'étudiant est inscrit."""
    user = request.user
    if hasattr(user, 'etudiant'):
        courses = Enrollment.objects.filter(student=user.etudiant)
        return render(request, 'Etudiant/student_courses.html', {'courses': courses})
    return redirect('login')

@login_required
def course_chapters_student(request, course_id):
    """Afficher les chapitres d'un cours spécifique."""
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if hasattr(user, 'etudiant'):
        chapters = Chapitre.objects.filter(cours=course)
        return render(request, 'Etudiant/course_chapters.html', {'chapters': chapters, 'course': course})
    return redirect('login')

@login_required
def chapter_details_student(request, chapter_id):
    """Afficher les vidéos et textes d'un chapitre."""
    user = request.user
    chapter = get_object_or_404(Chapitre, id=chapter_id)
    videos = Video.objects.filter(chapitre=chapter)
    texts = Texte.objects.filter(chapitre=chapter)

    if hasattr(user, 'etudiant'):
        return render(request, 'Etudiant/chapter_details.html', {'chapter': chapter, 'videos': videos, 'texts': texts})
    return redirect('login')

@login_required
def quiz_detail_student(request, quiz_id):
    """Afficher les détails d'un quiz et permettre à l'étudiant de le passer."""
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        # Logique pour évaluer le quiz
       
        pass

    return render(request, 'Etudiant/quiz_detail.html', {'quiz': quiz, 'questions': questions})



# Fin Partie View Concernant les Etudiants##########################################################################################





# Fin Partie View Concernant les Tuteurs##########################################################################################


@login_required
def dashboard_tuteur(request):
    tuteur = get_object_or_404(Tuteur, user=request.user)
    etudiants = Etudiant.objects.filter(enrolled_by_tuteur=tuteur)
    
    context = {
        'tuteur': tuteur,
        'etudiants': etudiants,
    }
    return render(request, 'dashboard_tuteur.html', context)











@login_required
def tuteur_available_courses(request, etudiant_id):
    tuteur = request.user.tuteur
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    
    # Obtenir la liste des cours auxquels l'étudiant n'est pas encore inscrit
    available_courses = Course.objects.exclude(students=etudiant)
    
    context = {
        'etudiant': etudiant,
        'available_courses': available_courses,
    }
    return render(request, 'Tuteur/available_courses.html', context)


@login_required
def tuteur_enroll_in_course(request, etudiant_id, course_id):
    tuteur = request.user.tuteur
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    course = get_object_or_404(Course, id=course_id)
    
    # Inscrire l'étudiant au cours si ce n'est pas déjà fait
    if etudiant not in course.students.all():
        course.students.add(etudiant)
    
    return redirect('tuteur_enrolled_courses', etudiant_id=etudiant.id)



@login_required
def tuteur_enrolled_courses(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    enrolled_courses = etudiant.course_set.all()  # Obtenir les cours auxquels l'étudiant est inscrit
    
    context = {
        'etudiant': etudiant,
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'Tuteur/enrolled_courses.html', context)





# Fin Partie View Concernant les Tuteurs##########################################################################################