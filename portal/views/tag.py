from django.core.paginator import Paginator
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from ..serializer.tag import TagListsSerializer,TagDetailViewSerializer
from ..models import Tag

class TagView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    def get_serializer_class(self):
        group_serializer = {
            'list':TagListsSerializer,
            'detail_view':TagDetailViewSerializer
        }
        if self.action in group_serializer.keys():
            return group_serializer[self.action]
        
    def list(self, request, *args, **kwargs):
        response = {}
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)
        queryset = Tag.objects.annotate(snippets=Count('snippet_tags'))
        pagination = Paginator(queryset, limit)
        records = pagination.get_page(page)
        has_next = records.has_next()
        has_previous = records.has_previous()
        ser = self.get_serializer(records,many=True,context={'request':request})
        response['result'] = 'success'
        response['records'] = ser.data,
        response['total_count'] = queryset.count()
        response['has_next'] = has_next
        response['has_previous'] = has_previous
        response['pages'] = pagination.num_pages
        return Response(response)
    
    def detail_view(self, request, *args, **kwargs):
        response = {}
        try:
            queryset = Tag.objects.prefetch_related('snippet_tags').get(id=self.kwargs['id'])
            ser = self.get_serializer(queryset,context={'request':request})
            response['result'],response['records'] = 'success',ser.data
        except Tag.DoesNotExist:
            response['result'],response['message'] = 'failure','Tag details not found'
        return Response(response)

