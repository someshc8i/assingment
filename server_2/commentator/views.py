# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

def HoldAndCommentClicked(request):
    if request.method=='GET':
        redis_conn = Redis('localhost',6379)
        q = Queue('somesh', connection=redis_conn)
        q.enqueue(score_func)
        return JsonResponse({"response" : "clicked"}, safe=False, content_type='application/json')


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
        print(comment)
        redis_conn = Redis('localhost',6379)
        q = Queue('somesh', connection=redis_conn)
        for i in range(q.count):
            if i > 0:
                job = q.jobs[i]
                job.perform()
                print job.result
        q.empty()
        return JsonResponse({"response" : "recieved"}, safe=False, content_type='application/json')
