from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views.snippets import SnippetView
from .views.tag import TagView

urlpatterns = [
    # signin
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # snippet
    path('snippets/',SnippetView.as_view({'get':'list'}),name='snippets'),
    path('snippet/<int:id>/',SnippetView.as_view({'get':'detail_view'}),name='snippet_detail'),
    path('create-snippet/',SnippetView.as_view({'post':'create'}),name='create_snippet'),
    path('update-snippet/<int:id>/',SnippetView.as_view({'put':'update'}),name='update_snippet'),
    path('delete-snippet/<int:id>/',SnippetView.as_view({'delete':'delete'}),name='delete_snippet'),
    # tag
    path('tags/',TagView.as_view({'get':'list'}),name='tags'),
    path('tags/<int:id>/',TagView.as_view({'get':'detail_view'}),name='tag_detail'),
]