import requests

# COLE SEU TOKEN AQUI DENTRO DAS ASPAS
TOKEN = "8399654376:AAGj3SKBUYDWoH-IwwJGKYSa8ag4AGIIXyM" 

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

print("Verificando mensagens...")
response = requests.get(url)
dados = response.json()

if dados["result"]:
    # Pega o ID da primeira pessoa que falou com o bot
    chat_id = dados["result"][0]["message"]["chat"]["id"]
    nome = dados["result"][0]["message"]["chat"]["first_name"]
    
    print(f"--- SUCESSO! ---")
    print(f"Mensagem recebida de: {nome}")
    print(f"SEU CHAT ID É: {chat_id}")
    print("Guarde este número!")
else:
    print("O bot ainda não recebeu mensagens. Vá no Telegram e mande um 'Oi' para ele primeiro.")