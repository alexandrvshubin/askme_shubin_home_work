from django.urls import path
from . import views
from .views import LikeQuestionAjaxView, LikeCommentAjaxView, MarkCorrectAnswerView



urlpatterns = [path('', views.QuestionView.as_view(), name='index'),
               path('question/<int:pk>/', views.QuestionDetails.as_view(), name='question_detail'),
               path('hot/', views.HotQuestionView.as_view(), name='hot_questions'),
               path('settings/', views.ProfileEditView.as_view(), name='settings'),
               path('ask/', views.NewAskView.as_view(), name='new_ask'),
               path('register/', views.RegisterView.as_view(), name='register'),
               path('login/', views.LoginView.as_view(), name='login'),
               path('logout', views.logout_view, name='logout'),
               path('tag/', views.TagView.as_view(), name='tag'),
               path('review/<int:pk>/', views.AddComments.as_view(), name='add_comments'),
               path('ajax/like/question/', LikeQuestionAjaxView.as_view(), name='like_question_ajax'),
               path('ajax/like/comment/', LikeCommentAjaxView.as_view(), name='like_comment_ajax'),
               path('ajax/mark-correct/', MarkCorrectAnswerView.as_view(), name='mark_correct_answer'),
               ]

