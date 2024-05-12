from django.urls import reverse

from rest_framework import serializers
from ..serializer.snippets import TagSerializer

class TagListsSerializer(TagSerializer):
    snippets = serializers.IntegerField()
    link = serializers.SerializerMethodField(read_only=True)

    def get_link(self,obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('tag_detail', kwargs={'id': obj.id}))

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)

    def get_link(self,obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('snippet_detail', kwargs={'id': obj.id}))

class TagDetailViewSerializer(TagSerializer):
    snippets = SnippetSerializer(source='snippet_tags',read_only=True,many=True)