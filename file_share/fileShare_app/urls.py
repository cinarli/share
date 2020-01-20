from django.urls import path
from .views import (simple_upload,
                    FileDetailView,
                    deleteFile,
                    deleteComment,
                    shareView,
                    sharedPeopleView,
                    delSharedPeopleView,
                    comment_permissionView,
                    editComment,
                    myFilesView
                    )
from django.conf import settings
from django.conf.urls.static import static

app_name='fileShare_app'
urlpatterns = [
    path('', simple_upload, name='home'),
    path('file/<int:id>/', FileDetailView.as_view(), name='file'),
    path('delete/<int:id>/', deleteFile, name='delete'),
    path('deletecomment/',deleteComment,name='deleteComment'),
    path('sharefile/',shareView,name='share'),
    path('sharedpeople/<int:id>/',sharedPeopleView,name='sharedpeople'),
    path('delsharedpeople/',delSharedPeopleView,name='delsharedpeople'),
    path('comment_permission/', comment_permissionView, name='comment_permission'),
    path('edit-comment/', editComment, name='edit_comment'),
     path('myfiles/', myFilesView, name='myfiles'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)