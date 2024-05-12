from django.db import transaction
from django.db import IntegrityError
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status

from ..serializer.snippets import SnippetSerializer,SnippetListSerializer
from ..models import Snippet

class SnippetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    def get_serializer_class(self):
        group_serializer = {
            'create':SnippetSerializer,
            'update':SnippetSerializer,
            'list':SnippetListSerializer,
            'detail_view':SnippetListSerializer
        }
        if self.action in group_serializer.keys():
            return group_serializer[self.action]
        
    def list(self, request, *args, **kwargs):
        response = {}
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)
        queryset = Snippet.objects.select_related('tag')
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
            queryset = Snippet.objects.select_related('tag').get(id=self.kwargs['id'])
            ser = self.get_serializer(queryset,context={'request':request})
            response['result'],response['records'] = 'success',ser.data
        except Snippet.DoesNotExist:
            response['result'],response['message'] = 'failure','Snippet details not found'
        return Response(response)

    def create(self, request, *args, **kwargs):
        response,status_code = {}, status.HTTP_200_OK
        try:
            ser = self.get_serializer(data=request.data,context={'request':request})
            if ser.is_valid():
                with transaction.atomic():
                    snippet = ser.save()
                    response['result'],response['records'] = 'success','Saved successfully'
            else:
                response['result'], response['errors'] =  'failure', {key:ser.errors[key][0] for key in ser.errors.keys()}
                status_code = status.HTTP_400_BAD_REQUEST
        except IntegrityError:
            response['result'],response['message'] = 'failure','Snippet already exists'
        return Response(response,status=status_code)
    
    def update(self, request, *args, **kwargs):
        response,status_code = {}, status.HTTP_200_OK
        try:
            instance = Snippet.objects.get(id=self.kwargs['id'])
            ser = self.get_serializer(data=request.data,instance=instance,context={'request':request})
            if ser.is_valid():
                with transaction.atomic():
                    snippet = ser.update()
                    response['result'],response['records'] = 'success','Updated successfully'
            else:
                response['result'], response['errors'] =  'failure', {key:ser.errors[key][0] for key in ser.errors.keys()}
                status_code = status.HTTP_400_BAD_REQUEST
        except Snippet.DoesNotExist:
            response['result'],response['message'] = 'failure','Snippet details not found'
        except IntegrityError:
            response['result'],response['message'] = 'failure','Snippet already exists'
        return Response(response,status=status_code)
    
    def delete(self, request, *args, **kwargs):
        response,status_code = {}, status.HTTP_200_OK
        try:
            instance = Snippet.objects.get(id=self.kwargs['id'])
            instance.delete()
            response['result'],response['records'] = 'success','Deleted successfully'
        except Snippet.DoesNotExist:
            response['result'],response['message'] = 'failure','Snippet details not found'
        return Response(response,status=status_code)
    
    
    
    
