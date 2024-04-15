import requests
import json

response = requests.get('https://vuzopedia.ru/vuz/509/poege/egemat;egerus;egeobsh;')
print(response.status_code)
letters = 'ЙЦУФЫВЯЧСМИТАПРКЕНГОЬШЛБЩДЮЗЖХЭЪйцукенгшщзхъэждлорпавыфячсмитьбю '
print(response.text)