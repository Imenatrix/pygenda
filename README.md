# pygenda
Programa de agenda concebido para a disciplina de Banco de Dados do curso de Técnico em Informática do IFPR - Campus Paranaguá da turma INFO19.

## Dependencias

- MySQL
- python 3.6+
- mysql-connector-python
- getch
- fuzzywuzzy

o programa foi escrito e testado no python 3.9.2,
compatilibidade com versões anteriores é esperada,
mas não garantida.

para as outras dependencias pode ser instaladas
com os seguintes comandos:

```
pip install mysql-connector-python
pip install getch
pip install fuzzywuzzy
```

## Instruções

1. [opcional] execute pygenda.sql em um banco de dados
compativel com MySQL, esse script vai gerar um schema
chamado "pygenda" com as tabelas necessarias para o
funcionamento do programa.

2. edite config.json de acordo com o banco de dados disponivel,
certifique-se que o usuario utilizado tenha permissões de
inserção, edição e deleção no schema selecionado; certifique-se
que o schema selecionado é compativel com o schema descrito
em pygenda.sql.

3. execute o programa com o seguinte comando:

```
python main.py
```

em algumas distribuições linux, o executavel "python"
refere-se ao python 2.7.x e o programa terminará com erro,
nesse caso tente:

```
python3 main.py
```
