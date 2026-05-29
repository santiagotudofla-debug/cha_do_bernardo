import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from supabase import create_client

# ============================================================
# 1. SUPABASE (Conexão)
# ============================================================
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# ============================================================
# 2. PAGE CONFIG + CSS COMPLETO COM EFEITO CAMALEÃO E TEXTO PRETO
# ============================================================
st.set_page_config(page_title="Chá de Bebê · Bernardo", layout="wide", page_icon="👶")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 0 !important; max-width: 1000px; }

/* ── FUNDO CAMALEÃO ANIMADO (AZUL E AMARELO) ── */
.stApp {
    background: linear-gradient(-45deg, #4facfe, #00f2fe, #f6d365, #ffb347);
    background-size: 400% 400%;
    animation: gradientCamaleao 12s ease infinite;
}

@keyframes gradientCamaleao {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── BARRA DE ETAPAS (NOVO DESIGN) ── */
.steps-container {
    position: fixed; top: 0; left: 0; width: 100%;
    background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.85) 100%);
    backdrop-filter: blur(8px); z-index: 9999;
    padding: 18px 0; border-bottom: 1px solid rgba(26,115,232,0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
.steps-bar { 
    display: flex; align-items: center; justify-content: center; 
    max-width: 850px; margin: 0 auto; gap: 8px;
}
.step { display: flex; align-items: center; gap: 12px; }

.step-num { 
    width: 42px; height: 42px; border-radius: 50%; 
    background: #f0f2f5; color: #8892a0; font-weight: 800; font-size: 16px; 
    display: flex; align-items: center; justify-content: center; 
}
.step-num.active { 
    background: #1565c0; color: white; 
    box-shadow: 0 4px 12px rgba(21,101,192,0.3);
}

.step-label { font-size: 15px; font-weight: 600; color: #aab4c3; }
.step-label.active { color: #1565c0; font-weight: 800; }

.step-line { 
    width: 70px; height: 4px; background: #f0f2f5; 
    margin: 0 4px; border-radius: 2px;
}
.step-line.done { 
    background: linear-gradient(90deg, #1565c0 0%, #d4af37 100%); 
}

/* ── HERO BANNER (AZUL COM BOLINHAS) ── */
.hero {
    background: linear-gradient(135deg, #1a73e8 0%, #0d3d7a 100%);
    border-radius: 20px; padding: 50px 20px; text-align: center;
    color: white; margin-top: 100px; margin-bottom: 30px;
    position: relative; overflow: hidden;
    box-shadow: 0 15px 40px rgba(26,115,232,0.25);
}
.hero::before {
    content: ''; position: absolute; inset: 0;
    background-image: radial-gradient(rgba(255, 255, 255, 0.12) 3px, transparent 3px);
    background-size: 26px 26px;
}
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3); padding: 6px 18px;
    border-radius: 50px; font-size: 12px; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 20px; position: relative; z-index: 1;
}
.hero h1 { font-family: 'Playfair Display', serif; font-size: clamp(32px, 5vw, 55px); margin: 0 0 10px 0; position: relative; z-index: 1; text-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.hero-sub { font-size: 16px; font-weight: 300; margin-bottom: 25px; color: #e8f0fe; position: relative; z-index: 1; }
.hero-data {
    display: inline-flex; gap: 30px; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 16px;
    padding: 15px 30px; backdrop-filter: blur(8px); position: relative; z-index: 1;
}
.hero-data-item { text-align: center; }
.hero-data-item .label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; margin-bottom: 4px; }
.hero-data-item .value { font-size: 15px; font-weight: 700; }

/* ── CHAMADA DOS POTES DE MEL ── */
.chamada-card {
    background: linear-gradient(135deg, #fdfbf4 0%, #fefcf8 100%);
    border: 2px solid #fbc02d; border-radius: 16px;
    padding: 25px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(251, 192, 45, 0.1);
}
.chamada-conteudo { display: flex; justify-content: center; align-items: center; gap: 20px; }
.chamada-emoji { font-size: 40px; animation: balanco 2.5s ease-in-out infinite; }
.chamada-emoji:last-child { animation-delay: 0.5s; }
@keyframes balanco { 0%, 100% { transform: rotate(-8deg) scale(1); } 50% { transform: rotate(8deg) scale(1.1); } }
.chamada-texto { text-align: center; }
.chamada-titulo { font-size: 17px; font-weight: 600; color: #1a73e8; margin: 0; }
.chamada-destaque { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: #c09628; margin: 4px 0; }
.chamada-sub { text-align: center; font-size: 14px; color: #666; margin-top: 15px; margin-bottom: 0; }

/* ── ESTILOS LIMPOS E TEXTOS EM PRETO NEGRITO ── */
.section-card { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 30px; margin-bottom: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.4); }
div.stButton > button { background-color: #fca3b7 !important; color: white !important; border-radius: 20px !important; border: none !important; font-weight: bold !important; width: 100% !important; transition: all 0.3s !important; padding: 14px !important; font-size: 16px !important; }
div.stButton > button:hover { background-color: #ff859f !important; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(252, 163, 183, 0.4); }
div.stAlert { background-color: rgba(255,255,255,0.9); border-radius: 10px; border-left: 5px solid #87ceeb; color: #00529B; }

/* Títulos das seções em PRETO e EXTRA NEGRITO (900) */
.secao-titulo { color: #000000; margin-top: 30px; margin-bottom: 15px; font-size: 20px; font-weight: 900; border-bottom: 2px solid #000000; padding-bottom: 5px;}
h4 { color: #333 !important; font-weight: 800 !important; margin-bottom: 10px !important; }

/* ── VITRINE CARDS (GRID PERFEITO) ── */
.vitrine-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 20px;
    padding: 10px 0;
}
.vitrine-card { 
    background-color: #ffffff; 
    border-radius: 15px; 
    padding: 15px; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
    transition: transform 0.3s ease; 
    border: 1px solid #f0f0f0; 
    display: flex; 
    flex-direction: column; 
    height: 100%;
}
.vitrine-card:hover { transform: translateY(-6px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
.vitrine-img-container { 
    position: relative; 
    border-radius: 10px; 
    overflow: hidden; 
    margin-bottom: 12px; 
    aspect-ratio: 4/3; 
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fdf0f3;
}
.vitrine-img-container img { width: 100%; height: 100%; object-fit: cover; display: block; }
.vitrine-titulo { 
    font-size: 15px; 
    font-weight: 700; 
    color: #444; 
    margin: 0 0 10px 0; 
    line-height: 1.3; 
    flex-grow: 1; /* O segredo do alinhamento: empurra o preço e o botão pra baixo */
}
.vitrine-preco { 
    font-size: 16px; 
    font-weight: 900; 
    color: #000000; 
    margin: 0 0 12px 0; 
}
.preco-botoes { 
    display: flex; 
    width: 100%; 
    margin-top: auto; 
}
.preco-btn { 
    display: inline-block; 
    width: 100%; 
    text-align: center; 
    padding: 10px 12px; 
    border-radius: 8px; 
    font-size: 12px; 
    font-weight: 700; 
    text-decoration: none !important; 
    color: #333 !important; 
    transition: filter 0.2s ease;
}
.preco-btn:hover { filter: brightness(0.95); }
.btn-ml { background: #FFE600; border: 1px solid #e6ce00;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. REGRAS DE NEGÓCIO E CATÁLOGO
# ============================================================
LIMITES_FRALDAS = {"RN": 20, "P": 40, "M": 40, "G": 30}
VALORES_PIX = {"RN": 40.00, "P": 45.00, "M": 50.00, "G": 60.00, "PIX Solidário (R$ 50)": 50.00}
CHAVE_PIX = "11963766575"

@st.cache_data
def gerar_catalogo_50_mimos():
    # Agora com 32 itens para fechar a última linha da grid com 4 cartões certinhos!
    dados_brutos = [
        ("Lenços Umedecidos (Leve 4)", "Higiene", 39.90, "Shopee", "Kit de lenços..."),
        ("Pomada Antiassaduras", "Higiene", 25.50, "Natura", "Proteção prolongada..."),
        ("Kit Cotonetes Infantis", "Higiene", 15.00, "Mercado Livre", "Hastes flexíveis..."),
        ("Sabonete Líquido RN", "Higiene", 32.90, "Natura", "Da cabeça aos pés..."),
        ("Álcool 70% e Algodão", "Higiene", 22.00, "Amazon", "Para a higiene..."),
        ("Banheira Ergonômica", "Banho", 89.90, "Amazon", "Banheira anatômica..."),
        ("Toalha com Capuz", "Banho", 55.00, "Elo7", "Toalha 100% algodão..."),
        ("Termômetro de Banho", "Banho", 28.50, "Shopee", "Mede a temperatura..."),
        ("Esponja Natural Soft", "Banho", 19.90, "Amazon", "Esponja extra macia..."),
        ("Naninha de Ovelha", "Naninhas", 49.90, "Elo7", "Paninho de apego..."),
        ("Chupeta RN Calmante", "Naninhas", 35.00, "Amazon", "Chupeta de silicone..."),
        ("Manta Leve Algodão", "Naninhas", 60.00, "Mercado Livre", "Meia-estação..."),
        ("Ninho Redutor de Berço", "Naninhas", 130.00, "Elo7", "Simula o útero..."),
        ("Kit 3 Bodys Manga Longa", "Roupinhas", 79.90, "Amazon", "100% algodão..."),
        ("Kit Mijões (Culote)", "Roupinhas", 55.00, "Shopee", "Com pezinho..."),
        ("Macacão Plush", "Roupinhas", 89.00, "Magazine Luiza", "Para noites frias..."),
        ("Luvinhas e Touca", "Roupinhas", 35.00, "Shopee", "Evita arranhões..."),
        ("Móbile de Berço Musical", "Brinquedos", 145.00, "Amazon", "Estimula a visão..."),
        ("Chocalho Macio", "Brinquedos", 32.00, "Shopee", "Barulhinho suave..."),
        ("Mordedor de Silicone", "Brinquedos", 28.90, "Natura", "Alivia gengivas..."),
        ("Livrinho de Pano", "Brinquedos", 45.00, "Amazon", "Livro sensorial..."),
        ("Kit 2 Mamadeiras Anticólica", "Alimentação", 120.00, "Amazon", "Reduz gases..."),
        ("Escova para Mamadeira", "Alimentação", 25.00, "Shopee", "Alcança cantos..."),
        ("Potes Armazenamento Leite", "Alimentação", 65.00, "Amazon", "Com tampa..."),
        ("Trocador Portátil de Bolsa", "Organização", 55.00, "Elo7", "Impermeável..."),
        ("Mochila Maternidade", "Organização", 250.00, "Amazon", "Bolso térmico..."),
        ("Kit Cabides Infantis", "Organização", 35.00, "Shopee", "Tamanho ideal..."),
        ("Quadro Porta-Maternidade", "Personalizados", 120.00, "Elo7", "Bordado à mão..."),
        ("Álbum do Bebê (1º Ano)", "Personalizados", 89.90, "Amazon", "Para preencher..."),
        # Os 3 novos itens adicionados para preencher os buracos do Grid:
        ("Aspirador Nasal", "Higiene", 45.90, "Amazon", "Ajuda a desobstruir o narizinho com segurança."),
        ("Babá Eletrônica", "Organização", 199.90, "Mercado Livre", "Monitoramento com áudio para tranquilidade."),
        ("Almofada Amamentação", "Alimentação", 89.90, "Shopee", "Conforto para a mãe e o bebê na hora de mamar.")
    ]
    catalogo = []
    for i, (nome, cat, valor, loja, desc) in enumerate(dados_brutos, 1):
        texto_img = urllib.parse.quote_plus(nome[:20])
        img_url = f"https://placehold.co/400x300/fdf0f3/000000.png?text={texto_img}"
        busca_mercadolivre = f"https://lista.mercadolivre.com.br/{urllib.parse.quote_plus(nome)}"
        catalogo.append({
            "id": i, "nome": nome, "categoria": cat, "valor": valor, "desc": desc, "img": img_url, "limite_fisico": 2,
            "link_mercadolivre": busca_mercadolivre,
        })
    return catalogo

CATALOGO_MIMOS = gerar_catalogo_50_mimos()

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
    payload = "000201"
    acc_info = f"0014br.gov.bcb.pix01{len(chave):02d}{chave}"
    payload += f"26{len(acc_info):02d}{acc_info}520400005303986"
    valor_str = f"{valor:.2f}"
    payload += f"54{len(valor_str):02d}{valor_str}5802BR"
    payload += f"59{len(nome):02d}{nome}60{len(cidade):02d}{cidade}62070503***6304"
    payload += calcular_crc16(payload)
    return payload

# ============================================================
# 4. FUNÇÕES DE BANCO DE DADOS (SUPABASE)
# ============================================================
@st.cache_data(ttl=30)
def checar_disponibilidade_fraldas(tamanho):
    try:
        sb = get_supabase()
        rt = sb.table("rsvp").select("id", count="exact").eq("fralda_titular", tamanho).execute()
        ra = sb.table("rsvp").select("id", count="exact").eq("fralda_acompanhante", tamanho).execute()
        return (rt.count or 0) + (ra.count or 0)
    except Exception: return 0

@st.cache_data(ttl=30)
def checar_fisicos_comprados(nome_item):
    try:
        r = get_supabase().table("rsvp").select("id", count="exact").eq("mimo_escolhido", nome_item).eq("formato_mimo", "Física").execute()
        return r.count or 0
    except Exception: return 0

def salvar_tudo_supabase(nome_titular, sexo_titular, fralda_t, formato_t, valor_t,
                         leva_acompanhante, nome_acomp, sexo_acomp, fralda_a, formato_a, valor_a,
                         qtd_filhos, mensagem, mimo_escolhido, formato_mimo, valor_mimo):
    
    total = round(valor_t + valor_a + (valor_mimo if formato_mimo == "PIX" else 0.0), 2)
    linha = {
        "nome_titular": nome_titular, "sexo_titular": sexo_titular,
        "fralda_titular": fralda_t if fralda_t else "-", "formato_fralda_titular": formato_t, "valor_pix_fralda_titular": valor_t,
        "leva_acompanhante": leva_acompanhante, "nome_acompanhante": nome_acomp, "sexo_acompanhante": sexo_acomp,
        "fralda_acompanhante": fralda_a if fralda_a else "-", "formato_fralda_acompanhante": formato_a, "valor_pix_fralda_acompanhante": valor_a,
        "qtd_criancas": qtd_filhos, "mimo_escolhido": mimo_escolhido["nome"] if mimo_escolhido else "Sem mimo",
        "categoria_mimo": mimo_escolhido["categoria"] if mimo_escolhido else "-",
        "formato_mimo": formato_mimo if mimo_escolhido else "-", "valor_pix_mimo": valor_mimo if formato_mimo == "PIX" else 0.0,
        "total_pix": total, "mensagem": mensagem
    }
    get_supabase().table("rsvp").insert(linha).execute()

def gerar_opcoes_fralda(sexo):
    opcoes = []
    if "Mulher" in sexo:
        if checar_disponibilidade_fraldas("RN") < LIMITES_FRALDAS["RN"]: opcoes.append("RN")
        if checar_disponibilidade_fraldas("P") < LIMITES_FRALDAS["P"]: opcoes.append("P")
        if not opcoes: opcoes.append("PIX Solidário (R$ 50)")
    elif "Homem" in sexo:
        if checar_disponibilidade_fraldas("M") < LIMITES_FRALDAS["M"]: opcoes.append("M")
        if checar_disponibilidade_fraldas("G") < LIMITES_FRALDAS["G"]: opcoes.append("G")
        if not opcoes: opcoes.append("PIX Solidário (R$ 50)")
    return opcoes

def exibir_bloco_presente(nome_referencia, sexo, sufixo_key):
    opcoes = gerar_opcoes_fralda(sexo)
    fralda_escolhida = st.radio(f"Opção de Fralda para {nome_referencia}:", opcoes, horizontal=True, key=f"fralda_{sufixo_key}")
    formato, valor_pix = "Física", 0.0
    if fralda_escolhida == "PIX Solidário (R$ 50)":
        formato, valor_pix = "PIX", 50.00
        st.success("Cotas de fraldas atingidas! Você foi direcionado para o PIX Solidário.")
    elif fralda_escolhida:
        formato = st.radio("Como prefere entregar esta fralda?", ["Levarei a fralda física", "Prefiro enviar o valor via PIX"], key=f"formato_{sufixo_key}")
        if "PIX" in formato:
            formato, valor_pix = "PIX", VALORES_PIX[fralda_escolhida]
            st.info(f"Valor sugerido para o pacote **{fralda_escolhida}**: R$ {valor_pix:.2f}")
    return fralda_escolhida, formato, valor_pix

# ============================================================
# 5. MAIN (INTERFACE)
# ============================================================
def main():
    
    # ── BARRA FIXA ──
    st.markdown("""
    <div class="steps-container">
        <div class="steps-bar">
            <div class="step"><div class="step-num active">1</div><div class="step-label active">Seus dados</div></div>
            <div class="step-line done"></div>
            <div class="step"><div class="step-num">2</div><div class="step-label">Fraldas</div></div>
            <div class="step-line"></div>
            <div class="step"><div class="step-num">3</div><div class="step-label">Mimos</div></div>
            <div class="step-line"></div>
            <div class="step"><div class="step-num">4</div><div class="step-label">Confirmar</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO BANNER AZUL ──
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✨ Você está convidado</div>
        <h1>Chá de Bebê do Bernardo</h1>
        <p class="hero-sub">Confirme sua presença e escolha um presentinho especial 🍯</p>
        <div class="hero-data">
            <div class="hero-data-item"><div class="label">📅 Data</div><div class="value">18/07/2026</div></div>
            <div class="hero-data-item"><div class="label">📍 Local</div><div class="value">Cotia · SP</div></div>
            <div class="hero-data-item"><div class="label">🍼 Bebê</div><div class="value">Bernardo</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CHAMADA POTES DE MEL ──
    st.markdown("""
    <div class="chamada-card">
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
    </div>
    """, unsafe_allow_html=True)

    # Envolvendo o formulário em cartões brancos para destacar do fundo colorido
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='secao-titulo'>1. Confirmação de Presença e Fraldas</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: nome_titular = st.text_input("Seu Nome Completo:")
    with c2: sexo_titular = st.selectbox("Seu Sexo:", ["Selecione...", "Mulher 🚺", "Homem 🚹"])

    fralda_t, formato_t, valor_t = None, "-", 0.0
    if sexo_titular != "Selecione...":
        st.markdown("#### Seu Presente 🎁 (Fraldas)")
        fralda_t, formato_t, valor_t = exibir_bloco_presente("você", sexo_titular, "t")

    st.markdown("---")
    leva_acompanhante = st.radio("Você levará um acompanhante adulto? (Ex: Esposa, Marido)", ["Não", "Sim"], horizontal=True)
    nome_acomp, sexo_acomp, fralda_a, formato_a, valor_a = "", "Selecione...", None, "-", 0.0

    if leva_acompanhante == "Sim":
        st.markdown("#### Dados do Acompanhante")
        ca1, ca2 = st.columns(2)
        with ca1: nome_acomp = st.text_input("Nome do Acompanhante:")
        with ca2: sexo_acomp = st.selectbox("Sexo do Acompanhante:", ["Selecione...", "Mulher 🚺", "Homem 🚹"], key="sexo_a")
        if sexo_acomp != "Selecione...":
            st.markdown("#### Presente do Acompanhante 🎁 (Fraldas)")
            fralda_a, formato_a, valor_a = exibir_bloco_presente("o acompanhante", sexo_acomp, "a")
        else:
            fralda_a, formato_a, valor_a = None, "-", 0.0

    qtd_filhos = st.number_input("Quantidade de crianças que irão com vocês:", min_value=0, max_value=10, value=0, step=1)
    mensagem = st.text_area("Deixe uma mensagem para o Bernardo (Opcional):")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='secao-titulo'>2. Mimo Extra para o Bernardo</div>", unsafe_allow_html=True)
    
    st.info("Além das fraldinhas, preparamos uma **vitrine com algumas sugestões de coisinhas que o Bernardo vai precisar**.")
    
    quer_mimo = st.radio("**Deseja adicionar um mimo extra ao seu presente?**", ["Não, vou presentear apenas com as fraldas.", "Sim, quero escolher um mimo!"], index=0)

    mimo_escolhido = None
    formato_mimo = "-"
    valor_mimo = 0.0

    if quer_mimo == "Sim, quero escolher um mimo!":
        st.markdown("#### 🛍️ Vitrine de Mimos")
        with st.expander("👀 Clique aqui para ver as fotos dos mimos disponíveis", expanded=True):
            
            grid_html = '<div class="vitrine-grid">'
            for item in CATALOGO_MIMOS:
                grid_html += '<div class="vitrine-card">'
                grid_html += f'<div class="vitrine-img-container"><img src="{item["img"]}"></div>'
                grid_html += f'<h4 class="vitrine-titulo">{item["nome"]}</h4>'
                grid_html += f'<p class="vitrine-preco">R$ {item["valor"]:.2f}</p>'
                grid_html += '<div class="preco-botoes">'
                grid_html += f'<a class="preco-btn btn-ml" href="{item["link_mercadolivre"]}" target="_blank">🛍 Mercado Livre</a>'
                grid_html += '</div></div>'
            grid_html += '</div>'
            
            st.markdown(grid_html, unsafe_allow_html=True)

        st.markdown("---")
        nomes_mimos = [m["nome"] for m in CATALOGO_MIMOS]
        mimo_selecionado = st.selectbox("**Qual mimo você escolheu da vitrine acima?**", ["Selecione um mimo..."] + nomes_mimos)
        if mimo_selecionado != "Selecione um mimo...":
            info_mimo = next(m for m in CATALOGO_MIMOS if m["nome"] == mimo_selecionado)
            st.success(f"Ótima escolha! **{info_mimo['nome']}** - R$ {info_mimo['valor']:.2f}")
            st.markdown(f"""🔎 **Pesquise preços:** &nbsp;&nbsp;[🟡 Mercado Livre]({info_mimo['link_mercadolivre']})""")
            fisicos_comprados = checar_fisicos_comprados(info_mimo["nome"])
            opcoes_entrega_m = ["Enviar valor via PIX (Recomendado)"]
            if fisicos_comprados < info_mimo["limite_fisico"]:
                opcoes_entrega_m.insert(0, "Levarei o produto físico no chá")
            else:
                st.warning("Já recebemos a cota física deste item! Disponível apenas via envio do PIX.")
            formato_mimo_radio = st.radio("Como você entregará este mimo?", opcoes_entrega_m)
            mimo_escolhido = info_mimo
            if "PIX" in formato_mimo_radio:
                formato_mimo = "PIX"
                valor_mimo = info_mimo["valor"]
            else:
                formato_mimo = "Física"
                valor_mimo = 0.0
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='secao-titulo'>3. Finalizar Confirmação</div>", unsafe_allow_html=True)
    if st.button("Confirmar Tudo e Gerar Resumo 🚀"):
        if not nome_titular or sexo_titular == "Selecione...":
            st.error("Por favor, preencha o seu nome e sexo no topo da página.")
        elif quer_mimo == "Sim, quero escolher um mimo!" and not mimo_escolhido:
            st.error("Você marcou que deseja dar um mimo. Por favor, selecione-o na lista acima.")
        else:
            with st.spinner("Salvando as informações..."):
                try:
                    salvar_tudo_supabase(
                        nome_titular.strip(), sexo_titular, fralda_t, formato_t, valor_t,
                        leva_acompanhante, nome_acomp.strip() if leva_acompanhante == "Sim" else "-", 
                        sexo_acomp if leva_acompanhante == "Sim" else "-", 
                        fralda_a if leva_acompanhante == "Sim" else "-", 
                        formato_a if leva_acompanhante == "Sim" else "-", 
                        valor_a if leva_acompanhante == "Sim" else 0.0,
                        int(qtd_filhos), mensagem, mimo_escolhido, formato_mimo, valor_mimo
                    )
                    
                    total_pix = valor_t + valor_a + valor_mimo
                    st.balloons()
                    st.success(f"Presença confirmada com sucesso! Muito obrigado, {nome_titular}. ❤️")
                    
                    st.markdown("### 📋 Seu Resumo:")
                    st.write(f"- Fralda ({nome_titular}): {fralda_t} - {formato_t} (R$ {valor_t:.2f})")
                    if leva_acompanhante == "Sim":
                        st.write(f"- Fralda (Acompanhante): {fralda_a} - {formato_a} (R$ {valor_a:.2f})")
                    if mimo_escolhido:
                        st.write(f"- Mimo Extra: {mimo_escolhido['nome']} - {formato_mimo} (R$ {valor_mimo:.2f})")
                    st.markdown(f"**TOTAL A PAGAR NO PIX: R$ {total_pix:.2f}**")

                    if total_pix > 0:
                        st.markdown("---")
                        st.markdown("### 📱 Realizar Pagamento (PIX)")
                        st.info("Abra o aplicativo do seu banco, escolha 'PIX QR Code' e aponte a câmera para a imagem abaixo, ou use o Copia e Cola.")
                        payload_pix = gerar_payload_pix(CHAVE_PIX, total_pix)
                        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(payload_pix)}"
                        col_qr, col_txt = st.columns([1, 2])
                        with col_qr:
                            st.image(qr_url)
                        with col_txt:
                            st.write("**Opção 1: PIX Copia e Cola**")
                            st.code(payload_pix, language="text")
                            st.write("**Opção 2: Chave Celular Direta**")
                            st.code(CHAVE_PIX, language="text")
                    else:
                        st.success("Tudo certo! Te esperamos na festa com os presentes físicos.")

                except Exception as e:
                    st.error(f"Erro de conexão com o banco de dados. Detalhe: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
