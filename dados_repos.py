from math import ceil
from dotenv import load_dotenv

import os
import pandas as pd
import requests

load_dotenv()

class DadosRepositorios:
    
    def __init__(self, owner):
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.auth_token = os.getenv('GITHUB_ACCESS_TOKEN')
        self.headers = {
            'Authorization': 'Bearer ' + self.auth_token,
            'X-GitHub-Api-Version': '2022-11-28'
        }
    
    def lista_repositorios(self):
        lista_repos = []
        
        response = requests.get(f'{self.api_base_url}/users/{self.owner}')
        num_pages = ceil(response.json()['public_repos'] / 30)
        
        for page_num in range(1, num_pages + 1):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                lista_repos.append(response.json())
            except:
                lista_repos.append(None)
        
        return lista_repos
    
    def nomes_repos(self, repos_list):
        nomes_repos = []
        
        for page in repos_list:
            if page is not None:
                try:
                    for repo in page:
                        nomes_repos.append(repo['name'])
                except:
                    pass
                
        return nomes_repos
    
    def nome_linguagens(self, repos_list):
        repo_linguagens = []
        
        for page in repos_list:
            if page is not None:
                try:
                    for repo in page:
                        repo_linguagens.append(repo['language'])
                except:
                    pass
                
        return repo_linguagens
    
    def cria_df_linguagens(self):
        
        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nome_linguagens(repositorios)
        
        dados = pd.DataFrame()
        dados['nome_repositorio'] = nomes
        dados['linguagem'] = linguagens
        
        dados.to_csv(f'data/linguagens_{self.owner}.csv')
        print(f'Dados de linguagens para {self.owner} salvos com sucesso!')
        
        return dados
    
amazon_rep = DadosRepositorios('amzn')
ling_mais_usadas_amzn = amazon_rep.cria_df_linguagens()
# print(ling_mais_usadas_amzn)

netflix_rep = DadosRepositorios('netflix')
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagens()
# print(ling_mais_usadas_netflix)

spotify_rep = DadosRepositorios('spotify')
ling_mais_usadas_spotify = spotify_rep.cria_df_linguagens()
# print(ling_mais_usadas_spotify)