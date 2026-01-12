# 🤖 VagaHunter - Monitor de Vagas Automatizado

O **VagaHunter** é uma ferramenta de automação (RPA) e Engenharia de Dados desenvolvida para monitorar oportunidades de emprego. Ele realiza a extração de dados (Web Scraping), filtragem inteligente e envia alertas instantâneos via Telegram.

## 🚀 Funcionalidades

- **Coleta Automatizada (ETL):** Acessa portais de vagas e extrai informações estruturadas.
- **Filtragem Inteligente:** Utiliza `Pandas` para selecionar apenas vagas relevantes (Ex: Localizadas no Brasil ou Remotas).
- **Alertas em Tempo Real:** Integração com a API do Telegram para notificação push no celular.
- **Log de Dados:** Salva histórico de vagas encontradas em CSV para análise posterior.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Web Scraping:** BeautifulSoup4, Requests
- **Tratamento de Dados:** Pandas
- **Segurança:** Python-Dotenv (Variáveis de ambiente)

## 📦 Como rodar este projeto

### Pré-requisitos
- Python 3 instalado
- Conta no Telegram (para criar o Bot)
