from django.conf.urls import url
from commentator.views import *
from django.views.generic.base import TemplateView
urlpatterns = [
    url(r'api/score_reciever$', ScoreReciever),
    url(r'api/comment_reciever$', CommentReciever),
    url(r'api/hold_and_comment$', HoldAndCommentClicked),
    ]
