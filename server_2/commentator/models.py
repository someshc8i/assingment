# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Commentator(models.Model):
    name = models.CharField(max_length = 100 )
    about_me = models.TextField()
    why_cricket = models.TextField()
    fav_cricket_moments = models.TextField()
    photo = models.TextField()
    def __str__(self):
        return self.name

class Commentary(models.Model):
    text = models.TextField()
    commentator = models.ForeignKey(Commentator , related_name = 'commentary')
    def __str__(self):
        return self.text
