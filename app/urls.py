from django.urls import path
from . import  views


urlpatterns =[path('', views.QuestionView.as_view(), name='index'),
              path('question/<int:pk>/', views.QuestionDetails.as_view(), name='question_detail'),
              path('hot/', views.HotQuestionView.as_view(), name='hot_questions'),
              path('settings/', views.SettingsView.as_view(), name='settings'),
              path('ask/', views.NewAskView.as_view(), name='new_ask'),
              path('register/', views.RegisterView.as_view(), name='register'),
              path('login/', views.LoginView.as_view(), name='login'),
              path('tag/', views.TagView.as_view(), name='tag'),
              path('review/<int:pk>/', views.AddComments.as_view(),name='add_comments'),
              path('review/<int:pk>/add_likes', views.AddLike.as_view(),name='add_likes'),
              path('review/<int:pk>/del_likes', views.DelLike.as_view(),name='del_likes')]
