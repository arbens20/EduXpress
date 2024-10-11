from django.urls import path
from utilisateurs import views as utilisateurs_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', utilisateurs_views.home, name="home"),
    path('index', utilisateurs_views.index, name="index"),
    path('login_view', utilisateurs_views.login_view, name="login_view"),
    path('register_enseignant', utilisateurs_views.register_enseignant, name="register_enseignant"),
    path('register_tuteur', utilisateurs_views.register_tuteur, name="register_tuteur"),
    path('register_etudiant', utilisateurs_views.register_etudiant, name="register_etudiant"),
    path('dashboard_enseignant', utilisateurs_views.dashboard_enseignant, name="dashboard_enseignant"),
    path('home_etudiant', utilisateurs_views.home_etudiant, name="home_etudiant"),

    path('logout_view', utilisateurs_views.logout_view, name="logout_view"),
    path('activate/<uidb64>/<token>/', utilisateurs_views.activate, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    



    
    
    

    
    





# Partie Url Concernant les Enseignant##########################################################################################

    path('create_course/', utilisateurs_views.create_course, name='create_course'),
    path('courses/', utilisateurs_views.course_list, name='course_list'),
    path('create_chapitre/<int:course_id>/', utilisateurs_views.create_chapitre, name='create_chapitre'),
    path('chapitres/<int:course_id>/', utilisateurs_views.chapter_list, name='chapter_list'),
    path('create_video/<int:chapitre_id>/', utilisateurs_views.create_video, name='create_video'),
    path('create_audio/<int:chapitre_id>/', utilisateurs_views.create_audio, name='create_audio'),
    path('create_texte/<int:chapitre_id>/', utilisateurs_views.create_texte, name='create_texte'),
    path('create_quiz/<int:chapitre_id>/', utilisateurs_views.create_quiz, name='create_quiz'),
    path('create_question/<int:quiz_id>/', utilisateurs_views.create_question, name='create_question'),
    path('quizzes/', utilisateurs_views.quiz_list, name='quiz_list'),
    path('chapitre/<int:chapitre_id>/', utilisateurs_views.chapitre_detail, name='chapitre_detail'),
    path('quiz/<int:quiz_id>/', utilisateurs_views.quiz_detail, name='quiz_detail'),
    path('chapitre/<int:chapitre_id>/', utilisateurs_views.chapitre_detail_global, name='chapitre_detail_global'),




#  Fin Partie Url Concernant les Enseignant##########################################################################################


# Urls Pour les etudiants ##########################################################################################################



    # path('courses/', utilisateurs_views.available_courses_student, name='available_courses_student'),
    path('enroll/<int:course_id>/', utilisateurs_views.enroll_in_course_student, name='enroll_in_course_student'),
    path('my_courses/', utilisateurs_views.student_courses_student, name='student_courses_student'),
    path('course/<int:course_id>/chapters/', utilisateurs_views.course_chapters_student, name='course_chapters_student'),
    path('chapter/<int:chapter_id>/', utilisateurs_views.chapter_details_student, name='chapter_details_student'),
    path('quiz/<int:quiz_id>/', utilisateurs_views.quiz_detail_student, name='quiz_detail_student'),
    
    path('etudiant/courses/available/', utilisateurs_views.available_courses, name='available_courses'),  # Cours disponibles
    path('etudiant/courses/enrolled/', utilisateurs_views.enrolled_courses, name='enrolled_courses'),  # Cours inscrits
    path('courses/enroll/<int:course_id>/', utilisateurs_views.enroll_in_course, name='enroll_in_course'),  # Inscription à un cours





#  Fin Urls Pour les etudiants ##########################################################################################################



# Debuts URLS Pour les Tuteurs #########################################################################################################

path('dashboard_tuteur', utilisateurs_views.dashboard_tuteur, name='dashboard_tuteur'),

path('tuteur/etudiant/<int:etudiant_id>/courses/available/', utilisateurs_views.tuteur_available_courses, name='tuteur_available_courses'),
    
path('tuteur/etudiant/<int:etudiant_id>/courses/enroll/<int:course_id>/', utilisateurs_views.tuteur_enroll_in_course, name='tuteur_enroll_in_course'),
    
path('tuteur/etudiant/<int:etudiant_id>/courses/enrolled/', utilisateurs_views.tuteur_enrolled_courses, name='tuteur_enrolled_courses'),








# Fin URLS Pour les Tuteurs #############################################################################################################











]