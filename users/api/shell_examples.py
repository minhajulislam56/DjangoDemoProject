

from users.api.serializers import StatusSerializer
from users.models import Status

'''
 'user': UUID('a44787d8-f09d-4ff4-9557-2d1852fe4f97')
'''

data = {'user': 'a44787d8-f09d-4ff4-9557-2d1852fe4f97', 'content': 'Testing the serializer'} #custom one is token
serializer = StatusSerializer(data=data)
serializer.is_valid()
create_obj = serializer.save() #instance of the object
print(create_obj)

'''
Update Objects
'''
obj = Status.objects.first()
data = {'content': 'some new content'}
serializer = StatusSerializer(obj, data=data)
serializer.is_valid()


#KEMON DILAM :p

import json
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

qs = Status.objects.all()
serializer = StatusSerializer(qs, many=True)
serializer.data

json_data = JSONRenderer().render(serializer.data)

json.loads(json_data)

stream = BytesIO(json_data)
data = JSONParser().parse(stream)



#CUSTOM SERIALIZER -> won't save in the database

from rest_framework import serializers

class CustomSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField()


data = {'email': 'minhaj@gmail.com', 'content': 'custom serializers'}
obj_serializer = CustomSerializer(data=data)
if obj_serializer.is_valid():
    data = obj_serializer.data
    print(data)


