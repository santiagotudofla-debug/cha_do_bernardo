import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Chá de Bebê - Confirmação", layout="wide", page_icon="🍼")

# Estilo profissional (MANTIDO)
st.markdown("""
    <style>
    .secao-titulo { color: #d6336c; font-weight: 800; border-bottom: 2px solid #fca3b7; padding-bottom: 5px; margin-top: 30px;}
    .vitrine-card { background-color: #ffffff; border-radius: 15px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; border: 1px solid #f0f0f0; }
    div.stButton > button { background-color: #fca3b7; color: white; border-radius: 20px; font-weight: bold; width: 100%; padding: 12px; }
    </style>
""", unsafe_allow_html=True)

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

LIMITES_FRALDAS = {"RN": 20, "P": 40, "M": 40, "G": 30}
VALORES_PIX = {"RN": 40.00, "P": 45.00, "M": 50.00, "G": 60.00, "PIX Solidário (R$ 50)": 50.00}
CHAVE_PIX = "11963766575"

# --- Funções de Leitura/Escrita no Google Sheets ---
def ler_sheets(aba):
    try:
        return conn.read(worksheet=aba, ttl=0).dropna(how="all")
    except:
        return pd.DataFrame()

def salvar_no_sheets(aba, dados):
    df = ler_sheets(aba)
    df_atualizado = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
    conn.update(worksheet=aba, data=df_atualizado)

# --- Restante do seu código (Gerar catálogo, payload, etc) ---
# [COLE AQUI A SUA FUNÇÃO gerar_catalogo_50_mimos e gerar_payload_pix QUE JÁ ESTÃO NO SEU CÓDIGO]

# --- Função Principal Atualizada ---
def main():
    # ... (Seu código de layout main() permanece igual, apenas troque a parte final) ...
    
    # 4. Finalização (Substitua o seu bloco de salvar pelo abaixo)
    if st.button("Confirmar Tudo e Gerar Resumo 🚀"):
        # ... (suas validações iniciais) ...
        
        # SALVAR NO GOOGLE SHEETS
        dados_rsvp = {
            "Nome Titular": nome_titular.strip(), 
            "Sexo Titular": sexo_titular, 
            "Fralda Titular": fralda_t,
            "Formato Titular": formato_t, 
            "Valor PIX Titular": valor_t, 
            "Leva Acompanhante": leva_acompanhante,
            "Nome Acompanhante": nome_acomp.strip() if leva_acompanhante == "Sim" else "-",
            "Mensagem": mensagem
        }
        
        # Salva na aba RSVP
        salvar_no_sheets("RSVP", dados_rsvp)
        
        # Salva na aba Mimos (se houver)
        if mimo_escolhido:
            salvar_no_sheets("Mimos", {"Nome": nome_titular, "Mimo": mimo_escolhido['nome'], "Valor": valor_mimo})

        st.success("Confirmado com sucesso!")
        # ... (restante do resumo e QR Code) ...
