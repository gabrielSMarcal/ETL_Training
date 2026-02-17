from dotenv import load_dotenv

import base64
import requests
import os

load_dotenv()

class ManipulaRepositorios:
    
    def __init__(self, username):
        
        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.access_token = os.getenv('GITHUB_ACCESS_TOKEN')
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'X-GitHub-Api-Version': '2022-11-28'
        }
        
    def cria_repo(self, nome_repo, descricao_repo='Repositório criado via API'):
        
        data = {
            'name': nome_repo,
            'description': descricao_repo,
            'private': False
        }
        response = requests.post(f'{self.api_base_url}/user/repos',
                                 json=data, headers=self.headers)
        
        print(f'Status Code Criação de Repositório: {response.status_code}')
        
    def add_arquivo(self, nome_repo, nome_arquivo,
                    caminho_arquivo, messagem_commit='Adicionando arquivo via API'):
        
        with open(caminho_arquivo, 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)
        
        url = f'{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}'
        data = {
            'message': messagem_commit,
            'content': encoded_content.decode('utf-8')
        }
        
        response = requests.put(url, json=data, headers=self.headers)
        print (f'Status Code Adição de Arquivo: {response.status_code}')
        