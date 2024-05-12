from django.urls import reverse

from rest_framework import serializers

from ..models import Tag,Snippet

class SnippetSerializer(serializers.Serializer):

    def __init__(self, instance=None, data=..., **kwargs):
        self.request = kwargs['context']['request']
        self.instance = instance
        super().__init__(instance, data, **kwargs)

    title = serializers.CharField(max_length=100,error_messages={'required':'Title is required'})
    content = serializers.CharField(error_messages={'required':'Content is required'})
    tag = serializers.CharField(max_length=100,error_messages={'required':'Tag is required'})

    def create(self, validated_data):
        data = self.validated_data
        tag,_ = Tag.objects.get_or_create(title=data.pop('tag'))
        data['tag'] = tag
        data['created_by'] = self.request.user
        snippet = Snippet.objects.create(**data)
        return snippet
    
    def update(self):
        instance = self.instance
        tag,_ = Tag.objects.get_or_create(title=self.validated_data.get('tag'))
        instance.title = self.validated_data.get('title')
        instance.content = self.validated_data.get('content')
        instance.tag = tag
        instance.save(update_fields=('title','content','tag','updated_at'))
        return instance
    
class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    
class SnippetListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)
    tag = TagSerializer(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)

    def get_link(self,obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('snippet_detail', kwargs={'id': obj.id}))


