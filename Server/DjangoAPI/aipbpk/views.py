from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import sqlite3
import numpy as np
import pandas as pd

from django.core.files.storage import default_storage
# from aipbpk.Handlers.MLModelLoaders import getModels
# from aipbpk.Handlers.DataLoader import GetData
# from aipbpk.Handlers.Predictor import prediction

from aipbpk.tasks.tasks import long_running_task
from celery.result import AsyncResult


import os
from dotenv import load_dotenv
import json

load_dotenv()


# Create your views here.
@csrf_exempt
def test(request,id=0):
    if request.method=='GET':
        print(os.environ.get('DB_HOST'))
        print(os.environ.get('tesval'))
        return JsonResponse("Get request",safe=False)
    elif request.method=='POST':
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        return JsonResponse("Deleted Successfully",safe=False)


# Create your views here.
@csrf_exempt
def getVariblesList(request, id=0):
    if request.method == 'GET':
        datasetPath = 'static/Data_Dictionary_-__Annotated__26Sep2023.csv'
        df = pd.read_csv(datasetPath)
        df_1 = df.copy()
        df_1.dropna(subset=['ITM_NAME'], inplace=True)
        df_1 = df_1[df_1['ITM_NAME'] != ' ']
        df_1 = df_1.drop_duplicates(subset = 'ITM_NAME')
        variable_list = df_1['ITM_NAME'].tolist()
        variable_list.remove('CNO')
        variable_list.remove('EVENT_ID')
        variable_list.remove('LAST_UPDATE')
        variable_list.remove('PAG_NAME')
        variable_list.remove('PATNO')
        variable_list.remove('REC_ID')

        remove = ['CNO', 'EVENT_ID', 'LAST_UPDATE', 'PAG_NAME', 'PATNO', 'REC_ID']
        df_1 = df_1[~df_1.ITM_NAME.isin(remove)]
        table_variables = df_1[['MOD_NAME', 'ITM_NAME']]

        # Convert DataFrame to dictionary
        grouped = table_variables.groupby('MOD_NAME')['ITM_NAME'].apply(list).to_dict()
        
        # Return the frequencies as JSON
        return JsonResponse({'varibles': variable_list, 'files': grouped}, safe=False)

@csrf_exempt
def getDataFromVariblesList(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        task = long_running_task.delay(data)
        
        return JsonResponse({'task_id': task.id})
        
@csrf_exempt
def check_task_status(request, task_id):
    if request.method == 'GET':
        print('task_id4444444444444444444444444444444444')
        print('task_id',task_id)
        try:
            result = AsyncResult(task_id)
            response_data = {
                'task_status': result.status,
                'task_result': result.result if result.successful() else str(result.result)
            }
        except ValueError as e:
            response_data = {
                'task_status': 'ERROR',
                'task_result': str(e)
            }
        return JsonResponse(response_data)