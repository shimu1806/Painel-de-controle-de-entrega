import requests
import json
from datetime import datetime, timedelta

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

    today_str = datetime.now().strftime('%Y%m%d')
    display_today_str = datetime.now().strftime('%d-%m-%Y')

    lastweek_str = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    display_lastweek_str = (datetime.now() - timedelta(days=7)).strftime('%d-%m-%Y')

    print (f'Filtrando a partir do dia: {display_lastweek_str} ao dia {display_today_str}\n\n')

    payload = {
        "PAGINA": 1,
        "PORPAGINA": 1000,
        "QUERY": f"SELECT CASE WHEN (CB7_DIVERG='1') THEN '4' WHEN (CB7_STATPA = '1' AND CB7_DIVERG='') THEN '3' WHEN (CB7_STATUS IN ('1','2','3','4','5','6','7','8') AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '2' WHEN (CB7_STATUS = '0' AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '1' WHEN (CB7_STATUS = '9' AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '0' END AS CB7_STATUS, CB7010.CB7_FILIAL, CB7010.CB7_ORDSEP, CB7010.CB7_PEDIDO, CB7010.CB7_CLIENT, CB7010.CB7_LOJA, SA1010.A1_NOME, (SELECT C5_ZZTPPED  FROM SC5010 WHERE C5_FILIAL = CB7_FILIAL AND C5_NUM = CB7_PEDIDO  AND SC5010.D_E_L_E_T_ = '') AS CB7_TPPED, CB7010.CB7_DTEMIS, CB7010.CB7_HREMIS, CB7010.CB7_DTINIS, CB7010.CB7_HRINIS, CB7010.CB7_DTFIMS, CB7010.CB7_HRFIMS, CB7010.CB7_NOTA, CB7010.CB7_SERIE, (SELECT SUM(CB8_SALDOS) FROM CB8010 WHERE  CB8_FILIAL = CB7_FILIAL AND CB8_PEDIDO = CB7_PEDIDO AND CB8010.D_E_L_E_T_ = '') AS CB8_TOTAL FROM CB7010 INNER JOIN SA1010 ON A1_COD = CB7010.CB7_CLIENT AND A1_LOJA = CB7010.CB7_LOJA AND SA1010.D_E_L_E_T_ = '' WHERE 0=0 AND CB7010.CB7_DTEMIS BETWEEN '{lastweek_str}' AND '{today_str}' AND CB7010.D_E_L_E_T_ = ''",
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
    