import requests
from bs4 import BeautifulSoup
from coletor.telegram_alerta import notificar_telegram
from coletor.utils import simular_comportamento_humano

def coletar_detalhes(link):
    try:
        simular_comportamento_humano()
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
        resp = requests.get(link, headers=headers, timeout=20)

        if resp.status_code != 200:
            notificar_telegram(f"[erro] Detalhe bloqueado ou não disponível: {link}")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        texto = soup.get_text(separator="\n")

        def extrair(label):
            try:
                linha = [l for l in texto.split("\n") if label in l][0]
                return linha.split(":", 1)[-1].strip()
            except:
                return ""

        detalhes = {
            "cnpj": extrair("CNPJ"),
            "orgao": extrair("Órgão"),
            "unidadeCompradora": extrair("Unidade Compradora"),
            "modalidade": extrair("Modalidade da Contratação"),
            "tipo": extrair("Tipo de Licitação"),
            "modoDisputa": extrair("Modo de Disputa"),
            "registroPreco": extrair("Registro de Preço"),
            "fonteOrcamentaria": extrair("Fonte de Recursos"),
            "dataDivulgacao": extrair("Data de Divulgação"),
            "situacao": extrair("Situação Atual"),
            "dataInicioRecebimento": extrair("Data início recebimento"),
            "dataFimRecebimento": extrair("Data fim recebimento"),
            "valorTotal": extrair("Valor estimado total"),
            "objetoDetalhado": extrair("Objeto Detalhado"),
            "itens": extrair("Itens")
        }

        return detalhes

    except Exception as e:
        notificar_telegram(f"[falha crítica] Erro ao detalhar edital: {e}")
        return None
