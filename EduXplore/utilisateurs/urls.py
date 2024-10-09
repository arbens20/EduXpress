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
    

    path('course/create/', utilisateurs_views.create_course, name='create_course'),
    path('course/<int:course_id>/enroll/', utilisateurs_views.enroll_student, name='enroll_student'),
    path('course/<int:course_id>/chapitre/create/', utilisateurs_views.create_chapitre, name='create_chapitre'),
    path('chapitre/<int:chapitre_id>/video/create/', utilisateurs_views.create_video, name='create_video'),
    path('chapitre/<int:chapitre_id>/audio/create/', utilisateurs_views.create_audio, name='create_audio'),
    path('chapitre/<int:chapitre_id>/text/create/', utilisateurs_views.create_text, name='create_text'),
    path('teacher/courses/', utilisateurs_views.teacher_courses, name='teacher_courses'),
    path('course/<int:course_id>/', utilisateurs_views.course_detail, name='course_detail'),
    # path('course/<int:course_id>/', utilisateurs_views.course_chapters, name='course_chapters'),
    path('course/<int:course_id>/chapters/', utilisateurs_views.course_chapters, name='course_chapters'),
    path('chapitre/<int:chapitre_id>/videos/', utilisateurs_views.chapitre_videos, name='chapitre_videos'),
    path('chapitre/<int:chapitre_id>/video/add/', utilisateurs_views.create_video, name='create_video'),
    path('chapitre/<int:chapitre_id>/audio/add/', utilisateurs_views.create_audio, name='create_audio'),
    path('chapitre/<int:chapitre_id>/text/add/', utilisateurs_views.create_text, name='create_text'),
    path('chapitre/<int:chapitre_id>/', utilisateurs_views.chapitre_detail, name='chapitre_detail'),
    path('chapitre/<int:chapitre_id>/audios/', utilisateurs_views.chapitre_audios, name='chapitre_audios'),
    path('chapitre/<int:chapitre_id>/textes/', utilisateurs_views.chapitre_textes, name='chapitre_textes'),
    
    
    
    path('chapitre/<int:chapitre_id>/quiz/create/', utilisateurs_views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/questions/add/', utilisateurs_views.add_question, name='add_question'),
    path('questions/<int:question_id>/choices/add/', utilisateurs_views.add_choices, name='add_choices'),
    
    
    path('courses/', utilisateurs_views.available_courses, name='available_courses'),
    path('courses/enroll/<int:course_id>/', utilisateurs_views.enroll_in_course, name='enroll_in_course'),
    path('my_courses/', utilisateurs_views.my_courses, name='my_courses'),
    path('courses/<int:course_id>/', utilisateurs_views.course_detail2, name='course_detail'),
    path('etudiant/course/<int:course_id>/detail/', utilisateurs_views.student_course_detail, name='student_course_detail'),
   

    path('course/<int:course_id>/chapters/', utilisateurs_views.course_chapters_student, name='course_chapters_student'),
    
    path('etudiant/courses/', utilisateurs_views.available_courses_for_student, name='available_courses_for_student'),
    path('etudiant/course/<int:course_id>/chapters/', utilisateurs_views.student_course_chapters, name='student_course_chapters'),







]