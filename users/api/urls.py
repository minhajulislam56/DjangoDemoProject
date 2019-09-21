from django.urls import path, include
from users.api import views
from users.api import myviews

from .views import Checking, student_checking, FileView, GenericView, FilePUDView, quotes_view, quotes_view2, \
                FileTask, deletingFile, get_view, CourseView

from .myviews import (
    StatusAll,
    StatusAPIView,
    StatusCreateAPIView,
    StatusRetriveAPIView,
    StatusUpdateAPIView,
    StatusDeleteAPIView,
    StatusMixinsView,
    StatusAPIDetailView,

    #Practicing...
    StaffDetection,
    )

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


    path('status/', StatusAPIView.as_view()),
    path('status/<id>/', StatusAPIDetailView.as_view()),
    #path('status/create/', StatusCreateAPIView.as_view()),
    #path('status/<id>/', StatusRetriveAPIView.as_view()), #<pk> is default
    #path('status/<pk>/update/', StatusUpdateAPIView.as_view()),
    #path('status/<pk>/delete/', StatusDeleteAPIView.as_view()),
    #path('status/mxn/<pk>', StatusMixinsView.as_view()),
    path('staff/', StaffDetection.as_view()),



    #.......Demo Project.....

    path('courses/', CourseView.as_view()),

]
