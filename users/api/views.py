from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from users.models import student_list, file_list, category, quotes
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse

from .serializers import FileSerializer, QuoteSerializer

from django.core import serializers



class Checking(APIView):

    def get(self, request):
        context = {
            'data': 'hello world'
        }

        return Response(context, status.HTTP_200_OK)


class deletingFile(APIView):   #DELETE FILE USING API

    def delete(self, request, pk):
        try:
            fl = ImageFile.objects.get(id=pk)
            fl.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"Sorry, File Not Found!"}, status=status.HTTP_404_NOT_FOUND)



@csrf_exempt
def deleteFile(request, pk):    #DELETING FILE USING CUSROM FUNCTION
    if request.method == 'POST':
        is_exists = ImageFile.objects.filter(id=pk).exists()

        if is_exists:
            fl = ImageFile.objects.get(id=pk)
            fl.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Sorry, File Not Found!"}, status=status.HTTP_404_NOT_FOUND)



class student_checking(APIView):

    def get(self, request, s_id):
        is_exist = student_list.objects.filter(id=s_id).exists()

        if is_exist:
            data = student_list.objects.filter(id=s_id).values('name', 'cgpa')

            return Response(data, status.HTTP_200_OK)

            # for p in data:
            #     context={
            #         "Student Name": p.name,
            #         "Current CGPA": p.cgpa
            #     }
            #     return Response(context, status.HTTP_200_OK)
        else:
            return Response({"Requested ID Not Found!"}, status.HTTP_200_OK)


import json
class quotes_view(APIView):

    def get(self, request, format=None):
        qu = quotes.objects.all().values()
        #qu = quotes.objects.order_by('id')

        #serializer = QuoteSerializer(qu, many=True)

        return Response(qu,  status=status.HTTP_200_OK)


class get_view(APIView):

    def post(self, request, pk):
        fl = quotes.objects.get(id=pk)
        srlz = QuoteSerializer(fl)
        return Response(srlz.data, status=status.HTTP_200_OK)


class quotes_view2(APIView):  #Have Error

    def get(self, request):
        qu = quotes.objects.all()
        return JsonResponse({"quotes": qu})


class FileView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        files = file_list.objects.all()
        fs = FileSerializer(files, many = True)

        # extra = files.values('file')
        # no = extra.count()
        #
        # if extra:
        #     fc={
        #
        #     }
        #     fc['Total Files:']=no
        #     x=1
        #     for p in extra:
        #         string="Not Elligible"
        #         if p['file'].endswith('.jpg'):
        #             string="Elligible"
        #         context={
        #             "File Format is": p['file'][-4:]+" / "+string,
        #             "File Name": p['file'],
        #             "Serial": x
        #         }
        #         fc['item no: '+str(x)] = context
        #         x+=1
        #
        #     #return Response(fc, status=status.HTTP_200_OK)

        return Response(fs.data, status=status.HTTP_200_OK)

class GenericView(viewsets.ViewSet):

    def list(self, request):
        queryset = file_list.objects.all()
        serializer = FileSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def quotes(self, request):
        queryset = quotes.objects.all()
        serializer = QuoteSerializer(queryset, many=True)


        # xx=queryset.values('body')
        # xa=category.objects.filter(id=cat).values('name')
        #
        # cat = list(queryset.values('category'))[0]['category']
        # for i in queryset:
        #     #cat = list(i.values('category'))[0]['category']
        #     context={
        #         'body': i['body'],
        #         'category': category.objects.filter(id=cat).values('name')
        #     }


        final_response={

        }
        x=0
        for i in serializer.data:
            get_category = list(category.objects.filter(id=i['category']).values('name'))[0]['name']
            context = {
                'body': i['body'],
                'category': get_category,
                'posted_on': i['posted_on']
            }
            final_response[str(x)] = context
            x+=1

        return Response(final_response, status=status.HTTP_200_OK)



    def oneby(selfs, request, key):
        queryset = file_list.objects.all()
        fl = get_object_or_404(queryset, pk=key)
        serializer = FileSerializer(fl)

        return Response(serializer.data, status=status.HTTP_200_OK)

class FilePUDView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'file'
    serializer_class = FileSerializer

    def get_queryset(self):
        return file_list.objects.all()


#Image Work
from .serializers import ImageSerializer
from users.models import ImageFile

class FileTask(APIView):


    def post(self, request, *args, **kwargs):
        image_serializer = ImageSerializer(data=request.data)

        #return Response(image_serializer.data, status=status.HTTP_200_OK)

        if image_serializer.is_valid():
            #image_serializer.save()
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # def delete(self, request, *args, **kwargs):
    #
    #     ims = ImageSerializer(data=request.data)
    #
    #     if ims.is_valid():
    #         im = ImageFile.objects.all()
    #         imd = ImageSerializer(im, many=True)
    #
    #         for i in imd.data:
    #             if i == ims.data:
    #                 i.delete()
    #                 return Response(i, status=status.HTTP_200_OK)



    def get(self, request):
        image = ImageFile.objects.all()
        ims = ImageSerializer(image, many=True)


        # k=1
        # data = {}
        # for i in ims.data:
        #     if i['id'] == k:
        #         data[str(k)] = {"image": i['image']}
        #         k+=1
                

        return Response(ims.data, status=status.HTTP_200_OK)



#..........Demo Project Tasks.............

from users.models import Course
from .serializers import CourseSerializer

class CourseView(APIView):

    def get(self, request, format=None):
        qs = Course.objects.all()
        serializer = CourseSerializer(qs, many=True)

        course_list = []

        for i in serializer.data:

            gen_tags = i.get("tags").split("#")
            gen_tags.remove("")

            context = {
                "course_id": i["course_id"],
                "author": i["author"],
                "is_approved": i["is_approved"],
                "outline": i["outline"],
                "prerequisits": i["prerequisits"],
                "banner": i["banner"],
                "private": i["private"],
                "tags": gen_tags,
                "title": i["title"],
                "rating": i["rating"],
                "date_created": i["date_created"],
                "date_updated": i["date_updated"],
                "fee": i["fee"]
            }

            course_list.append(context)

        return Response(course_list, status=status.HTTP_200_OK)