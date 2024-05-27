import requests
import json

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@login_required(login_url="/login")
def index(request):
    return render(request, 'api/index.html')


@csrf_exempt
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return render(request, 'api/index.html')
        else:
            return render(request, 'api/login.html')
    else:
        return render(request, 'api/login.html')


def api_fetch(request):
    payload = {
        "PAGINA": 1,
        "PORPAGINA": 8000,
        "QUERY": "SELECT CASE WHEN (CB7_DIVERG='1') THEN '4' WHEN (CB7_STATPA = '1' AND CB7_DIVERG='') THEN '3' WHEN (CB7_STATUS IN ('1','2','3','4','5','6','7','8') AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '2' WHEN (CB7_STATUS = '0' AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '1' WHEN (CB7_STATUS = '9' AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '0' END AS CB7_STATUS, CB7010.CB7_FILIAL, CB7010.CB7_ORDSEP, CB7010.CB7_PEDIDO, CB7010.CB7_CLIENT, CB7010.CB7_LOJA, SA1010.A1_NOME, CB7010.CB7_DTEMIS, CB7010.CB7_HREMIS, CB7010.CB7_DTINIS, CB7010.CB7_HRINIS, CB7010.CB7_DTFIMS, CB7010.CB7_HRFIMS, CB7010.CB7_NOTA, CB7010.CB7_SERIE, CB8010.CB8_PROD, SB1010.B1_DESC FROM CB7010 INNER JOIN CB8010 ON CB8_FILIAL = CB7010.CB7_FILIAL AND CB8_ORDSEP = CB7010.CB7_ORDSEP AND CB8_PEDIDO = CB7010.CB7_PEDIDO AND CB8010.D_E_L_E_T_ = '' INNER JOIN SA1010 ON A1_COD = CB7010.CB7_CLIENT AND A1_LOJA = CB7010.CB7_LOJA AND SA1010.D_E_L_E_T_ = '' INNER JOIN SB1010 ON B1_COD = CB8010.CB8_PROD AND SB1010.D_E_L_E_T_ = '' WHERE 0=0 AND CB7010.CB7_DTEMIS BETWEEN '20240520' AND '20240527' AND CB7010.D_E_L_E_T_ = ''",
        "ORDEM": "CB7_STATUS, CB7_ORDSEP, CB7_PEDIDO"
    }
    response = requests.post('http://suntechsupplies170773.protheus.cloudtotvs.com.br:1907/rest/restqry', json=payload)

    # Parse the JSON response
    queryset_response = response.json()
   
    # Extract the items within the 'RETORNOS' key
    return_items = queryset_response.get('RETORNOS', [])

    return return_items


def fetch_data(request):
    return_items = api_fetch(request)    
    
    # Return the extracted items as a JsonResponse
    return JsonResponse(return_items, safe=False)


@csrf_exempt
def update_status_counts(request):
    return_items = api_fetch(request)

    status_counts = {
        '1': 0,
        '2': 0,
        '0': 0,
        '3': 0,
        '4': 0,
    }

    for item in return_items:
        status = item.get('CB7_STATUS')
        if status in status_counts:
            status_counts[status] += 1


    # Return the counted status as a JsonResponse
    return JsonResponse(status_counts)
    