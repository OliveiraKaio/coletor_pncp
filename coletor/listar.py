import requests
from bs4 import BeautifulSoup
import random
from coletor.utils import simular_comportamento_humano
from coletor.db import edital_existe, salvar_edital_completo
from coletor.telegram_alerta import notificar_telegram
from coletor.detalhar import coletar_detalhes

def executar_coleta():
    base_url = "https://pncp.gov.br/app/editais?pagina={}&tam_pagina=100&ordenacao=-data"
    paginas = random.sample(range(1, 100), k=random.randint(3, 6))

    for pagina in paginas:
        try:
            url = base_url.format(pagina)
            resp = requests.get(url, timeout=20, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
            })

            if resp.status_code != 200:
                notificar_telegram(f"[erro] Falha na página {pagina}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            blocos = soup.find_all("div", class_="col-12 col-md")

            for bloco in random.sample(blocos, k=min(random.randint(5, 10), len(blocos))):
                try:
                    texto = bloco.get_text()
                    titulo = bloco.find("strong").text.strip()
                    idpncp = texto.split("Id contratação PNCP:")[-1].split()[0].strip()
                    modalidade = "?"
                    orgao = "?"
                    local = "?"
                    objeto = "?"
                    link = "https://pncp.gov.br"

                    if edital_existe(idpncp):
                        continue

                    # Detalhamento do edital
                    detalhes = coletar_detalhes(link)
                    if not detalhes:
                        continue

                    salvar_edital_completo({
                        "idpncp": idpncp,
                        "titulo": titulo,
                        "modalidade": detalhes.get("modalidade", modalidade),
                        "ultima_atualizacao": "hoje",
                        "orgao": detalhes.get("orgao", orgao),
                        "local": detalhes.get("local", local),
                        "objeto": detalhes.get("objetoDetalhado", objeto),
                        "link": link,
                        "cnpj": detalhes.get("cnpj"),
                        "tipo": detalhes.get("tipo"),
                        "modo_disputa": detalhes.get("modoDisputa"),
                        "registro_preco": detalhes.get("registroPreco"),
                        "fonte_orcamentaria": detalhes.get("fonteOrcamentaria"),
                        "data_divulgacao": detalhes.get("dataDivulgacao"),
                        "situacao": detalhes.get("situacao"),
                        "data_inicio": detalhes.get("dataInicioRecebimento"),
                        "data_fim": detalhes.get("dataFimRecebimento"),
                        "valor_total": detalhes.get("valorTotal"),
                        "itens": detalhes.get("itens")
                    })

                    simular_comportamento_humano()

                except Exception as e:
                    print(f"[erro] Erro no bloco: {e}")
        except Exception as e:
            notificar_telegram(f"[bloqueio?] Erro geral na página {pagina}: {e}")
