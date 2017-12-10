"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.shortcuts import render
from django.views.generic import View
from final_project import Processor

import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = json.load(open(BASE_DIR + '/final_project/strategy-stock.json'))
print(data)


# Create your views here.
class HomePageView(View):
    def get(self, request, **kwargs):
        return render(request, "index.html", context=None)


class PrintPageView(View):

    def post(self, request, **kwargs):
        print("================")
        print("total:" + request.POST["total"])
        print("strategy:" + request.POST["strategy"])
        total_money = float(request.POST["total"])
        strategy = request.POST["strategy"]
        company_list = data[strategy]
        # print(company_list)
        '''
        [ 
            {'name': 'AAPL', 'portion': '30', 'result':['1503.81', '1502.39', '1496.81', '1499.56', '1500.00']}, 
            {'name': 'ADBE', 'portion': '30', 'result':['1503.81', '1502.39', '1496.81', '1499.56', '1500.00']}, 
            {'name': 'AQQQ', 'portion': '30', 'result':['1503.81', '1502.39', '1496.81', '1499.56', '1500.00']},
            {'name': 'TOTAL', 'portion': '100', 'result':['1503.81', '1502.39', '1496.81', '1499.56', '1500.00']}
        ]
        
        '''
        # result_list = []
        return_list = []
        total_prices = [0.0,0.0,0.0,0.0,0.0]

        for c in company_list:
            # result_list.append(Processor.processor.one_price(c["name"], total_money * float(c["portion"]) / 100 ))
            result_item = Processor.processor.one_price(c["name"], total_money * float(c["portion"]) / 100 )
            print(result_item)
            return_list.append({'name': c["name"], 'portion': c['portion'], 'result' : result_item})
            total_prices = [total_prices[i] + float(result_item[i]) for i in range(len(total_prices))]

          
        return_list.append({'name': 'TOTAL', 'portion': '100', 'result' : total_prices})  
        print(return_list)
        print('***************')

        context = return_list

        return render(request, "about.html", {"context":context})

