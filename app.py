import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from supabase import create_client

# ============================================================
# 1. SUPABASE — conexão via Secrets
# ============================================================
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# ============================================================
# 2. CONFIGURAÇÕES GLOBAIS
# ============================================================
st.set_page_config(page_title="Chá de Bebê - Bernardo", layout="wide", page_icon="🍼")

st.markdown("""
    <style>
    div.stButton > button { background-color: #fca3b7; color: white; border-radius: 20px; border: none; font-weight: bold; width: 100%; transition: all 0.3s; padding: 12px; font-size: 16px;}
    div.stButton > button:hover { background-color: #ff859f; color: white; }
    div.stAlert { background-color: #e6f3ff; border-radius: 10px; border-left: 5px solid #87ceeb; color: #00529B; }
    .vitrine-card { background-color: #ffffff; border-radius: 15px; padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.3s ease; margin-bottom: 20px; border: 1px solid #f0f0f0; }
    .vitrine-card:hover { transform: translateY(-8px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    .vitrine-img-container { position: relative; border-radius: 10px; overflow: hidden; margin-bottom: 12px; }
    .vitrine-img-container img { width: 100%; height: auto; display: block; }
    .vitrine-titulo { font-size: 16px; font-weight: 800; color: #444; margin: 0 0 5px 0; line-height: 1.2; }
    .secao-titulo { color: #d6336c; margin-top: 30px; margin-bottom: 15px; font-weight: 800; border-bottom: 2px solid #fca3b7; padding-bottom: 5px;}
    .preco-botoes { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 8px; }
    .preco-btn { display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 700; text-decoration: none !important; color: white !important; }
    .btn-buscape  { background: #e8401c; }
    .btn-google   { background: #4285F4; }
    .btn-ml       { background: #FFE600; color: #333 !important; }
    .vitrine-preco { font-size: 15px; font-weight: 800; color: #d6336c; margin: 4px 0; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 3. REGRAS DE NEGÓCIO
# ============================================================
LIMITES_FRALDAS = {"RN": 20, "P": 40, "M": 40, "G": 30}
VALORES_PIX     = {"RN": 40.00, "P": 45.00, "M": 50.00, "G": 50.00, "PIX Solidário (R$ 50)": 50.00}
CHAVE_PIX       = "11963766575"

# ============================================================
# 4. CATÁLOGO DE MIMOS
# ============================================================
@st.cache_data
def gerar_catalogo_50_mimos():
    dados_brutos = [
        ("Lenços Umedecidos (Leve 4)",   "Higiene",       39.90,  "Shopee",         "Kit de lenços para pele sensível sem perfume."),
        ("Pomada Antiassaduras",          "Higiene",       25.50,  "Natura",         "Proteção prolongada com vitaminas e óleos."),
        ("Kit Cotonetes Infantis",        "Higiene",       15.00,  "Mercado Livre",  "Hastes flexíveis com ponta de segurança."),
        ("Sabonete Líquido RN",           "Higiene",       32.90,  "Natura",         "Da cabeça aos pés, não arde os olhos."),
        ("Álcool 70% e Algodão",          "Higiene",       22.00,  "Amazon",         "Para a higiene do coto umbilical do bebê."),
        ("Banheira Ergonômica",           "Banho",         89.90,  "Amazon",         "Banheira com apoio de segurança anatômico."),
        ("Toalha com Capuz",              "Banho",         55.00,  "Elo7",           "Toalha 100% algodão super absorvente."),
        ("Termômetro de Banho",           "Banho",         28.50,  "Shopee",         "Mede a temperatura da água no formato de bichinho."),
        ("Esponja Natural Soft",          "Banho",         19.90,  "Amazon",         "Esponja extra macia para recém-nascidos."),
        ("Naninha de Ovelha",             "Naninhas",      49.90,  "Elo7",           "Paninho de apego macio com pelúcia."),
        ("Chupeta RN Calmante",           "Naninhas",      35.00,  "Amazon",         "Chupeta de silicone inteiriça ortodôntica."),
        ("Manta Leve Algodão",            "Naninhas",      60.00,  "Mercado Livre",  "Ideal para dias de meia-estação."),
        ("Ninho Redutor de Berço",        "Naninhas",     130.00,  "Elo7",           "Simula o útero materno para um sono tranquilo."),
        ("Kit 3 Bodys Manga Longa",       "Roupinhas",     79.90,  "Amazon",         "Cores neutras, 100% algodão suedine."),
        ("Kit Mijões (Culote)",           "Roupinhas",     55.00,  "Shopee",         "Calças com pezinho reversível super práticas."),
        ("Macacão Plush",                 "Roupinhas",     89.00,  "Magazine Luiza", "Macacão quentinho para noites frias."),
        ("Luvinhas e Touca",              "Roupinhas",     35.00,  "Shopee",         "Evita que o bebê se arranhe nos primeiros dias."),
        ("Móbile de Berço Musical",       "Brinquedos",   145.00,  "Amazon",         "Estimula a visão e acalma com cantigas."),
        ("Chocalho Macio",                "Brinquedos",    32.00,  "Shopee",         "Barulhinho suave e formato fácil de segurar."),
        ("Mordedor de Silicone",          "Brinquedos",    28.90,  "Natura",         "Alivia o desconforto das gengivas."),
        ("Livrinho de Pano",              "Brinquedos",    45.00,  "Amazon",         "Livro sensorial que pode ir na boca e na água."),
        ("Kit 2 Mamadeiras Anticólica",   "Alimentação",  120.00,  "Amazon",         "Sistema de ventilação para reduzir gases."),
        ("Escova para Mamadeira",         "Alimentação",   25.00,  "Shopee",         "Alcança os cantos difíceis das garrafinhas."),
        ("Potes Armazenamento Leite",     "Alimentação",   65.00,  "Amazon",         "Recipientes com tampa hermética e medição."),
        ("Trocador Portátil de Bolsa",    "Organização",   55.00,  "Elo7",           "Impermeável, fecha como uma bolsinha."),
        ("Mochila Maternidade",           "Organização",  250.00,  "Amazon",         "Múltiplos compartimentos e bolso térmico."),
        ("Kit Cabides Infantis",          "Organização",   35.00,  "Shopee",         "Tamanho ideal para as roupinhas pequenas."),
        ("Quadro Porta-Maternidade",      "Personalizados",120.00, "Elo7",           "Bordado à mão com o nome do Bernardo."),
        ("Álbum do Bebê (Primeiro Ano)",  "Personalizados", 89.90, "Amazon",         "Para preencher as conquistas de cada mês.")
    ]
    catalogo = []
    for i, (nome, cat, valor, loja, desc) in enumerate(dados_brutos, 1):
        texto_img  = urllib.parse.quote_plus(nome[:20])
        img_url    = f"https://placehold.co/400x300/fdf0f3/d6336c.png?text={texto_img}"
        termo      = urllib.parse.quote_plus(nome + " bebe")
        catalogo.append({
            "id": i, "nome": nome, "categoria": cat, "valor": valor,
            "desc": desc, "img": img_url, "limite_fisico": 2,
            "link_buscape":       f"https://www.buscape.com.br/busca?q={urllib.parse.quote_plus(nome)}",
            "link_google":        f"https://www.google.com.br/search?q={termo}&tbm=shop",
            "link_mercadolivre":  f"https://lista.mercadolivre.com.br/{urllib.parse.quote_plus(nome)}",
        })
    return catalogo

CATALOGO_MIMOS = gerar_catalogo_50_mimos()

# ============================================================
# 5. GERADOR DE QR CODE PIX (ALGORITMO BCB)
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
    payload  = "000201"
    acc_info = f"0014br.gov.bcb.pix01{len(chave):02d}{chave}"
    payload += f"26{len(acc_info):02d}{acc_info}"
    payload += "52040000"
    payload += "5303986"
    valor_str = f"{valor:.2f}"
    payload += f"54{len(valor_str):02d}{valor_str}"
    payload += "5802BR"
    payload += f"59{len(nome):02d}{nome}"
    payload += f"60{len(cidade):02d}{cidade}"
    payload += "62070503***"
    payload += "6304"
    payload += calcular_crc16(payload)
    return payload

# ============================================================
# 6. FUNÇÕES DE BANCO DE DADOS — SUPABASE
#
#  Tabela esperada no Supabase (SQL para criar):
#
#  create table rsvp (
#    id                              bigserial primary key,
#    nome_titular                    text,
#    sexo_titular                    text,
#    fralda_titular                  text,
#    formato_fralda_titular          text,
#    valor_pix_fralda_titular        numeric,
#    leva_acompanhante               text,
#    nome_acompanhante               text,
#    sexo_acompanhante               text,
#    fralda_acompanhante             text,
#    formato_fralda_acompanhante     text,
#    valor_pix_fralda_acompanhante   numeric,
#    qtd_criancas                    int,
#    mimo_escolhido                  text,
#    categoria_mimo                  text,
#    formato_mimo                    text,
#    valor_pix_mimo                  numeric,
#    total_pix                       numeric,
#    mensagem                        text,
#    data_confirmacao                timestamptz default now()
#  );
# ============================================================

def salvar_tudo_supabase(dados_rsvp: dict, mimo: dict | None, formato_mimo: str, valor_mimo: float):
    """Insere uma linha unificada (RSVP + mimo) na tabela 'rsvp' do Supabase."""
    supabase = get_supabase()

    val_titular    = dados_rsvp.get("Valor PIX Fralda Titular (R$)", 0.0)
    val_acomp      = dados_rsvp.get("Valor PIX Fralda Acompanhante (R$)", 0.0)
    val_mimo_final = valor_mimo if formato_mimo == "PIX" else 0.0
    total_pix      = round(val_titular + val_acomp + val_mimo_final, 2)

    linha = {
        # ── Titular ───────────────────────────────────────────
        "nome_titular":                  dados_rsvp.get("Nome Titular", ""),
        "sexo_titular":                  dados_rsvp.get("Sexo Titular", ""),
        "fralda_titular":                dados_rsvp.get("Fralda Titular", ""),
        "formato_fralda_titular":        dados_rsvp.get("Formato Fralda Titular", ""),
        "valor_pix_fralda_titular":      val_titular,
        # ── Acompanhante ──────────────────────────────────────
        "leva_acompanhante":             dados_rsvp.get("Leva Acompanhante", "Não"),
        "nome_acompanhante":             dados_rsvp.get("Nome Acompanhante", "-"),
        "sexo_acompanhante":             dados_rsvp.get("Sexo Acompanhante", "-"),
        "fralda_acompanhante":           dados_rsvp.get("Fralda Acompanhante", "-"),
        "formato_fralda_acompanhante":   dados_rsvp.get("Formato Fralda Acompanhante", "-"),
        "valor_pix_fralda_acompanhante": val_acomp,
        # ── Crianças ──────────────────────────────────────────
        "qtd_criancas":                  dados_rsvp.get("Qtd Crianças", 0),
        # ── Mimo ──────────────────────────────────────────────
        "mimo_escolhido":  mimo["nome"]      if mimo else "Sem mimo",
        "categoria_mimo":  mimo["categoria"] if mimo else "-",
        "formato_mimo":    formato_mimo      if mimo else "-",
        "valor_pix_mimo":  val_mimo_final,
        # ── Totais / Controle ─────────────────────────────────
        "total_pix":       total_pix,
        "mensagem":        dados_rsvp.get("Mensagem", ""),
        # data_confirmacao é preenchida automaticamente pelo default now() do Supabase
    }

    try:
        get_supabase().table("rsvp").insert(linha).execute()
    except Exception as e:
        st.error(f"Erro ao salvar no banco de dados: {e}")
        raise


@st.cache_data(ttl=30)   # cache de 30 s para não sobrecarregar o Supabase
def checar_disponibilidade_fraldas(tamanho: str) -> int:
    """Conta quantas vezes um tamanho de fralda já foi confirmado."""
    try:
        supabase = get_supabase()
        r_titular = (
            supabase.table("rsvp")
            .select("id", count="exact")
            .eq("fralda_titular", tamanho)
            .execute()
        )
        r_acomp = (
            supabase.table("rsvp")
            .select("id", count="exact")
            .eq("fralda_acompanhante", tamanho)
            .execute()
        )
        return (r_titular.count or 0) + (r_acomp.count or 0)
    except Exception:
        return 0


@st.cache_data(ttl=30)
def checar_fisicos_comprados(nome_item: str) -> int:
    """Conta quantas entregas físicas de um mimo já foram confirmadas."""
    try:
        r = (
            get_supabase().table("rsvp")
            .select("id", count="exact")
            .eq("mimo_escolhido", nome_item)
            .eq("formato_mimo", "Física")
            .execute()
        )
        return r.count or 0
    except Exception:
        return 0

# ============================================================
# 7. LÓGICA DE FRALDAS E FORMULÁRIO
# ============================================================
def gerar_opcoes_fralda(sexo):
    opcoes = []
    if "Mulher" in sexo:
        if checar_disponibilidade_fraldas("RN") < LIMITES_FRALDAS["RN"]:
            opcoes.append("RN")
        if checar_disponibilidade_fraldas("P") < LIMITES_FRALDAS["P"]:
            opcoes.append("P")
        if not opcoes:
            opcoes.append("PIX Solidário (R$ 50)")
    elif "Homem" in sexo:
        if checar_disponibilidade_fraldas("M") < LIMITES_FRALDAS["M"]:
            opcoes.append("M")
        if checar_disponibilidade_fraldas("G") < LIMITES_FRALDAS["G"]:
            opcoes.append("G")
        if not opcoes:
            opcoes.append("PIX Solidário (R$ 50)")
    return opcoes


def exibir_bloco_presente(nome_referencia, sexo, sufixo_key):
    opcoes = gerar_opcoes_fralda(sexo)
    fralda_escolhida = st.radio(
        f"Opção de Fralda para {nome_referencia}:", opcoes,
        horizontal=True, key=f"fralda_{sufixo_key}"
    )
    formato, valor_pix = "Física", 0.0

    if fralda_escolhida == "PIX Solidário (R$ 50)":
        formato, valor_pix = "PIX", 50.00
        st.success("Cotas de fraldas atingidas! Você foi direcionado para o PIX Solidário.")
    elif fralda_escolhida:
        formato = st.radio(
            "Como prefere entregar esta fralda?",
            ["Levarei a fralda física", "Prefiro enviar o valor via PIX"],
            key=f"formato_{sufixo_key}"
        )
        if "PIX" in formato:
            formato, valor_pix = "PIX", VALORES_PIX[fralda_escolhida]
            st.info(f"Valor sugerido para o pacote **{fralda_escolhida}**: R$ {valor_pix:.2f}")

    return fralda_escolhida, formato, valor_pix

# ============================================================
# 8. MAIN
# ============================================================
def main():
    st.markdown("<h2 style='text-align:center;color:#5a5a5a;'>🍼 Confirmação e Lista de Presentes</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#d6336c;font-size:22px;font-weight:bold;'>🍯 Prepare os potes de mel porque o Chá de Bebê do Bernardo está chegando! 🍯</p>", unsafe_allow_html=True)

    # ── ETAPA 1: RSVP ────────────────────────────────────────
    st.markdown("<div class='secao-titulo'>1. Confirmação de Presença e Fraldas</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: nome_titular  = st.text_input("Seu Nome Completo:")
    with c2: sexo_titular  = st.selectbox("Seu Sexo:", ["Selecione...", "Mulher 🚺", "Homem 🚹"])

    fralda_t, formato_t, valor_t = None, "-", 0.0
    if sexo_titular != "Selecione...":
        fralda_t, formato_t, valor_t = exibir_bloco_presente("você", sexo_titular, "t")

    st.markdown("---")
    leva_acompanhante = st.radio(
        "Você levará um acompanhante adulto? (Ex: Esposa, Marido)",
        ["Não", "Sim"], horizontal=True
    )
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
    mensagem   = st.text_area("Deixe uma mensagem para o Bernardo (Opcional):")

    # ── ETAPA 2: MIMOS ───────────────────────────────────────
    st.markdown("<div class='secao-titulo'>2. Mimo Extra para o Bernardo</div>", unsafe_allow_html=True)
    st.info("Além das fraldinhas, preparamos uma vitrine com sugestões de coisinhas que o Bernardo vai precisar.")

    quer_mimo = st.radio(
        "**Deseja adicionar um mimo extra ao seu presente?**",
        ["Não, vou presentear apenas com as fraldas.", "Sim, quero escolher um mimo!"],
        index=0
    )

    mimo_escolhido = None
    formato_mimo   = "-"
    valor_mimo     = 0.0

    if quer_mimo == "Sim, quero escolher um mimo!":
        st.markdown("#### 🛍️ Vitrine de Mimos")

        with st.expander("👀 Clique aqui para ver as fotos dos mimos disponíveis", expanded=True):
            colunas = st.columns(4)
            for idx, item in enumerate(CATALOGO_MIMOS):
                with colunas[idx % 4]:
                    card_html = f"""
                    <div class="vitrine-card">
                        <div class="vitrine-img-container"><img src="{item['img']}"></div>
                        <h4 class="vitrine-titulo">{item['nome']}</h4>
                        <p class="vitrine-preco">R$ {item['valor']:.2f}</p>
                        <div class="preco-botoes">
                            <a class="preco-btn btn-buscape" href="{item['link_buscape']}"      target="_blank">🔍 Buscapé</a>
                            <a class="preco-btn btn-google"  href="{item['link_google']}"       target="_blank">🛒 Google</a>
                            <a class="preco-btn btn-ml"      href="{item['link_mercadolivre']}" target="_blank">🛍 Mercado Livre</a>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)

        st.markdown("---")
        nomes_mimos    = [m["nome"] for m in CATALOGO_MIMOS]
        mimo_selecionado = st.selectbox("**Qual mimo você escolheu da vitrine acima?**", ["Selecione um mimo..."] + nomes_mimos)

        if mimo_selecionado != "Selecione um mimo...":
            info_mimo = next(m for m in CATALOGO_MIMOS if m["nome"] == mimo_selecionado)
            st.success(f"Ótima escolha! **{info_mimo['nome']}** - R$ {info_mimo['valor']:.2f}")
            st.markdown(
                f"🔎 **Compare preços antes de comprar:**  \n"
                f"[🔴 Buscapé]({info_mimo['link_buscape']}) &nbsp;|&nbsp; "
                f"[🔵 Google Shopping]({info_mimo['link_google']}) &nbsp;|&nbsp; "
                f"[🟡 Mercado Livre]({info_mimo['link_mercadolivre']})"
            )

            fisicos_comprados  = checar_fisicos_comprados(info_mimo["nome"])
            opcoes_entrega_m   = ["Enviar valor via PIX (Recomendado)"]
            if fisicos_comprados < info_mimo["limite_fisico"]:
                opcoes_entrega_m.insert(0, "Levarei o produto físico no chá")
            else:
                st.warning("Já recebemos a cota física deste item! Disponível apenas via envio do PIX.")

            formato_mimo_radio = st.radio("Como você entregará este mimo?", opcoes_entrega_m)
            mimo_escolhido     = info_mimo

            if "PIX" in formato_mimo_radio:
                formato_mimo = "PIX"
                valor_mimo   = info_mimo["valor"]
            else:
                formato_mimo = "Física"
                valor_mimo   = 0.0

    # ── ETAPA 3: FINALIZAR ───────────────────────────────────
    st.markdown("<div class='secao-titulo'>3. Finalizar Confirmação</div>", unsafe_allow_html=True)

    if st.button("Confirmar Tudo e Gerar Resumo 🚀"):
        if not nome_titular or sexo_titular == "Selecione...":
            st.error("Por favor, preencha o seu nome e sexo no topo da página.")
        elif quer_mimo == "Sim, quero escolher um mimo!" and not mimo_escolhido:
            st.error("Você marcou que deseja dar um mimo. Por favor, selecione-o na lista acima.")
        else:
            dados_rsvp = {
                "Nome Titular":                       nome_titular.strip(),
                "Sexo Titular":                       sexo_titular,
                "Fralda Titular":                     fralda_t,
                "Formato Fralda Titular":             formato_t,
                "Valor PIX Fralda Titular (R$)":      valor_t,
                "Leva Acompanhante":                  leva_acompanhante,
                "Nome Acompanhante":                  nome_acomp.strip() if leva_acompanhante == "Sim" else "-",
                "Sexo Acompanhante":                  sexo_acomp        if leva_acompanhante == "Sim" else "-",
                "Fralda Acompanhante":                fralda_a          if leva_acompanhante == "Sim" else "-",
                "Formato Fralda Acompanhante":        formato_a         if leva_acompanhante == "Sim" else "-",
                "Valor PIX Fralda Acompanhante (R$)": valor_a           if leva_acompanhante == "Sim" else 0.0,
                "Qtd Crianças":                       int(qtd_filhos),
                "Mensagem":                           mensagem,
            }

            with st.spinner("Salvando sua confirmação..."):
                salvar_tudo_supabase(dados_rsvp, mimo_escolhido, formato_mimo, valor_mimo)
                # Limpa cache de contagens para refletir o novo registro imediatamente
                checar_disponibilidade_fraldas.clear()
                checar_fisicos_comprados.clear()

            total_pix = valor_t + valor_a + (valor_mimo if formato_mimo == "PIX" else 0.0)

            st.balloons()
            st.success(f"Presença confirmada com sucesso! Muito obrigado, {nome_titular}. ❤️")

            st.markdown("### 📋 Seu Resumo:")
            st.write(f"- Fralda ({nome_titular}): {fralda_t} — {formato_t} (R$ {valor_t:.2f})")
            if leva_acompanhante == "Sim":
                st.write(f"- Fralda (Acompanhante): {fralda_a} — {formato_a} (R$ {valor_a:.2f})")
            if mimo_escolhido:
                st.write(f"- Mimo Extra: {mimo_escolhido['nome']} — {formato_mimo} (R$ {valor_mimo:.2f})")
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

if __name__ == "__main__":
    main()
