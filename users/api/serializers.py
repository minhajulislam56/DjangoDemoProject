from rest_framework import serializers
from users.models import file_list, quotes, ImageFile, Status


class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = file_list
    fields = ('file', 'remark', 'timestamp')

class QuoteSerializer(serializers.ModelSerializer):
  class Meta():
    model = quotes
    fields = ('body', 'category', 'posted_on')



class ImageSerializer(serializers.ModelSerializer):
  class Meta():
    model = ImageFile
    fields = '__all__'

    #read_only_fields = ['remark']

  #VALIDATION PORTION...
  '''def validate_remark(self, request):
    qs = file_list.objects.filter(remark__iexact=request)

    if qs:
      raise serializers.ValidationError('File name must be unique')
    else:
      return request'''


class StatusSerializer(serializers.ModelSerializer):
  class Meta:
    model = Status
    fields = [
      'user',
      'content',
      'image'
    ]

    '''
    VALIDATION IN THE SERIALIZER...
    
    def validate_content(self, value):
      if len(value) > 10000:
        raise serializers.ValidationError("Too much long content")
      return value

    def validate(self, data):

      content = data.get('content', None)
      if content == "":
        content = None

      image = data.get('image', None)
      if content is None and image is None:
        raise serializers.ValidationError('Required fields are not filled up!')
      return data
    
    '''