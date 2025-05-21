import psycopg2
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS editais_completo (
        idpncp TEXT PRIMARY KEY,
        titulo TEXT,
        modalidade TEXT,
        ultima_atualizacao TEXT,
        orgao TEXT,
        local TEXT,
        objeto TEXT,
        link TEXT,
        cnpj TEXT,
        tipo TEXT,
        modo_disputa TEXT,
        registro_preco TEXT,
        fonte_orcamentaria TEXT,
        data_divulgacao TEXT,
        situacao TEXT,
        data_inicio TEXT,
        data_fim TEXT,
        valor_total TEXT,
        itens TEXT,
        coletado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def edital_existe(idpncp):
    cursor.execute("SELECT 1 FROM editais_completo WHERE idpncp = %s", (idpncp,))
    return cursor.fetchone() is not None

def salvar_edital_completo(dados):
    cursor.execute("""
        INSERT INTO editais_completo (
            idpncp, titulo, modalidade, ultima_atualizacao, orgao, local,
            objeto, link, cnpj, tipo, modo_disputa, registro_preco,
            fonte_orcamentaria, data_divulgacao, situacao,
            data_inicio, data_fim, valor_total, itens
        )
        VALUES (
            %(idpncp)s, %(titulo)s, %(modalidade)s, %(ultima_atualizacao)s, %(orgao)s, %(local)s,
            %(objeto)s, %(link)s, %(cnpj)s, %(tipo)s, %(modo_disputa)s, %(registro_preco)s,
            %(fonte_orcamentaria)s, %(data_divulgacao)s, %(situacao)s,
            %(data_inicio)s, %(data_fim)s, %(valor_total)s, %(itens)s
        )
        ON CONFLICT (idpncp) DO UPDATE SET
            titulo = EXCLUDED.titulo,
            modalidade = EXCLUDED.modalidade,
            ultima_atualizacao = EXCLUDED.ultima_atualizacao,
            orgao = EXCLUDED.orgao,
            local = EXCLUDED.local,
            objeto = EXCLUDED.objeto,
            link = EXCLUDED.link,
            cnpj = EXCLUDED.cnpj,
            tipo = EXCLUDED.tipo,
            modo_disputa = EXCLUDED.modo_disputa,
            registro_preco = EXCLUDED.registro_preco,
            fonte_orcamentaria = EXCLUDED.fonte_orcamentaria,
            data_divulgacao = EXCLUDED.data_divulgacao,
            situacao = EXCLUDED.situacao,
            data_inicio = EXCLUDED.data_inicio,
            data_fim = EXCLUDED.data_fim,
            valor_total = EXCLUDED.valor_total,
            itens = EXCLUDED.itens,
            coletado_em = CURRENT_TIMESTAMP
    """, dados)
    conn.commit()
