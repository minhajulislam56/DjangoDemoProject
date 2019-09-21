from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from users.models import Status
from .serializers import StatusSerializer

from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions

from rest_framework import mixins
from django.shortcuts import get_object_or_404


def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class StatusAll(APIView):

    def get(self, request, format=None):
        qs = Status.objects.all()
        serializer = StatusSerializer(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        qs = Status.objects.all()
        serializer = StatusSerializer(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework import generics
from rest_framework.generics import ListAPIView


class StatusAPIDetailView(mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication] #Oauth, JWT
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request.body, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None

    def perform_update(self, serializer):
        serializer.save(updated_by_user = self.request.user)


class StatusAPIView(mixins.CreateModelMixin,
                    generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication] #Oauth, JWT
    serializer_class = StatusSerializer
    passed_id = None


    def get_queryset(self):
        #print(self.request.user) # Checking the request user using Session authentication
        qs = Status.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class StatusAPIView(mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     mixins.RetrieveModelMixin,
#                     generics.ListAPIView):
#
#     permission_classes = []
#     authentication_classes = []
#     serializer_class = StatusSerializer
#     passed_id = None
#
#
#     def get_queryset(self):
#         qs = Status.objects.all()
#         query = self.request.GET.get('q')
#
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#         return qs
#
#
#
#     #...2nd portion..
#
#     def get_object(self):
#         request = self.request
#         passed_id = request.GET.get('id', None) or self.passed_id
#         queryset = self.get_queryset()
#         obj = None
#
#         if passed_id is not None:
#             obj = get_object_or_404(queryset, id=passed_id)
#             self.check_object_permissions(request, obj)
#         return obj
#
#     def get(self, request, *args, **kwargs):
#
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#
#         if is_json(body_):
#             json_data = json.loads(request.body)
#
#         new_passed_id = json_data.get('id', None)
#
#         #print(request.body)
#
#         passed_id = url_passed_id or new_passed_id or None #For cfe command output...
#
#         self.passed_id = passed_id
#
#         if passed_id is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return super().get(request, *args, **kwargs)
#
#
#     def post(self, request, *args, **kwargs):
#
#         #url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#
#         if is_json(body_):
#             json_data = json.loads(request.body)
#
#         #new_passed_id = json_data.get('id', None)
#
#         # print(request.body)
#
#         #passed_id = url_passed_id or new_passed_id or None  # For cfe command output...
#
#         #self.passed_id = passed_id
#
#         return self.create(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#
#         if is_json(body_):
#             json_data = json.loads(request.body)
#
#         new_passed_id = json_data.get('id', None)
#
#         #print(request.data)
#
#         requested_id = request.data.get('id')
#
#         passed_id = url_passed_id or requested_id or new_passed_id or None  # For cfe command output...
#
#         self.passed_id = passed_id
#
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#
#         if is_json(body_):
#             json_data = json.loads(request.body)
#
#         new_passed_id = json_data.get('id', None)
#
#         # print(request.body)
#
#         passed_id = url_passed_id or new_passed_id or None  # For cfe command output...
#
#         self.passed_id = passed_id
#         return self.update(request, *args, **kwargs)
#
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
#     def perform_destroy(self, instance):
#         if instance is not None:
#             return instance.delete()
#         return None
#
#
#     def perform_update(self, serializer):
#         serializer.save(updated_by_user = self.request.user)
#
#
#     def delete(self, request, *args, **kwargs):
#
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#
#         if is_json(body_):
#             json_data = json.loads(request.body)
#
#         new_passed_id = json_data.get('id', None)
#
#         # print(request.body)
#
#         passed_id = url_passed_id or new_passed_id or None  # For cfe command output...
#
#         self.passed_id = passed_id
#
#         return self.destroy(request.body, *args, **kwargs)


class StatusCreateAPIView(generics.CreateAPIView):

    permission_classes = []
    authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)


class StatusRetriveAPIView(generics.RetrieveAPIView):

    permission_classes = []
    authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    #lookup_field = 'id' # 'slug field' #lookup_field is used for custom dynamic url

    def get_object(self, *args, **kwargs): #This one is faster than upper method
        kwargs = self.kwargs
        kw_id = kwargs.get('id')
        return Status.objects.get(id=kw_id)


class StatusUpdateAPIView(generics.UpdateAPIView):

    permission_classes = []
    authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusDeleteAPIView(generics.DestroyAPIView):

    permission_classes = []
    authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer



#Mixins


class StatusMixinsView(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):

    permission_classes = []
    authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


'''
class StatusMixinsView(generics.RetrieveUpdateDestroyAPIView): #Do the same as above class

    permission_classes = []
    authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

'''


#...Practicing...

from users.models import User
from users.api.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

class StaffDetection(APIView):

    def get(self, request):

        qs = User.objects.filter(username="minhaj")
        serializer = UserSerializer(qs, many=True)

        json_data = JSONRenderer().render(serializer.data)
        stream = BytesIO(json_data)
        data = JSONParser().parse(stream)

        is_staff = data[0]['is_staff']

        context = {
            "is_staff": is_staff
        }

        return Response(context, status=status.HTTP_200_OK)



















