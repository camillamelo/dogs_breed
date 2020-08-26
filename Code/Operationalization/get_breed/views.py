from get_breed.models import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from get_breed.serializers import *
import requests
import pandas as pd
import cv2
import urllib.request
import numpy as np
from matplotlib import pyplot as plt
import pickle
PROJECT_FOLDER = 'C:/Users/cammy/OneDrive/MIT IA/git/projeto_dogs/dogs_brand'
img_h, img_w = 64, 64 # Altura e largura das imagens

class PicturesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer

class ClassifyBreed(APIView):
  """
  """
  def get(self, request):
    """
    Return the refurbishments
    """
    try:
        address = request.query_params['urladdress']

        # Convert Images
        req = urllib.request.urlopen(address)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr,0)
        imres = cv2.resize(img, (img_h, img_w), interpolation=cv2.INTER_CUBIC)
        photo = imres.flatten()

        # Load models
        model_file = PROJECT_FOLDER + '/Data/Modeling/trained_models.jbl'
        with open(model_file, 'rb') as fid:
            model_pipe = pickle.load(fid)

        #ClassifyBreed
        photos = []
        photos.append(photo)
        breed = model_pipe.predict(photos)

        # Save forecast objects
        # for dt, estimate in forecast.iteritems():
        #     obj,flag = Forecasts.objects.get_or_create(date=dt,
        #                                                forecast_model=forecastmodel)
        #     obj.estimated_cases=estimate
        #     obj.save()
        #
        # forecast_objs = [obj for obj in Forecasts.objects.filter(forecast_model=forecastmodel)
        #                  if obj.date >= forecastmodel.train_last_date]
        # serial_data = ForecastsSerializer(forecast_objs,
        #                                    many=True,
        #                                    context={'request': request})

        return Response(breed, status=status.HTTP_200_OK)

    except Exception as err:
        return Response('Detailed Error: ' + err.__str__(), status = status.HTTP_400_BAD_REQUEST)
