

# %%
import pandas as pd
# %%
from tqdm import tqdm
# %%
import requests

# %%
from bs4 import BeautifulSoup

# %%
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '_gid=GA1.2.153721723.1723054225; __gads=ID=8b0863c977e202c6:T=1723054224:RT=1723062598:S=ALNI_MZBg-qsJk4kqhyS-Dr6EfaACbLr-w; __gpi=UID=00000a4b9dc16c64:T=1723054224:RT=1723062598:S=ALNI_MaLbMdUBoIHyDQPfbtbxncT6VmY_Q; __eoi=ID=aa3d720b6294ed76:T=1723054224:RT=1723062598:S=AA-Afjai_piKCZqMAs1UM-4fqSOk; _ga=GA1.2.669600580.1723054224; FCNEC=%5B%5B%22AKsRol9VzXbDwt0RsQnlkJMS4fl-BzBQzgGhwfOB3LwuDcrBivO7b7QGMOh7c3fEbnFiLlWEnX_Fkh47a11pDHCHtRAyIIuuRvE1ZYFvtsWtFAHb_ocHBaaVVemWvFqaSd9HtPboMTeG0B__q-r79SUDYrsJhNwjxg%3D%3D%22%5D%5D; _ga_DJLCSW50SC=GS1.1.1723062597.2.1.1723062601.56.0.0; _ga_D6NF5QC4QT=GS1.1.1723062597.2.1.1723062601.56.0.0',
    'priority': 'u=0, i',
    'referer': 'https://www.residentevildatabase.com/personagens/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}
# %%
def get_content(url):
    response = requests.get(url, headers=headers)
    return response # %%
# %%
def get_basic_infos(soup):
    div_page = soup.find('div',class_ = 'td-page-content')
    paragraph= div_page.find_all('p')[1]
    ems = paragraph.find_all('em')
    data = {}
    for i in ems:
        chave , valor = i.text.split(':')
        chave = chave.strip(' ')
        data[chave] = valor.strip(' ')
    return data 
# %%
def get_person_info(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("não foi possível achar a url")
        return 0
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        return data
# %%
def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url, headers = headers)
    soup_person= BeautifulSoup(resp.text,features="html.parser")
    ancoras = soup_person.find("div",class_="td-page-content").find_all("a")
       
    links =[i["href"] for i in ancoras]
    return links 
# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_person_info(i)
    d["Link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)

# %%
df = pd.DataFrame(data)
df.to_parquet("dados_re.parquet", index=False)

# %%
