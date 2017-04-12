from django.conf.urls import url
from commentator.views import *
from django.views.generic.base import TemplateView
urlpatterns = [
    url(r'api/score_reciever$', ScoreReciever),
    url(r'api/comment_reciever$', CommentReciever),
    url(r'api/hold_and_comment$', HoldAndCommentClicked),
    url(r'api/commentator_entry$', CommentatorEntry),
    url(r'xyz$', CloudinaryDetails),
    url(r'api/commentator_details/(?P<pk>[0-9]+)$', CommentatorDetails.as_view()),
    url(r'(?P<name>\w+)$' , CommentatorProfile),
    ]
