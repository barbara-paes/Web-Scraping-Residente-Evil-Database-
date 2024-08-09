# Web-Scraping-Residente-Evil-Database-

## Resident Evil Database

Este projeto tem como objetivo criar um dataframe contendo informações detalhadas dos personagens de Resident Evil, obtidas por meio de raspagem de dados do site [Resident Evil Database](https://www.residentevildatabase.com/). As características extraídas incluem ano de nascimento, tipo sanguíneo, altura e peso de cada personagem.

## Etapas do Projeto

### 1. Coleta Inicial de Dados

Começamos capturando a URL de um personagem em formato cURL, utilizando a ferramenta de desenvolvedor do navegador. Em seguida, convertendo o cURL para um script Python, realizamos a requisição simulando o comportamento do navegador.
![1](https://github.com/user-attachments/assets/da9629b8-4147-4e56-bdc5-e05cb807493c)
![2](https://github.com/user-attachments/assets/95608e41-745a-4cf5-9e4f-3b1fe79b801f)

O status code retornado foi 200, indicando que a requisição foi bem-sucedida. Inicialmente, obtivemos a página completa, mas nosso foco está nas características gerais do personagem.

### 2. Extração de Dados com Beautiful Soup

Utilizamos a biblioteca `Beautiful Soup` do Python para analisar o HTML da página e navegar na estrutura do documento de forma eficiente. Localizamos a `div` que contém as informações desejadas e filtramos o parágrafo específico que contém os detalhes do personagem.
![3](https://github.com/user-attachments/assets/4b146737-89e4-44ba-8aff-1238abb393ae)

```python
div_page = soup.find('div', class_='td-page-content')
paragraph = div_page.find_all('p')[1]
ems = paragraph.find_all('em')
```

As informações extraídas são formatadas como:

```html
<em>Ano de nascimento: 1974 (24 anos em 1998)</em>
<em>Tipo sanguíneo: AB</em>
<em>Altura: Desconhecida.</em>
<em>Peso: Desconhecido.</em>
```
Com essas informações, podemos agora acessar o texto de cada elemento em:

```python
ems[0].text  # Retorna 'Ano de nascimento: 1974 (24 anos em 1998)'
```

### 3. Estruturação do Código em Funções


Para facilitar a coleta dos dados de todos os personagens, organizamos o código em funções reutilizáveis. Primeiro, criamos uma função para obter o conteúdo de uma URL:


```python
def get_content(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    return response
```

Depois, criamos uma função para extrair as informações básicas de cada personagem:

```python
def get_basic_infos(soup):
    div_page = soup.find('div', class_='td-page-content')
    paragraph = div_page.find_all('p')[1]
    ems = paragraph.find_all('em')
    
    data = {}
    for i in ems:
        chave, valor = i.text.split(':')
        data[chave.strip()] = valor.strip()
    return data
```

A função get_basic_infos é projetada para extrair  informações específicas dos personagens. Ela começa localizando uma <div> com a classe 'td-page-content', que é onde o conteúdo principal da página está localizado. Dentro dessa <div>, a função seleciona o segundo parágrafo e, em seguida, busca por todas as tags <em> nesse parágrafo.

Para cada tag <em>, a função divide o texto usando ':' como separador. O texto antes dos ':' é considerado a "chave" e o texto depois é a "valor". Essas chaves e valores são então armazenados em um dicionário, com espaços extras removidos.

Por fim, a função retorna esse dicionário, que contém as informações extraídas e organizadas de forma estruturada.


### 4. Coleta de Dados de Todos os Personagens

Por fim, implementamos uma função para coletar os links de todos os personagens no site e extrair as informações de cada um. Esses dados são organizados em um dataframe e salvos em um arquivo Parquet ,pois suporta compressão de dados, o que significa que os arquivos ocupam menos espaço em disco em comparação com formatos como CSV ou JSON. Queremos uma formato mais elegante 🦄.

```python
def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url, headers=headers)
    soup_person = BeautifulSoup(resp.text, features="html.parser")
    ancoras = soup_person.find("div", class_="td-page-content").find_all("a")
    
    links = [i["href"] for i in ancoras]
    return links 
```
```python
links = get_links()
data = []

for i in tqdm(links):
    d = get_basic_infos(get_content(i))
    d["Link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)
```
O loop está iterando sobre uma lista de links de personagens acima, fazendo requisições web, extraindo dados, e processando essas informações. Dependendo do número de links e da velocidade da rede, isso pode demorar, logo usamos o tqdm fornece uma barra de progresso visual no terminal ou notebook, permitindo que você veja quanto do trabalho já foi concluído e quanto ainda falta! Mesmo que esse projeto tenha um número pequeno de dados.

```python
df = pd.DataFrame(data)
df.to_parquet("dados_re.parquet", index=False)

E pronto! Agora temos um dataframe completo com as informações dos personagens de Resident Evil, extraído diretamente do site. O arquivo Parquet gerado pode ser utilizado para futuras análises e visualizações.
