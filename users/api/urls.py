from django.urls import path, include
from users.api import views
from .views import Checking, student_checking, FileView, GenericView, FilePUDView, quotes_view, quotes_view2, \
                FileTask, deletingFile, get_view

urlpatterns = [
    path('check/', Checking.as_view()),
    path('checking/<s_id>', student_checking.as_view()),
    path('file/', FileView.as_view()),
    path('file/generic/', GenericView.as_view({'get': 'list'})),
    path('file/generic/<key>', GenericView.as_view({'get': 'oneby'})),
    path('file/pud/<file>', FilePUDView.as_view()),
    path('file/generic/quote/', GenericView.as_view({'get': 'quotes'})),
    path('quotes/', quotes_view.as_view()),
    path('quotes2/', quotes_view2.as_view()),
    path('image/', FileTask.as_view()),
    path('image/<int:pk>/', views.deleteFile),
    path('delete/<int:pk>/', deletingFile.as_view()),
    path('single/<int:pk>/', get_view.as_view()),
]
