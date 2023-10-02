import requests
import os
import random
import string
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import socket

# Função para obter o endereço IP do site
def obter_endereco_ip(site):
    try:
        endereco_ip = socket.gethostbyname(site)
        return endereco_ip
    except socket.gaierror as e:
        print("Erro ao obter o endereço IP do site:", str(e))
        return None

# Função para obter o servidor web usado pelo site
def obter_servidor_web(url):
    try:
        response = requests.head(url)
        server = response.headers.get('Server')
        if server:
            return server
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Erro ao obter o servidor web usado pelo site:", str(e))
        return None

# Função para obter o IP real do site
def obter_ip_real_do_site(url):
    try:
        response = requests.head(url)
        ip_real = response.headers.get('X-Forwarded-For')
        if ip_real:
            return ip_real
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Erro ao obter o IP real do site:", str(e))
        return None

# Configuração do argumento da linha de comando
parser = argparse.ArgumentParser(description='Script para extrair o código fonte de um site.')
parser.add_argument('-u', '--url', type=str, help='URL do site que deseja extrair o código fonte', required=True)
args = parser.parse_args()

# URL do site a ser extraído o código fonte
url = args.url

# Adiciona o esquema "https://" à URL, se não estiver presente
if not url.startswith('http://') and not url.startswith('https://'):
    url = 'https://' + url

# Faz a requisição HTTP para obter o código fonte do site
response = requests.get(url)
html_content = response.text

# Cria um objeto BeautifulSoup para analisar o código HTML
soup = BeautifulSoup(html_content, "html.parser")

# Organiza e formata o código de forma legível
formatted_code = soup.prettify()

# Salva o código em um arquivo .txt com um nome aleatório baseado no site extraído
parsed_url = urlparse(url)
site_name = parsed_url.netloc
random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
file_name = f"{site_name}_{random_string}.txt"
with open(file_name, "w") as file:
    file.write(formatted_code)

# Lista os serviços usados pelo site
services = []
for script in soup.find_all("script"):
    if script.has_attr("src"):
        src = script["src"]
        service = os.path.basename(src)
        services.append(service)
for link in soup.find_all("link"):
    if link.has_attr("href"):
        href = link["href"]
        service = os.path.basename(href)
        services.append(service)

print("Serviços usados pelo site:", services)

# Obter e exibir o endereço IP do site
endereco_ip = obter_endereco_ip(url)
if endereco_ip:
    print("Endereço IP do site:", endereco_ip)
else:
    print("Não foi possível obter o endereço IP do site.")

# Obter e exibir o servidor web usado pelo site
servidor_web = obter_servidor_web(url)
if servidor_web:
    print("Servidor web usado pelo site:", servidor_web)
else:
    print("Não foi possível obter o servidor web usado pelo site.")

# Obter e exibir o IP real do site
ip_real = obter_ip_real_do_site(url)
if ip_real:
    print("IP real do site:", ip_real)
else:
    print("Não foi possível obter o IP real do site.")