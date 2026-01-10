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

# INICIO DO SCRAPER

url = 'https://www.python.org/jobs'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac Os X 10_15_7)'
}
print('Iniciando VagaBot...')
response = requests.get(url, headers=headers)

print(f'Status da resposta do site: {response.status_code}')

# 200: sucesso
# 403: negado
# 404: nao encontrado

print(f'Status da resposta: {response.status_code}')
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    lista_de_vagas = soup.find('ol', class_ = 'list-recent-jobs')
    todas_as_vagas = lista_de_vagas.find_all('li')

    dados_vagas = []
    print(f'Site acessado! Processando {len(todas_as_vagas)} vagas...\n')

    for vaga in todas_as_vagas:
        titulo_tag = vaga.find('a')
        local_tag = vaga.find('span', class_='listing-location')

        if titulo_tag and local_tag:
            titulo = titulo_tag.text.strip()
            local = local_tag.text.strip()
            link = 'https://www.python.org' + titulo_tag['href']

            #filtrar vagas que sejam no brasil, remotas ou que nao sejam senior/lead
            titulo_lower = titulo.lower()    
            local_lower = local.lower()

            #if 'brazil' in local_lower or 'remote' in local_lower:
            if 'brazil' in local_lower:
                msg_final = f"🔥 VAGA ENCONTRADA!\n\nCargo: {titulo}\nLocal: {local}\nLink: {link}"
                vaga_dict = {
                    'Cargo': titulo,
                    'Localização': local,
                    'Link': link 
                }
                dados_vagas.append(vaga_dict)
                print(f"Enviando alerta: {titulo}...")
                enviar_telegram(msg_final)

                time.sleep(1) #recurso pro telegram não bloquear as solicitações
        
    if dados_vagas:
        df = pd.DataFrame(dados_vagas)
        df.to_csv('vagas_encontradas.csv', index=False)
        print(f'\nSucesso! Verifique seu Telegram e o arquivo CSV.')
    else:
        print('Nenhuma vaga correspondeu aos filtros.')

else:
    print('Erro ao acessar o site.')