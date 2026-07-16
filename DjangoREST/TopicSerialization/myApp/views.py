from django.views.decorators.csrf import csrf_exempt
from .serializer import UserSerializer
import io
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

@csrf_exempt
def user_create(request):
    if request.method == "POST":
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        print(stream)
        python_data = JSONParser().parse(stream)
        print(python_data)
        serializer = UserSerializer(data=python_data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
