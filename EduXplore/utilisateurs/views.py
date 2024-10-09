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


def dashboard_enseignant(request):
    user = request.user
    if hasattr(user, 'enseignant'):
        # C'est un enseignant
        context = {'role': 'Enseignant', 'user_info': user.enseignant}
    else:
        context = {'role': 'Utilisateur inconnu'}
    return render(request, 'dashboard_enseignant.html', context)


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
    if hasattr(user, 'enseignant'):
        # C'est un enseignant
        context = {'role': 'Etudiant', 'user_info': user.etudiant}
    else:
        context = {'role': 'Utilisateur inconnu'}
    return render(request, 'home_etudiant.html', context)







# Vue d'activation du compte
from django.shortcuts import redirect
from django.http import HttpResponse

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
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login_view')  # Redirige vers la page de connexion






# Créer un cours
@login_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        teacher = Enseignant.objects.get(user=request.user)

        course = Course.objects.create(title=title, description=description, teacher=teacher)
        return redirect('teacher_courses')  # redirection vers la liste des cours après la création

    return render(request, 'create_course.html')


# Créer un enrôlement
@login_required
def enroll_student(request, course_id):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Etudiant, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        Enrollment.objects.create(student=student, course=course)
        return redirect('course_detail', course_id=course.id)

    students = Etudiant.objects.all()  # liste d'étudiants pour enrôler
    return render(request, 'enroll_student.html', {'students': students})


# Créer un chapitre
@login_required
def create_chapitre(request, course_id):
    if request.method == 'POST':
        nom_chapitre = request.POST.get('nom_chapitre')
        description = request.POST.get('description')
        course = get_object_or_404(Course, id=course_id)
        chapitre = Chapitre.objects.create(cours=course, nom_chapitre=nom_chapitre, description=description)
        return redirect('course_detail', course_id=course.id)

    return render(request, 'create_chapitre.html')


# Créer une vidéo avec gestion de la taille


@login_required
def create_video(request, chapitre_id):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.FILES.get('contenu')
        chapitre = get_object_or_404(Chapitre, id=chapitre_id)

        # Vérification de la taille du fichier (par exemple, 50 MB maximum)
        max_file_size = 50 * 1024 * 1024  # 50 MB
        if contenu.size > max_file_size:
            return HttpResponse('La taille de la vidéo dépasse la limite autorisée de 50 MB.')

        Video.objects.create(chapitre=chapitre, titre=titre, contenu=contenu)

        # Rediriger vers la page des chapitres du cours en utilisant course_id
        return redirect('chapitre_detail', course_id=chapitre.cours.id)

    return render(request, 'create_video.html')



@login_required
def chapitre_videos(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    videos = Video.objects.filter(chapitre=chapitre)

    return render(request, 'chapitre_videos.html', {'chapitre': chapitre, 'videos': videos})



# Créer un audio
@login_required
def create_audio(request, chapitre_id):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.FILES.get('contenu')
        chapitre = get_object_or_404(Chapitre, id=chapitre_id)

        Audio.objects.create(chapitre=chapitre, titre=titre, contenu=contenu)
        return redirect('chapitre_detail', chapitre_id=chapitre.id)

    return render(request, 'create_audio.html')


# Créer un texte
@login_required
def create_text(request, chapitre_id):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        chapitre = get_object_or_404(Chapitre, id=chapitre_id)

        Texte.objects.create(chapitre=chapitre, titre=titre, contenu=contenu)
        return redirect('chapitre_detail', chapitre_id=chapitre.id)

    return render(request, 'create_text.html')




# Vue pour afficher les cours de l'enseignant connecté
@login_required
def teacher_courses(request):
    # Vérifiez que l'utilisateur est un enseignant et est connecté
    if request.user.is_authenticated :
        # Trouver l'enseignant lié à cet utilisateur
        try:
            enseignant = Enseignant.objects.get(user=request.user)
        except Enseignant.DoesNotExist:
            enseignant = None
        
        # Filtrer les cours associés à cet enseignant
        if enseignant:
            courses = Course.objects.filter(teacher=enseignant)
        else:
            courses = []
    else:
        # Si l'utilisateur n'est pas un enseignant ou n'est pas connecté
        courses = []

    # Renvoyer les cours filtrés à un template
    return render(request, 'teacher_courses.html', {'courses': courses})




def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})



