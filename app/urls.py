from django.urls import path
from . import  views


urlpatterns =[path('', views.QuestionView.as_view()),
              path('question/<int:pk>/', views.QuestionDetails.as_view()),
              path('hot/', views.HotQuestionView.as_view()),
              path('settings/', views.SettingsView.as_view()),
              path('ask/', views.NewAskView.as_view()),
              path('register/', views.RegisterView.as_view()),
              path('login/', views.LoginView.as_view()),
              path('tag/', views.TagView.as_view()),
              path('review/<int:pk>/', views.AddComments.as_view(),name='add_comments'),
              path('review/<int:pk>/add_likes', views.AddLike.as_view(),name='add_likes'),
              path('review/<int:pk>/del_likes', views.DelLike.as_view(),name='del_likes')]
