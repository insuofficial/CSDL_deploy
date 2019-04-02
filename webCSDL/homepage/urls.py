from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('test/', views.test_page, name='test_page'),

    path('', views.main_page, name='main_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', auth_views.LoginView.as_view(template_name='homepage/account/login.html'), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('profile_update/', views.profile_update, name='profile_update'),

    path('professor/', views.professor_page, name='professor_page'),
    path('member/', views.member_page, name='member_page'),
    path('alumni/', views.alumni_page, name='alumni_page'),

    path('overview/', views.overview_list, name='overview_list'),
    path('overview/<path:pk>/', views.overview_detail, name='overview_detail'),
    path('project/', views.project_list, name='project_list'),
    path('project/newpost', views.project_post, name='project_post'),
    path('project/<path:pk>/edit', views.project_edit, name='project_edit'),

    path('journal/', views.journal_list, name='journal_list'),
    path('journal/newpost', views.journal_post, name='journal_post'),
    path('journal/<path:pk>/edit/', views.journal_edit, name='journal_edit'),
    path('conference/', views.conference_list, name='conference_list'),
    path('conference/<path:pk>/edit/', views.conference_edit, name='conference_edit'),
    path('patent/', views.patent_list, name='patent_list'),
    path('patent/newpost', views.patent_post, name='patent_post'),
    path('patent/<path:pk>/edit/', views.patent_edit, name='patent_edit'),

    path('notice/', views.notice_list, name='notice_list'),
    path('notice/newpost', views.notice_post, name='notice_post'),
    path('notice/<path:pk>/edit/', views.notice_edit, name='notice_edit'),
    path('notice/<path:pk>/', views.notice_detail, name='notice_detail'),
    path('seminar/', views.seminar_list, name='seminar_list'),
    path('seminar/newpost', views.seminar_post, name='seminar_post'),
    path('seminar/<path:pk>/edit/', views.seminar_edit, name='seminar_edit'),
    path('album/', views.album_list, name='album_list'),
    path('album/newpost', views.album_post, name='album_post'),
    path('album/<path:pk>/edit/', views.album_edit, name='album_edit'),
    path('album/<path:pk>', views.album_detail, name='album_detail'),

    path('contact/', views.contact_page, name='contact_page'),
]