def course_chapters(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapitres = Chapitre.objects.filter(cours=course)
    
    return render(request, 'course_chapters.html', {'course': course, 'chapitres': chapitres})



@login_required
def chapitre_detail(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    videos = chapitre.video_set.all()  
    audios = chapitre.audio_set.all()  
    texts = chapitre.texte_set.all()  

    context = {
        'chapitre': chapitre,
        'videos': videos,
        'audios': audios,
        'texts': texts,
    }
    
    return render(request, 'chapitre_detail.html', context)




# recuperer audio d'un chapitre

@login_required
def chapitre_audios(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    audios = chapitre.audio_set.all()  # Récupère tous les audios liés au chapitre

    context = {
        'chapitre': chapitre,
        'audios': audios,
    }
    
    return render(request, 'chapitre_audios.html', context)



# recuperer texte d'un chapitre
@login_required
def chapitre_textes(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    texts = chapitre.texte_set.all()  # 

    context = {
        'chapitre': chapitre,
        'texts': texts,
    }
    
    return render(request, 'chapitre_textes.html', context)





############################################################################################################
@login_required
def create_quiz(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            quiz = Quiz.objects.create(title=title, chapitre=chapitre, teacher=request.user.enseignant)
            return redirect('add_question', quiz_id=quiz.id)
    return render(request, 'create_quiz.html', {'chapitre': chapitre})




# Ajouter question Quiz Prof

@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        question_text = request.POST.get('text')
        points = request.POST.get('points')
        if question_text and points:
            question = Question.objects.create(text=question_text, points=points, quiz=quiz)
            return redirect('add_choices', question_id=question.id)
    return render(request, 'add_question.html', {'quiz': quiz})





# ajouter reponse quiz prof

@login_required
def add_choices(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        choice_text = request.POST.get('text')
        is_correct = request.POST.get('is_correct') == 'on'
        if choice_text:
            Choice.objects.create(text=choice_text, is_correct=is_correct, question=question)
        return redirect('add_choices', question_id=question.id)  # Reviens sur la même page pour ajouter d'autres réponses
    return render(request, 'add_choices.html', {'question': question})





# voir les cours disponible non enregistrer
@login_required
def available_courses(request):
    student = Etudiant.objects.get(user=request.user)
    enrolled_courses = Enrollment.objects.filter(student=student).values_list('course', flat=True)
    courses = Course.objects.exclude(id__in=enrolled_courses)
    
    return render(request, 'available_courses.html', {'courses': courses})




# lec cours ou l'etudiant est inscrit
def available_courses_for_student(request):
    etudiant = get_object_or_404(Etudiant, user=request.user)
    
    # Filtrer les cours auxquels l'étudiant n'est pas encore inscrit
    available_courses = Course.objects.exclude(students=etudiant)
    
    return render(request, 'available_courses.html', {'courses': available_courses})




# @login_required
# def enroll_in_course(request, course_id):
#     student = Etudiant.objects.get(user=request.user)
#     course = get_object_or_404(Course, id=course_id)
    
#     # Vérifie si l'étudiant est déjà enrôlé
#     if not Enrollment.objects.filter(student=student, course=course).exists():
#         Enrollment.objects.create(student=student, course=course)
    
#     return redirect('my_courses')  # Rediriger vers une vue où l'étudiant voit ses cours

def enroll_in_course(request, course_id):
    etudiant = get_object_or_404(Etudiant, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    
    # Ajouter l'étudiant au cours s'il n'est pas déjà inscrit
    if etudiant not in course.students.all():
        Enrollment.objects.create(student=etudiant, course=course)
    
    return redirect('student_course_chapters', course_id=course.id)



# Afficher les cours enrolle

@login_required
def my_courses(request):
    student = Etudiant.objects.get(user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    
    return render(request, 'my_courses.html', {'enrollments': enrollments})




@login_required
def course_detail2(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapters = course.chapitre_set.all()  # Assumant que tu as un modèle "Chapitre" lié à "Course"
    
    return render(request, 'course_chapters_student.html', {'course': course, 'chapters': chapters})



def course_chapters_student(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapitres = Chapitre.objects.filter(cours=course)
    
    return render(request, 'course_chapters_student.html', {'course': course, 'chapitres': chapitres})



# Afficher chapitre cours

def student_course_chapters(request, course_id):
    # Récupérer l'étudiant connecté
    etudiant = get_object_or_404(Etudiant, user=request.user)
    
    course = get_object_or_404(Course, id=course_id)
    
    if etudiant not in course.students.all():
        return redirect('available_courses_for_student')  

    chapters = course.chapitre_set.all()  
    
    context = {
        'course': course,
        'chapters': chapters
    }
    return render(request, 'course_chapters_student.html', context)



# details cours etudiant


def student_course_detail(request, course_id):
    # Récupérer l'étudiant connecté
    etudiant = get_object_or_404(Etudiant, user=request.user)
    
    # Vérifier que l'étudiant est bien inscrit dans le cours
    enrollment = get_object_or_404(Enrollment, course_id=course_id, student=etudiant)
    
    # Récupérer le cours et ses chapitres
    course = enrollment.course
    chapters = course.chapitre_set.all()
    
    context = {
        'course': course,
        'chapters': chapters,
    }
    return render(request, 'student_course_detail.html', context)


