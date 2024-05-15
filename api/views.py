import requests
import json
from .models import Produto
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse

#@login_required(login_url="api/login")
def index(request):    
    # Gera queryset do banco de dados e faz display no html
    data        = Produto.objects.all()
    paginator   = Paginator(data, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj    = paginator.get_page(page_number)
    
    if not data:
        return render(request, 'api/index.html', {'data': page_obj})
    else:
        return render(request, 'api/index.html', {'data': page_obj})

def fetch_data(request):
    
    payload = {
        "PAGINA": 1,
        "PORPAGINA": 100,
            "QUERY": "SELECT CASE WHEN (CB7_DIVERG='1') THEN '4' WHEN (CB7_STATPA = '1' AND CB7_DIVERG='') THEN '3' WHEN (CB7_STATUS IN ('1','2','3','4','5','6','7','8') AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '2' WHEN (CB7_STATUS = '0' AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '1' WHEN (CB7_STATUS = '9' AND CB7_STATPA = '' AND CB7_DIVERG='') THEN '0' END AS CB7_STATUS, CB7010.CB7_FILIAL, CB7010.CB7_ORDSEP, CB7010.CB7_PEDIDO, CB7010.CB7_CLIENT, CB7010.CB7_LOJA, SA1010.A1_NOME, CB7010.CB7_DTEMIS, CB7010.CB7_HREMIS, CB7010.CB7_DTINIS, CB7010.CB7_HRINIS, CB7010.CB7_DTFIMS, CB7010.CB7_HRFIMS, CB7010.CB7_NOTA, CB7010.CB7_SERIE, CB8010.CB8_PROD, SB1010.B1_DESC FROM CB7010 INNER JOIN CB8010 ON CB8_FILIAL = CB7010.CB7_FILIAL AND CB8_ORDSEP = CB7010.CB7_ORDSEP AND CB8_PEDIDO = CB7010.CB7_PEDIDO AND CB8010.D_E_L_E_T_ = '' INNER JOIN SA1010 ON A1_COD = CB7010.CB7_CLIENT AND A1_LOJA = CB7010.CB7_LOJA AND SA1010.D_E_L_E_T_ = '' INNER JOIN SB1010 ON B1_COD = CB8010.CB8_PROD AND SB1010.D_E_L_E_T_ = '' WHERE 0=0 AND CB7010.CB7_DTEMIS BETWEEN '20240508' AND '20240508' AND CB7010.D_E_L_E_T_ = ''",
            "ORDEM": "CB7_STATUS, CB7_ORDSEP, CB7_PEDIDO"
    }
    response = requests.post('http://suntechsupplies170773.protheus.cloudtotvs.com.br:1907/rest/restqry', json=payload)
    queryset_response = response.json()
    aux = []
    new_records_count = 0

    for produto in queryset_response['RETORNOS']:
       if not Produto.objects.filter(CB7_ORDSEP=produto["CB7_ORDSEP"]).exists():
            obj = Produto(            
                    CB7_STATUS  = produto["CB7_STATUS"],
                    CB7_FILIAL  = produto["CB7_FILIAL"],
                    CB7_ORDSEP  = produto["CB7_ORDSEP"],
                    CB7_PEDIDO  = produto["CB7_PEDIDO"],
                    CB7_CLIENT  = produto["CB7_CLIENT"],
                    CB7_LOJA    = produto["CB7_LOJA"],
                    A1_NOME     = produto["A1_NOME"],
                    CB7_DTEMIS  = produto["CB7_DTEMIS"],
                    CB7_HREMIS  = produto["CB7_HREMIS"],
                    CB7_DTINIS  = produto["CB7_DTINIS"],
                    CB7_HRINIS  = produto["CB7_HRINIS"],
                    CB7_DTFIMS  = produto["CB7_DTFIMS"],
                    CB7_HRFIMS  = produto["CB7_HRFIMS"],
                    CB7_NOTA    = produto["CB7_NOTA"],
                    CB7_SERIE   = produto["CB7_SERIE"],
                    CB8_PROD    = produto["CB8_PROD"],
                    B1_DESC     = produto["B1_DESC"],
                    LINE        = produto["LINE"]
                )
            aux.append(obj)
            new_records_count =+ 1
    print(f"{new_records_count} cadastrado")

    Produto.objects.bulk_create(aux)
    
@csrf_exempt
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return redirect('api/index.html')
        else:
            return render(request, 'api/login.html')
    else:
        return render(request, 'api/login.html')
    
    
@csrf_exempt
def update_status_counts(request):
    fetch_data(request)

    status_counts = {
        '1': str(Produto.objects.filter(CB7_STATUS=1).count()),
        '2': str(Produto.objects.filter(CB7_STATUS=2).count()),
        '0': str(Produto.objects.filter(CB7_STATUS=0).count()),
        '3': str(Produto.objects.filter(CB7_STATUS=3).count()),
        '4': str(Produto.objects.filter(CB7_STATUS=4).count()),
    }
    print(status_counts)
    

    return JsonResponse(status_counts)