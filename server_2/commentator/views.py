# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics, mixins

from django.shortcuts import render
# from rest_framework.views import APIView
from django.http import JsonResponse
# from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.exceptions import ParseError
from rest_framework import status
from django_rq import job
from rq import Queue
from redis import Redis
import time
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib


from commentator.models import *
from commentator.serializers import *

def score_func(score):
    return score

@csrf_exempt
def ScoreReciever(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        score = str(data['score']) + '/' + str(data['wickets'])
        redis_conn = Redis('localhost',6379)
        q = Queue('somesh', connection=redis_conn)
        if q.count != 0:
            q.enqueue(score_func,score)
        else:
            print score_func(score)
        return JsonResponse({"response" : "recieved"}, safe=False, content_type='application/json')


def CommentatorProfile(request , name):
    if request.method == 'GET':
        try:
            c = Commentator.objects.get(name = name)
        except:
            return redirect('/')
        pk = c.pk
        return render(request, 'commentary.html' , {'pk' : pk})

def HoldAndCommentClicked(request):
    if request.method=='GET':
        redis_conn = Redis('localhost',6379)
        q = Queue('somesh', connection=redis_conn)
        q.enqueue(score_func)
        return JsonResponse({"response" : "clicked"}, safe=False, content_type='application/json')


def CloudinaryDetails(request):
    if request.method=='GET':
        t =  int(time.time())
        public_id = str(t)
        api_key = 'XCrOdtboQsVJ0qvfarG-VXByv0g'
        a = 'public_id=' + public_id + '&timestamp=' + str(t) + api_key
        h = hashlib.sha1()
        h.update(a)
        h=h.hexdigest()
        return JsonResponse({"signature" : h , "timestamp" : t , "api_key" : "377269835254154" , "public_id" : public_id }, safe=False, content_type='application/json')

@csrf_exempt
def CommentatorEntry(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        name = data['name']
        photo = data['photo']
        about_me = data['about_me']
        why_cricket = data['why_cricket']
        fav_cricket_moments = data['fav_cricket_moments']
        c = Commentator(
            name = name,
            photo = photo,
            about_me = about_me,
            why_cricket = why_cricket,
            fav_cricket_moments = fav_cricket_moments
        )
        c.save()
        return JsonResponse({"response" : "success"}, safe=False, content_type='application/json')

@csrf_exempt
def CommentReciever(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        comment = data['comment']
        pk = data['pk']
        commentator = Commentator.objects.get(pk = pk)
        commentary = Commentary(
            text = comment,
            commentator = commentator
        )
        commentary.save()
        print(comment)
        redis_conn = Redis('localhost',6379)
        q = Queue('somesh', connection=redis_conn)
        for i in range(q.count):
            if i > 0:
                job = q.jobs[i]
                try:
                    job.perform()
                    if job.result != None:
                        print job.result
                except:
                    print('')
        q.empty()
        return JsonResponse({"response" : "recieved"}, safe=False, content_type='application/json')

class CommentatorDetails(generics.RetrieveAPIView):
    queryset = Commentator.objects.all()
    serializer_class = CommentatorSerializer
