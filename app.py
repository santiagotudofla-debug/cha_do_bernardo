import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from supabase import create_client

# ============================================================
# 1. SUPABASE
# ============================================================
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# ============================================================
# 2. PAGE CONFIG + CSS PREMIUM
# ============================================================
st.set_page_config(page_title="Chá de Bebê · Bernardo", layout="wide", page_icon="👶")

st.markdown("""
<style>
/* ── Reset & Fonte ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Fundo geral ── */
.stApp {
    background: linear-gradient(135deg, #f0f6ff 0%, #e8f2ff 50%, #fffbe6 100%);
}

/* ── Esconde toolbar e menu padrão do Streamlit ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1100px; }

/* ── HERO BANNER ── */
.hero {
    background: linear-gradient(135deg, #1a73e8 0%, #1558b0 40%, #0d3d7a 100%);
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(26,115,232,0.30);
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.08'%3E%3Ccircle cx='30' cy='30' r='20'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.4);
    color: white;
    padding: 6px 18px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 6vw, 64px);
    color: white;
    margin: 0 0 12px 0;
    line-height: 1.1;
    text-shadow: 0 2px 20px rgba(0,0,0,0.1);
}
.hero-sub {
    font-size: 18px;
    color: rgba(255,255,255,0.88);
    font-weight: 300;
    margin: 0 0 30px 0;
    letter-spacing: 0.5px;
}
.hero-data {
    display: inline-flex;
    gap: 32px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 16px;
    padding: 16px 32px;
    backdrop-filter: blur(10px);
}
.hero-data-item { color: white; text-align: center; }
.hero-data-item .label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.7; }
.hero-data-item .value { font-size: 16px; font-weight: 600; margin-top: 2px; }

/* ── STEPS (etapas) ── */
.steps-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 0 0 40px 0;
}
.step {
    display: flex;
    align-items: center;
    gap: 10px;
}
.step-num {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: #f0f0f0;
    color: #aaa;
    font-weight: 700;
    font-size: 14px;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.3s;
}
.step-num.active { background: linear-gradient(135deg,#1a73e8,#0d3d7a); color: white; box-shadow: 0 4px 14px rgba(26,115,232,0.4); }
.step-label { font-size: 13px; font-weight: 500; color: #aaa; }
.step-label.active { color: #1a73e8; font-weight: 600; }
.step-line { width: 60px; height: 2px; background: #f0f0f0; margin: 0 8px; }
.step-line.done { background: linear-gradient(90deg,#1a73e8,#f5c400); }

/* ── CARD DE SEÇÃO ── */
.section-card {
    background: white;
    border-radius: 20px;
    padding: 36px;
    margin-bottom: 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
    border: 1px solid rgba(26,115,232,0.08);
}
.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid #ddeaf8;
}
.section-icon {
    width: 48px; height: 48px;
    background: linear-gradient(135deg,#ddeaf8,#b8d4f5);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.section-title { font-family: 'Playfair Display', serif; font-size: 22px; color: #2d2d2d; margin: 0; }
.section-subtitle { font-size: 13px; color: #999; margin: 2px 0 0 0; }

/* ── INPUTS ── */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div {
    border-radius: 12px !important;
    border: 1.5px solid #c8ddf5 !important;
    background: #f8fbff !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #1a73e8 !important;
    box-shadow: 0 0 0 3px rgba(26,115,232,0.12) !important;
}
div[data-testid="stTextArea"] textarea {
    border-radius: 12px !important;
    border: 1.5px solid #c8ddf5 !important;
    background: #f8fbff !important;
}

/* ── RADIO ── */
div[data-testid="stRadio"] label {
    background: #fafafa;
    border: 1.5px solid #efefef;
    border-radius: 10px;
    padding: 8px 16px;
    margin-right: 8px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg,#ddeaf8,#b8d4f5);
    border-color: #1a73e8;
    color: #0d3d7a;
    font-weight: 600;
}

/* ── BOTÃO PRINCIPAL ── */
div.stButton > button {
    background: linear-gradient(135deg, #f5c400 0%, #e6b000 100%) !important;
    color: #0d3d7a !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 40px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px !important;
    width: 100% !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 24px rgba(245,196,0,0.40) !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(245,196,0,0.55) !important;
}
div.stButton > button:active { transform: translateY(0) !important; }

/* ── VITRINE CARDS ── */
.mimo-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    border: 1.5px solid #ddeaf8;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
    height: 100%;
}
.mimo-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(26,115,232,0.15);
    border-color: #1a73e8;
}
.mimo-card-img { width: 100%; aspect-ratio: 4/3; object-fit: cover; display: block; }
.mimo-card-body { padding: 14px; }
.mimo-card-cat {
    font-size: 10px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1.5px; color: #1a73e8; margin-bottom: 4px;
}
.mimo-card-name { font-size: 14px; font-weight: 700; color: #2d2d2d; margin: 0 0 4px 0; line-height: 1.3; }
.mimo-card-desc { font-size: 11px; color: #999; margin: 0 0 10px 0; line-height: 1.4; }
.mimo-card-price { font-size: 18px; font-weight: 800; color: #1a73e8; margin: 0 0 10px 0; }
.mimo-card-btns { display: flex; gap: 4px; flex-wrap: wrap; }
.mimo-btn {
    display: inline-block; padding: 4px 9px; border-radius: 8px;
    font-size: 10px; font-weight: 700; text-decoration: none !important;
    color: white !important; letter-spacing: 0.3px;
}
.mimo-btn-b { background: #e8401c; }
.mimo-btn-g { background: #4285F4; }
.mimo-btn-m { background: #f0bf00; color: #333 !important; }

/* ── RESUMO / PIX CARD ── */
.resumo-card {
    background: linear-gradient(135deg,#f0f6ff,#e8f2ff);
    border: 1.5px solid #c5dff7;
    border-radius: 20px;
    padding: 28px;
    margin-top: 24px;
}
.resumo-linha {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px dashed #c5dff7; font-size: 15px;
}
.resumo-linha:last-child { border-bottom: none; }
.resumo-total {
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 0 0 0; font-size: 20px; font-weight: 800; color: #1a73e8;
}

.pix-card {
    background: white;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    border: 1.5px solid #c5dff7;
    box-shadow: 0 8px 32px rgba(26,115,232,0.08);
}
.pix-card h3 { font-family: 'Playfair Display',serif; color: #2d2d2d; font-size: 22px; margin-bottom: 8px; }
.pix-card p { color: #888; font-size: 14px; margin-bottom: 24px; }

/* ── INFO BOX ── */
.info-box {
    background: linear-gradient(135deg,#e8f4fd,#ddeffa);
    border-left: 4px solid #4a90d9;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 14px;
    color: #1a5276;
    margin: 16px 0;
}
.warn-box {
    background: linear-gradient(135deg,#fef9e7,#fdf2cc);
    border-left: 4px solid #f0c030;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 14px;
    color: #7d6608;
    margin: 16px 0;
}
.success-box {
    background: linear-gradient(135deg,#e6f4ea,#c8ecd0);
    border-left: 4px solid #27ae60;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 14px;
    color: #0d3d7a;
    margin: 16px 0;
}

/* ── LABEL DE CAMPO ── */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #555 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 4px !important;
}

/* ── DIVIDER ── */
hr { border: none; border-top: 1px solid #f0e0ea; margin: 28px 0; }

/* ── NUMBER INPUT ── */
div[data-testid="stNumberInput"] input {
    border-radius: 12px !important;
    border: 1.5px solid #c8ddf5 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. REGRAS DE NEGÓCIO
# ============================================================
LIMITES_FRALDAS = {"RN": 20, "P": 40, "M": 40, "G": 30}
VALORES_PIX     = {"RN": 40.00, "P": 45.00, "M": 50.00, "G": 60.00, "PIX Solidário (R$ 50)": 50.00}
CHAVE_PIX       = "11963766575"

# ============================================================
# 4. CATÁLOGO DE MIMOS
# ============================================================
@st.cache_data
def gerar_catalogo():
    dados = [
        ("Lenços Umedecidos (Leve 4)",   "Higiene",        39.90,  "Kit de lenços para pele sensível sem perfume."),
        ("Pomada Antiassaduras",          "Higiene",        25.50,  "Proteção prolongada com vitaminas e óleos."),
        ("Kit Cotonetes Infantis",        "Higiene",        15.00,  "Hastes flexíveis com ponta de segurança."),
        ("Sabonete Líquido RN",           "Higiene",        32.90,  "Da cabeça aos pés, não arde os olhos."),
        ("Álcool 70% e Algodão",          "Higiene",        22.00,  "Para a higiene do coto umbilical do bebê."),
        ("Banheira Ergonômica",           "Banho",          89.90,  "Banheira com apoio de segurança anatômico."),
        ("Toalha com Capuz",              "Banho",          55.00,  "Toalha 100% algodão super absorvente."),
        ("Termômetro de Banho",           "Banho",          28.50,  "Mede a temperatura da água no formato de bichinho."),
        ("Esponja Natural Soft",          "Banho",          19.90,  "Esponja extra macia para recém-nascidos."),
        ("Naninha de Ovelha",             "Naninhas",       49.90,  "Paninho de apego macio com pelúcia."),
        ("Chupeta RN Calmante",           "Naninhas",       35.00,  "Chupeta de silicone inteiriça ortodôntica."),
        ("Manta Leve Algodão",            "Naninhas",       60.00,  "Ideal para dias de meia-estação."),
        ("Ninho Redutor de Berço",        "Naninhas",      130.00,  "Simula o útero materno para um sono tranquilo."),
        ("Kit 3 Bodys Manga Longa",       "Roupinhas",      79.90,  "Cores neutras, 100% algodão suedine."),
        ("Kit Mijões (Culote)",           "Roupinhas",      55.00,  "Calças com pezinho reversível super práticas."),
        ("Macacão Plush",                 "Roupinhas",      89.00,  "Macacão quentinho para noites frias."),
        ("Luvinhas e Touca",              "Roupinhas",      35.00,  "Evita que o bebê se arranhe nos primeiros dias."),
        ("Móbile de Berço Musical",       "Brinquedos",    145.00,  "Estimula a visão e acalma com cantigas."),
        ("Chocalho Macio",                "Brinquedos",     32.00,  "Barulhinho suave e formato fácil de segurar."),
        ("Mordedor de Silicone",          "Brinquedos",     28.90,  "Alivia o desconforto das gengivas."),
        ("Livrinho de Pano",              "Brinquedos",     45.00,  "Livro sensorial que pode ir na boca e na água."),
        ("Kit 2 Mamadeiras Anticólica",   "Alimentação",   120.00,  "Sistema de ventilação para reduzir gases."),
        ("Escova para Mamadeira",         "Alimentação",    25.00,  "Alcança os cantos difíceis das garrafinhas."),
        ("Potes Armazenamento Leite",     "Alimentação",    65.00,  "Recipientes com tampa hermética e medição."),
        ("Trocador Portátil de Bolsa",    "Organização",    55.00,  "Impermeável, fecha como uma bolsinha."),
        ("Mochila Maternidade",           "Organização",   250.00,  "Múltiplos compartimentos e bolso térmico."),
        ("Kit Cabides Infantis",          "Organização",    35.00,  "Tamanho ideal para as roupinhas pequenas."),
        ("Quadro Porta-Maternidade",      "Personalizados",120.00,  "Bordado à mão com o nome do Bernardo."),
        ("Álbum do Bebê (Primeiro Ano)",  "Personalizados", 89.90,  "Para preencher as conquistas de cada mês.")
    ]
    # Ícone por categoria
    icones = {"Higiene":"🧴","Banho":"🛁","Naninhas":"🧸","Roupinhas":"👕",
              "Brinquedos":"🎾","Alimentação":"🍼","Organização":"🎒","Personalizados":"🎨"}
    cat_cores = {
        "Higiene":"e3f2fd/0d47a1","Banho":"e8f5e9/1b5e20","Naninhas":"fff8e1/e65100",
        "Roupinhas":"e8eaf6/283593","Brinquedos":"f3e5f5/4a148c","Alimentação":"e0f7fa/006064",
        "Organização":"fff9c4/f57f17","Personalizados":"e8f5e9/1b5e20"
    }
    catalogo = []
    for i, (nome, cat, valor, desc) in enumerate(dados, 1):
        cor = cat_cores.get(cat, "f5f5f5/333333")
        icone = icones.get(cat, "🎁")
        texto_img = urllib.parse.quote_plus(f"{icone} {nome[:18]}")
        img_url   = f"https://placehold.co/400x300/{cor}.png?text={texto_img}"
        termo     = urllib.parse.quote_plus(nome + " bebe")
        catalogo.append({
            "id": i, "nome": nome, "categoria": cat, "valor": valor,
            "desc": desc, "img": img_url, "limite_fisico": 2, "icone": icone,
            "link_buscape":      f"https://www.buscape.com.br/busca?q={urllib.parse.quote_plus(nome)}",
            "link_google":       f"https://www.google.com.br/search?q={termo}&tbm=shop",
            "link_mercadolivre": f"https://lista.mercadolivre.com.br/{urllib.parse.quote_plus(nome)}",
        })
    return catalogo

CATALOGO_MIMOS = gerar_catalogo()

# ============================================================
# 5. PIX
# ============================================================
def calcular_crc16(payload):
    crc = 0xFFFF
    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000: crc = (crc << 1) ^ 0x1021
            else: crc = crc << 1
        crc &= 0xFFFF
    return f"{crc:04X}"

def gerar_payload_pix(chave, valor, nome="Cha do Bernardo", cidade="Cotia"):
    if len(chave) == 11 and chave.isdigit(): chave = f"+55{chave}"
    payload   = "000201"
    acc_info  = f"0014br.gov.bcb.pix01{len(chave):02d}{chave}"
    payload  += f"26{len(acc_info):02d}{acc_info}"
    payload  += "52040000"; payload += "5303986"
    valor_str = f"{valor:.2f}"
    payload  += f"54{len(valor_str):02d}{valor_str}"
    payload  += "5802BR"
    payload  += f"59{len(nome):02d}{nome}"
    payload  += f"60{len(cidade):02d}{cidade}"
    payload  += "62070503***"; payload += "6304"
    payload  += calcular_crc16(payload)
    return payload

# ============================================================
# 6. SUPABASE — LEITURA E ESCRITA
# ============================================================
def salvar_tudo_supabase(dados_rsvp, mimo, formato_mimo, valor_mimo):
    val_t  = dados_rsvp.get("Valor PIX Fralda Titular (R$)", 0.0)
    val_a  = dados_rsvp.get("Valor PIX Fralda Acompanhante (R$)", 0.0)
    val_m  = valor_mimo if formato_mimo == "PIX" else 0.0
    total  = round(val_t + val_a + val_m, 2)
    linha  = {
        "nome_titular":                  dados_rsvp.get("Nome Titular",""),
        "sexo_titular":                  dados_rsvp.get("Sexo Titular",""),
        "fralda_titular":                dados_rsvp.get("Fralda Titular",""),
        "formato_fralda_titular":        dados_rsvp.get("Formato Fralda Titular",""),
        "valor_pix_fralda_titular":      val_t,
        "leva_acompanhante":             dados_rsvp.get("Leva Acompanhante","Não"),
        "nome_acompanhante":             dados_rsvp.get("Nome Acompanhante","-"),
        "sexo_acompanhante":             dados_rsvp.get("Sexo Acompanhante","-"),
        "fralda_acompanhante":           dados_rsvp.get("Fralda Acompanhante","-"),
        "formato_fralda_acompanhante":   dados_rsvp.get("Formato Fralda Acompanhante","-"),
        "valor_pix_fralda_acompanhante": val_a,
        "qtd_criancas":                  dados_rsvp.get("Qtd Crianças",0),
        "mimo_escolhido":   mimo["nome"]      if mimo else "Sem mimo",
        "categoria_mimo":   mimo["categoria"] if mimo else "-",
        "formato_mimo":     formato_mimo      if mimo else "-",
        "valor_pix_mimo":   val_m,
        "total_pix":        total,
        "mensagem":         dados_rsvp.get("Mensagem",""),
    }
    try:
        get_supabase().table("rsvp").insert(linha).execute()
    except Exception as e:
        st.markdown(f'<div class="warn-box">⚠️ Erro ao salvar: {e}</div>', unsafe_allow_html=True)
        raise

@st.cache_data(ttl=30)
def checar_disponibilidade_fraldas(tamanho):
    try:
        sb = get_supabase()
        rt = sb.table("rsvp").select("id", count="exact").eq("fralda_titular", tamanho).execute()
        ra = sb.table("rsvp").select("id", count="exact").eq("fralda_acompanhante", tamanho).execute()
        return (rt.count or 0) + (ra.count or 0)
    except Exception:
        return 0

@st.cache_data(ttl=30)
def checar_fisicos_comprados(nome_item):
    try:
        r = get_supabase().table("rsvp").select("id", count="exact").eq("mimo_escolhido", nome_item).eq("formato_mimo", "Física").execute()
        return r.count or 0
    except Exception:
        return 0

# ============================================================
# 7. LÓGICA DE FRALDAS
# ============================================================
def gerar_opcoes_fralda(sexo):
    opcoes = []
    if "Mulher" in sexo:
        if checar_disponibilidade_fraldas("RN") < LIMITES_FRALDAS["RN"]: opcoes.append("RN")
        if checar_disponibilidade_fraldas("P")  < LIMITES_FRALDAS["P"]:  opcoes.append("P")
        if not opcoes: opcoes.append("PIX Solidário (R$ 50)")
    elif "Homem" in sexo:
        if checar_disponibilidade_fraldas("M") < LIMITES_FRALDAS["M"]: opcoes.append("M")
        if checar_disponibilidade_fraldas("G") < LIMITES_FRALDAS["G"]: opcoes.append("G")
        if not opcoes: opcoes.append("PIX Solidário (R$ 50)")
    return opcoes

def exibir_bloco_fralda(label, sexo, key):
    opcoes = gerar_opcoes_fralda(sexo)
    fralda = st.radio(f"Tamanho de fralda — {label}", opcoes, horizontal=True, key=f"fralda_{key}")
    formato, valor = "Física", 0.0
    if fralda == "PIX Solidário (R$ 50)":
        formato, valor = "PIX", 50.00
        st.markdown('<div class="info-box">💡 Todas as cotas de fralda já foram preenchidas. Você foi direcionado para o <strong>PIX Solidário</strong>.</div>', unsafe_allow_html=True)
    elif fralda:
        formato = st.radio("Como você vai entregar?",
                           ["🎁  Levarei a fralda física no dia", "📱  Prefiro enviar o valor via PIX"],
                           key=f"formato_{key}")
        if "PIX" in formato:
            formato, valor = "PIX", VALORES_PIX[fralda]
            st.markdown(f'<div class="info-box">💳 Valor sugerido para o pacote <strong>{fralda}</strong>: <strong>R$ {valor:.2f}</strong></div>', unsafe_allow_html=True)
    return fralda, formato, valor

# ============================================================
# 8. MAIN
# ============================================================
def main():

    # ── HERO ─────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✨ Você está convidado</div>
        <h1>Chá de Bebê do Bernardo</h1>
        <p class="hero-sub">Confirme sua presença e escolha um presentinho especial 🍯</p>
        <div class="hero-data">
            <div class="hero-data-item">
                <div class="label">📅 Data</div>
                <div class="value">18/07/2026</div>
            </div>
            <div class="hero-data-item">
                <div class="label">📍 Local</div>
                <div class="value">Cotia · SP</div>
            </div>
            <div class="hero-data-item">
                <div class="label">🍼 Bebê</div>
                <div class="value">Bernardo</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ETAPAS ───────────────────────────────────────────────
    st.markdown("""
    <div class="steps-bar">
        <div class="step">
            <div class="step-num active">1</div>
            <div class="step-label active">Seus dados</div>
        </div>
        <div class="step-line"></div>
        <div class="step">
            <div class="step-num">2</div>
            <div class="step-label">Fraldas</div>
        </div>
        <div class="step-line"></div>
        <div class="step">
            <div class="step-num">3</div>
            <div class="step-label">Mimos</div>
        </div>
        <div class="step-line"></div>
        <div class="step">
            <div class="step-num">4</div>
            <div class="step-label">Confirmar</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SEÇÃO 1: DADOS PESSOAIS ──────────────────────────────
    st.markdown("""
    <div class="section-card chamada-card">
        <div class="chamada-conteudo">
            <div class="chamada-emoji">🍯</div>
            <div class="chamada-texto">
                <p class="chamada-titulo">Prepare os potes de mel porque o</p>
                <p class="chamada-destaque">Chá de Bebê do Bernardo</p>
                <p class="chamada-titulo">está chegando! 🍯</p>
            </div>
            <div class="chamada-emoji">🍯</div>
        </div>
        <p class="chamada-sub">Preencha seus dados abaixo e confirme sua presença — mal podemos esperar para te ver! 💛</p>
        <hr style="border:none;border-top:1px solid #ddeaf8;margin:20px 0 24px 0;">
        <div class="section-header" style="margin-bottom:0;padding-bottom:0;border-bottom:none;">
            <div class="section-icon">👤</div>
            <div>
                <p class="section-title">Seus dados</p>
                <p class="section-subtitle">Conte-nos um pouquinho sobre você</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        c1, c2 = st.columns([2, 1])
        with c1: nome_titular = st.text_input("Nome completo", placeholder="Ex: Maria Silva")
        with c2: sexo_titular = st.selectbox("Sexo", ["Selecione...", "Mulher 🚺", "Homem 🚹"])

    st.markdown("<br>", unsafe_allow_html=True)
    leva_acomp = st.radio("Vai levar acompanhante adulto?", ["Não", "Sim"], horizontal=True)

    nome_acomp, sexo_acomp, fralda_a, formato_a, valor_a = "", "Selecione...", None, "-", 0.0

    if leva_acomp == "Sim":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header" style="margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #f5e6ee;">
            <div class="section-icon">👫</div>
            <div>
                <p class="section-title" style="font-size:18px;">Dados do acompanhante</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        ca1, ca2 = st.columns([2, 1])
        with ca1: nome_acomp = st.text_input("Nome do acompanhante", placeholder="Ex: João Silva")
        with ca2: sexo_acomp = st.selectbox("Sexo do acompanhante", ["Selecione...", "Mulher 🚺", "Homem 🚹"], key="sexo_a")

    qtd_filhos = st.number_input("Crianças que vão junto (filhos, sobrinhos…)", min_value=0, max_value=10, value=0)
    mensagem   = st.text_area("Mensagem para o Bernardo 💌 (opcional)", placeholder="Escreva com carinho…", height=100)

    # ── SEÇÃO 2: FRALDAS ─────────────────────────────────────
    st.markdown("""
    <div class="section-card" style="margin-top:24px;">
        <div class="section-header">
            <div class="section-icon">🍼</div>
            <div>
                <p class="section-title">Presente de fraldas</p>
                <p class="section-subtitle">Cada convidado traz um pacotinho — ajuda muito!</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fralda_t, formato_t, valor_t = None, "-", 0.0
    if sexo_titular != "Selecione...":
        st.markdown(f"**Fralda de {nome_titular or 'você'}**")
        fralda_t, formato_t, valor_t = exibir_bloco_fralda(nome_titular or "você", sexo_titular, "t")
    else:
        st.markdown('<div class="info-box">ℹ️ Selecione seu sexo acima para ver as opções de fralda.</div>', unsafe_allow_html=True)

    if leva_acomp == "Sim" and sexo_acomp != "Selecione...":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"**Fralda do acompanhante ({nome_acomp or 'acompanhante'})**")
        fralda_a, formato_a, valor_a = exibir_bloco_fralda(nome_acomp or "acompanhante", sexo_acomp, "a")

    # ── SEÇÃO 3: MIMOS ───────────────────────────────────────
    st.markdown("""
    <div class="section-card" style="margin-top:24px;">
        <div class="section-header">
            <div class="section-icon">🎁</div>
            <div>
                <p class="section-title">Mimo extra</p>
                <p class="section-subtitle">Surpresas que o Bernardo vai adorar — completamente opcional</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    quer_mimo = st.radio("Deseja presentear com um mimo além das fraldas?",
                         ["Não, apenas as fraldas 🙂", "Sim, quero escolher um mimo! 🎁"], index=0)

    mimo_escolhido = None
    formato_mimo   = "-"
    valor_mimo     = 0.0

    if "Sim" in quer_mimo:
        # Filtro por categoria
        categorias = ["Todas"] + sorted(set(m["categoria"] for m in CATALOGO_MIMOS))
        col_f, _ = st.columns([1, 3])
        with col_f:
            cat_filtro = st.selectbox("Filtrar por categoria", categorias)

        lista_filtrada = CATALOGO_MIMOS if cat_filtro == "Todas" else [m for m in CATALOGO_MIMOS if m["categoria"] == cat_filtro]

        # Grid de cards
        cols = st.columns(4)
        for idx, item in enumerate(lista_filtrada):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="mimo-card">
                    <img class="mimo-card-img" src="{item['img']}">
                    <div class="mimo-card-body">
                        <div class="mimo-card-cat">{item['icone']} {item['categoria']}</div>
                        <p class="mimo-card-name">{item['nome']}</p>
                        <p class="mimo-card-desc">{item['desc']}</p>
                        <p class="mimo-card-price">R$ {item['valor']:.2f}</p>
                        <div class="mimo-card-btns">
                            <a class="mimo-btn mimo-btn-b" href="{item['link_buscape']}"      target="_blank">🔍 Buscapé</a>
                            <a class="mimo-btn mimo-btn-g" href="{item['link_google']}"       target="_blank">🛒 Google</a>
                            <a class="mimo-btn mimo-btn-m" href="{item['link_mercadolivre']}" target="_blank">🛍 ML</a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        nomes = [m["nome"] for m in CATALOGO_MIMOS]
        escolha = st.selectbox("Qual mimo você escolheu?", ["— Selecione —"] + nomes)

        if escolha != "— Selecione —":
            info = next(m for m in CATALOGO_MIMOS if m["nome"] == escolha)
            st.markdown(f'<div class="success-box">✅ <strong>{info["nome"]}</strong> — R$ {info["valor"]:.2f}<br><small>Compare antes de comprar: <a href="{info["link_buscape"]}" target="_blank">Buscapé</a> · <a href="{info["link_google"]}" target="_blank">Google Shopping</a> · <a href="{info["link_mercadolivre"]}" target="_blank">Mercado Livre</a></small></div>', unsafe_allow_html=True)

            fisicos = checar_fisicos_comprados(info["nome"])
            opcoes_entrega = ["📱  Enviar valor via PIX (Recomendado)"]
            if fisicos < info["limite_fisico"]:
                opcoes_entrega.insert(0, "🎁  Levarei o produto físico no chá")
            else:
                st.markdown('<div class="warn-box">⚠️ A cota de entrega física deste item já foi preenchida. Apenas PIX disponível.</div>', unsafe_allow_html=True)

            entrega_mimo = st.radio("Como vai entregar o mimo?", opcoes_entrega)
            mimo_escolhido = info
            if "PIX" in entrega_mimo:
                formato_mimo, valor_mimo = "PIX", info["valor"]
            else:
                formato_mimo, valor_mimo = "Física", 0.0

    # ── SEÇÃO 4: CONFIRMAR ───────────────────────────────────
     st.markdown("""
    <div class="section-card" style="margin-top:24px;">
        <div class="section-header">
            <div class="section-icon">🚀</div>
            <div>
                <p class="section-title">Confirmar presença</p>
                <p class="section-subtitle">Revise e finalize — mal podemos esperar para te ver!</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨  Confirmar Presença e Gerar PIX"):
        if not nome_titular or sexo_titular == "Selecione...":
            st.markdown('<div class="warn-box">⚠️ Por favor, preencha seu nome e sexo antes de confirmar.</div>', unsafe_allow_html=True)
        elif "Sim" in quer_mimo and not mimo_escolhido:
            st.markdown('<div class="warn-box">⚠️ Você marcou que deseja dar um mimo. Selecione-o na lista acima.</div>', unsafe_allow_html=True)
        else:
            dados_rsvp = {
                "Nome Titular":                       nome_titular.strip(),
                "Sexo Titular":                       sexo_titular,
                "Fralda Titular":                     fralda_t,
                "Formato Fralda Titular":             formato_t,
                "Valor PIX Fralda Titular (R$)":      valor_t,
                "Leva Acompanhante":                  leva_acomp,
                "Nome Acompanhante":                  nome_acomp.strip() if leva_acomp == "Sim" else "-",
                "Sexo Acompanhante":                  sexo_acomp         if leva_acomp == "Sim" else "-",
                "Fralda Acompanhante":                fralda_a           if leva_acomp == "Sim" else "-",
                "Formato Fralda Acompanhante":        formato_a          if leva_acomp == "Sim" else "-",
                "Valor PIX Fralda Acompanhante (R$)": valor_a            if leva_acomp == "Sim" else 0.0,
                "Qtd Crianças":                       int(qtd_filhos),
                "Mensagem":                           mensagem,
            }

            with st.spinner("Confirmando presença..."):
                salvar_tudo_supabase(dados_rsvp, mimo_escolhido, formato_mimo, valor_mimo)
                checar_disponibilidade_fraldas.clear()
                checar_fisicos_comprados.clear()

            total_pix = valor_t + valor_a + (valor_mimo if formato_mimo == "PIX" else 0.0)

            st.balloons()
            st.markdown(f'<div class="success-box" style="font-size:16px;">🎉 <strong>Presença confirmada!</strong> Muito obrigado, {nome_titular}. O Bernardo já está ansioso para te ver! ❤️</div>', unsafe_allow_html=True)

            # Resumo
            st.markdown('<div class="resumo-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="resumo-card">
                <div style="font-family:'Playfair Display',serif;font-size:20px;color:#2d2d2d;margin-bottom:16px;">📋 Seu Resumo</div>
                <div class="resumo-linha">
                    <span>🍼 Fralda ({nome_titular})</span>
                    <span><strong>{fralda_t}</strong> · {formato_t} · R$ {valor_t:.2f}</span>
                </div>
                {"" if leva_acomp != "Sim" else f'<div class="resumo-linha"><span>🍼 Fralda ({nome_acomp or "Acompanhante"})</span><span><strong>{fralda_a}</strong> · {formato_a} · R$ {valor_a:.2f}</span></div>'}
                {"" if not mimo_escolhido else f'<div class="resumo-linha"><span>🎁 Mimo · {mimo_escolhido["nome"]}</span><span>{formato_mimo} · R$ {valor_mimo:.2f}</span></div>'}
                <div class="resumo-total">
                    <span>Total a pagar via PIX</span>
                    <span>R$ {total_pix:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # PIX
            if total_pix > 0:
                payload_pix = gerar_payload_pix(CHAVE_PIX, total_pix)
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=260x260&data={urllib.parse.quote(payload_pix)}"
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="pix-card">', unsafe_allow_html=True)
                p1, p2 = st.columns([1, 2])
                with p1:
                    st.image(qr_url, width=220)
                with p2:
                    st.markdown(f"""
                    <div style="text-align:left;padding:16px 0;">
                        <p style="font-family:'Playfair Display',serif;font-size:22px;color:#2d2d2d;margin:0 0 6px 0;">📱 Pague via PIX</p>
                        <p style="color:#888;font-size:14px;margin:0 0 20px 0;">Abra o app do seu banco → PIX → Pagar com QR Code</p>
                        <p style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#1a73e8;margin-bottom:6px;">Chave celular</p>
                        <code style="background:#eaf3ff;border:1px solid #b8d4f5;border-radius:8px;padding:10px 16px;font-size:15px;font-weight:700;color:#0d3d7a;display:block;margin-bottom:20px;">{CHAVE_PIX}</code>
                        <p style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#1a73e8;margin-bottom:6px;">PIX Copia e Cola</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(payload_pix, language="text")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">🎁 Tudo certo! Te esperamos no chá com os presentes físicos. 🥳</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
