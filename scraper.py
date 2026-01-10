import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def enviar_telegram(mensagem):
    url_api = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': mensagem}
    requests.post(url_api, data=data)

def scrap_python_org():
    url = 'https://www.python.org/jobs'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac Os X 10_15_7)'}
    response = requests.get(url, headers=headers)
    print(f'Status da resposta do site: {response.status_code}')
    lista_vagas_python = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lista_de_vagas = soup.find('ol', class_ = 'list-recent-jobs')
        todas_as_vagas = lista_de_vagas.find_all('li')
        print(f'Site acessado! Processando {len(todas_as_vagas)} vagas...\n')

        for vaga in todas_as_vagas:
            titulo_tag = vaga.find('a')
            local_tag = vaga.find('span', class_='listing-location')

            if titulo_tag and local_tag:
                titulo = titulo_tag.text.strip()
                local = local_tag.text.strip()
                link = 'https://www.python.org' + titulo_tag['href']
                local_lower = local.lower()

                #filtrando apenas vagas no Brasil:
                if 'brazil' in local_lower:
                    vaga_dict = {
                        'Cargo': titulo,
                        'Localização': local,
                        'Link': link 
                    }
                    lista_vagas_python.append(vaga_dict)
    else:
        print('Erro ao acessar o site.')

    return lista_vagas_python #cada vaga tem seu dict


if __name__ == "__main__":
    vagas_total = []
    vagas_total.extend(scrap_python_org())
    #vagas_total.extend(scrap_sites_sjc())

    if vagas_total:
        df = pd.DataFrame(vagas_total)
        df.to_csv('vagas_encontradas.csv', index=False)
        for vaga in vagas_total:
            msg_final = f"🔥 VAGA ENCONTRADA!\n\nCargo: {vaga['Cargo']}\nLocal: {vaga['Localização']}\nLink: {vaga['Link']}"
            print(f"Enviando alerta: {vaga['Cargo']}...")
            enviar_telegram(msg_final)                
            time.sleep(1) #recurso pro telegram não bloquear as solicitações
        print(f'\nSucesso! Verifique seu Telegram e o arquivo CSV.')
    else:
        print('Nenhuma vaga correspondeu aos filtros.')