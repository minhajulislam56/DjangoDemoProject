from rest_framework import permissions, generics
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializers import RegisterUserSerializer

from rest_framework_jwt.settings import api_settings



# from .utils import jwt_response_payload_handler   # Relative import

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()

class AuthAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        # print(request.user)
        if request.user.is_authenticated:
            return Response({"detail" : "You are authenticated"})

        data = request.data
        username = data.get('username')
        password = data.get('password')
        # user = authenticate(username = username, password = password)
        # print(user)

        qs = User.objects.filter(
            Q(username__iexact = username)|
            Q(email__iexact = username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj

                #Creating a new token manually
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request= request)
                return Response(response, status = status.HTTP_200_OK)

        return Response({"Detail" : "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)




class RegisterAPIView(generics.CreateAPIView):

    permission_classes = [permissions.AllowAny]

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer




# class RegisterAPIView(APIView):
#
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#
#         if request.user.is_authenticated:
#             return Response({"Detail" : "You are already authenticated"})
#
#         data = request.data
#
#         username = data.get('username') # username or email address
#         email = data.get('username')
#         password = data.get('password')
#         password2 = data.get('password2')
#
#         qs = User.objects.filter(
#             Q(username__iexact = username)|
#             Q(email__iexact = username)
#         )
#         if password != password2:
#             return Response({"Password": "Passwords don't matched"})
#         if qs.exists():
#             return Response({"Detail": "This user already exists!"})
#         else:
#             user = User.objects.create(username = username, email = email)
#             user.set_password(password)
#             user.save()
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             response = jwt_response_payload_handler(token, user, request=request)
#             return Response(response, status=status.HTTP_201_CREATED)
#         return Response({"Detail": "Invalid request"})



















