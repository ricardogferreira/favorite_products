# FAVORITE PRODUCTS
Api para para gerenciar cliente e produtos favoritos

### Docker
Fazer o build da imagem: `docker build --tag favorite_products:0.1 .`

Para subir a imagem utilize o comando:
`docker run --publish 5000:5000 --rm --name nome_da_aplicacao favorite_products:0.1`

A aplicação vai rodar na porta 5000

## Docker-compose
### Com o docker-compose você consegue subir o ambiente completo, com persistência de dados.

Primeiramente é preciso fazer o build, utilize o comando `docker-compose build`

Para subir o ambiente execute o comando `docker-compose up`

Comandos podem serem executados dentro do container da seguinte forma: `docker-compose exec app <comando>`

A aplicação vai rodar na porta 5000

## Instalação local sem docker e docker-compose
Utilizando o pyenv ou virtualenv crie um ambiente virtual, utilize o python3.7

#### Comando virtualenv
Criar ambiente: `virutalenv -p python3.7 .venv`

Ativar ambiente: `source .venv/bin/activate`

#### Comando pyenv
Criar ambiente `pyenv virtualenv 3.7.9 favorite_products_env`

Ativar ambiente: `pyenv activate favorite_products_env`

Instale as dependências: `pip install -r requirements.txt`

para rodar o server utilize o comando `make serve`

Obs: Executando dessa forma o banco de dados a ser utilizado por padrão vai ser o sqlite.
A conexão com o banco de dados pode ser alterado via variáveis de ambiente ou dentro do arquivo config.py

## Comandos Uteis

Rodar validação do pep8: `make pep8`

Fazer correção de imports: `make fix-import`

Executar teste sem coverage: `make test`

Executar teste e coverage: `make coverage`

Executar coverage com detalhes: `make coverage-report`

Executar servidor de desenvolvimento: `make serve`

Comando para criar migrações do banco de dados: `flask db migrate`

Comando para instalar migrações: `flask db upgrade`


## Variáveis de ambiente disponíveis para configuração
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_ADDRESS=localhost
POSTGRES_DB=favorite_products
SECRET_KEY=my_secret_key
FLASK_APP=app
FLASK_ENV=development
CELERY_BROKER_URL=
```
Obs: Para utilizar o POSTGRES todas variáveis POSTGRES_... devem ser preenchidas.
