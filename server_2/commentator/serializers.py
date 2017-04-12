from rest_framework import serializers
from commentator.models import *

class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = '__all__'
        
class CommentatorSerializer(serializers.ModelSerializer):
    commentary = CommentarySerializer(many = True , read_only = True)
    class Meta:
        model = Commentator
        fields = [
        'name',
        'about_me',
        'why_cricket',
        'fav_cricket_moments',
        'photo',
        'commentary'
        ]
