# Sistema de Cadastro de Pessoas com interface gráfica
O objetivo desse projeto é aprender um pouco sobre interface gráfica em python utilizando o módulo CustomTkInter

## ATENÇÃO

Todos os dados do banco de dados foram coletados do https://www.4devs.com.br/gerador_de_pessoas

## Como executar?

Necessário ter o python instalado

Na primeira execução, abra o "criar_ambiente_virtual.bat" e em seguida o "START.vbs"

Nas seguintes execuções abra somente o "START.vbs"

## Erro ao abrir "criar_ambiente_virtual.bat"?

caso não funcione a criação do ambiente virtual por esse arquivo

1. abra a pasta do projeto no VSCode
2. vá até o terminal
3. copia e cola os comandos no presentes no arquivo "comandos_ambiente_virtual.txt"

## Módulos utilizados

- customtkinter - interface grafica\
[Acessar Documentação](https://customtkinter.tomschimansky.com/documentation/)
- datetime - manipular data e hora\
[Acessar Documentação](https://docs.python.org/pt-br/3/library/datetime.html)
- PyCEP - coletar dados do CEP\
[Acessar Documentação](https://pypi.org/project/pycep/)
- SQLAlchemy - manipular o banco de dados\
[Acessar Documentação](https://docs.sqlalchemy.org/en/20/)
- validate_docbr - validader CPF\
[Acessar Documentação](https://pypi.org/project/validate-docbr/)

## Comandos para criar o ambiente virtual terminal VSCode

1. Abra a pasta do projeto no VisualStudioCode

2. instalar o virtualenv\
`pip install virtualenv`

3. criar o ambiente virtual\
`virtualenv venv -p 3.12.6`

4. navegar até a pasta do ambiente virtual\
`cd venv\Scripts`

5. ativar o ambiente virtual\
`activate`

6. instalar os módulos necessários\
`pip install -r ..\..\requirements.txt`