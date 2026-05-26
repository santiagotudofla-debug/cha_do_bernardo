import streamlit as st
import pandas as pd
import os
import urllib.parse

st.set_page_config(page_title="Chá de Bebê - Confirmação", layout="wide", page_icon="🍼")

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

DATA_FILE = "rsvp_cascata_pix.csv"
MIMOS_FILE = "mimos_comprados.csv"

LIMITES_FRALDAS = {"RN": 20, "P": 40, "M": 40, "G": 30}
VALORES_PIX = {"RN": 40.00, "P": 45.00, "M": 50.00, "G": 60.00, "PIX Solidário (R$ 50)": 50.00}

CHAVE_PIX = "11963766575"

@st.cache_data
def gerar_catalogo_50_mimos():
    dados_brutos = [
        ("Lenços Umedecidos (Leve 4)", "Higiene", 39.90, "Shopee", "Kit de lenços para pele sensível sem perfume."),
        ("Pomada Antiassaduras", "Higiene", 25.50, "Natura", "Proteção prolongada com vitaminas e óleos."),
        ("Kit Cotonetes Infantis", "Higiene", 15.00, "Mercado Livre", "Hastes flexíveis com ponta de segurança."),
        ("Sabonete Líquido RN", "Higiene", 32.90, "Natura", "Da cabeça aos pés, não arde os olhos."),
        ("Álcool 70% e Algodão", "Higiene", 22.00, "Amazon", "Para a higiene do coto umbilical do bebê."),
        ("Banheira Ergonômica", "Banho", 89.90, "Amazon", "Banheira com apoio de segurança anatômico."),
        ("Toalha com Capuz", "Banho", 55.00, "Elo7", "Toalha 100% algodão super absorvente."),
        ("Termômetro de Banho", "Banho", 28.50, "Shopee", "Mede a temperatura da água no formato de bichinho."),
        ("Esponja Natural Soft", "Banho", 19.90, "Amazon", "Esponja extra macia para recém-nascidos."),
        ("Naninha de Ovelha", "Naninhas", 49.90, "Elo7", "Paninho de apego macio com pelúcia."),
        ("Chupeta RN Calmante", "Naninhas", 35.00, "Amazon", "Chupeta de silicone inteiriça ortodôntica."),
        ("Manta Leve Algodão", "Naninhas", 60.00, "Mercado Livre", "Ideal para dias de meia-estação."),
        ("Ninho Redutor de Berço", "Naninhas", 130.00, "Elo7", "Simula o útero materno para um sono tranquilo."),
        ("Kit 3 Bodys Manga Longa", "Roupinhas", 79.90, "Amazon", "Cores neutras, 100% algodão suedine."),
        ("Kit Mijões (Culote)", "Roupinhas", 55.00, "Shopee", "Calças com pezinho reversível super práticas."),
        ("Macacão Plush", "Roupinhas", 89.00, "Magazine Luiza", "Macacão quentinho para noites frias."),
        ("Luvinhas e Touca", "Roupinhas", 35.00, "Shopee", "Evita que o bebê se arranhe nos primeiros dias."),
        ("Móbile de Berço Musical", "Brinquedos", 145.00, "Amazon", "Estimula a visão e acalma com cantigas."),
        ("Chocalho Macio", "Brinquedos", 32.00, "Shopee", "Barulhinho suave e formato fácil de segurar."),
        ("Mordedor de Silicone", "Brinquedos", 28.90, "Natura", "Alivia o desconforto das gengivas."),
        ("Livrinho de Pano", "Brinquedos", 45.00, "Amazon", "Livro sensorial que pode ir na boca e na água."),
        ("Kit 2 Mamadeiras Anticólica", "Alimentação", 120.00, "Amazon", "Sistema de ventilação para reduzir gases."),
        ("Escova para Mamadeira", "Alimentação", 25.00, "Shopee", "Alcança os cantos difíceis das garrafinhas."),
        ("Potes Armazenamento Leite", "Alimentação", 65.00, "Amazon", "Recipientes com tampa hermética e medição."),
        ("Trocador Portátil de Bolsa", "Organização", 55.00, "Elo7", "Impermeável, fecha como uma bolsinha."),
        ("Mochila Maternidade", "Organização", 250.00, "Amazon", "Múltiplos compartimentos e bolso térmico."),
        ("Kit Cabides Infantis", "Organização", 35.00, "Shopee", "Tamanho ideal para as roupinhas pequenas."),
        ("Quadro Porta-Maternidade", "Personalizados", 120.00, "Elo7", "Bordado à mão com o nome do Bernardo."),
        ("Álbum do Bebê (Primeiro Ano)", "Personalizados", 89.90, "Amazon", "Para preencher as conquistas de cada mês.")
    ]
    catalogo = []
    for i, (nome, cat, valor, loja, desc) in enumerate(dados_brutos, 1):
        texto_img = urllib.parse.quote_plus(nome[:20])
        img_url = f"https://placehold.co/400x300/fdf0f3/d6336c.png?text={texto_img}"
        termo_busca = urllib.parse.quote_plus(nome + " bebe")
        # Links para os principais comparadores/marketplaces brasileiros
        busca_buscape   = f"https://www.buscape.com.br/busca?q={urllib.parse.quote_plus(nome)}"
        busca_google    = f"https://www.google.com.br/search?q={termo_busca}&tbm=shop"
        busca_mercadolivre = f"https://lista.mercadolivre.com.br/{urllib.parse.quote_plus(nome)}"
        catalogo.append({
            "id": i, "nome": nome, "categoria": cat, "valor": valor, "desc": desc,
            "img": img_url, "limite_fisico": 2,
            "link_buscape": busca_buscape,
            "link_google": busca_google,
            "link_mercadolivre": busca_mercadolivre,
        })
    return catalogo

# CORREÇÃO: era gerar_catalogo_49_mimos() — nome inconsistente com a função definida acima
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

def inicializar_bancos():
    if not os.path.exists(DATA_FILE): pd.DataFrame(columns=["Nome Titular", "Sexo Titular", "Fralda Titular", "Formato Titular", "Valor PIX Titular", "Leva Acompanhante", "Nome Acompanhante", "Sexo Acompanhante", "Fralda Acompanhante", "Formato Acompanhante", "Valor PIX Acompanhante", "Qtd Filhos", "Mensagem"]).to_csv(DATA_FILE, index=False)
    if not os.path.exists(MIMOS_FILE): pd.DataFrame(columns=["Nome Convidado", "ID Item", "Item", "Formato", "Valor"]).to_csv(MIMOS_FILE, index=False)

def salvar_confirmacao_rsvp(dados_dict):
    df = pd.read_csv(DATA_FILE)
    nova_entrada = pd.DataFrame([dados_dict])
    df = pd.concat([df, nova_entrada], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def salvar_mimo(nome, id_item, nome_item, formato, valor):
    df = pd.read_csv(MIMOS_FILE)
    nova_linha = pd.DataFrame([{"Nome Convidado": nome, "ID Item": id_item, "Item": nome_item, "Formato": formato, "Valor": valor}])
    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_csv(MIMOS_FILE, index=False)

def checar_disponibilidade_fraldas(tamanho):
    df = pd.read_csv(DATA_FILE)
    if df.empty: return 0
    return (df["Fralda Titular"] == tamanho).sum() + (df["Fralda Acompanhante"] == tamanho).sum()

def checar_fisicos_comprados(id_item):
    df = pd.read_csv(MIMOS_FILE)
    if df.empty: return 0
    return ((df["ID Item"] == id_item) & (df["Formato"] == "Física")).sum()

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

def main():
    inicializar_bancos()
    st.markdown("<h2 style='text-align: center; color: #5a5a5a;'>🍼 Confirmação e Lista de Presentes</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d6336c; font-size: 22px; font-weight: bold;'>🍯Prepare os potes de mel porque o Chá de Bebê do Bernardo está chegando!🍯</p>", unsafe_allow_html=True)

    st.markdown("<div class='secao-titulo'>1. Confirmação de Presença e Fraldas</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: nome_titular = st.text_input("Seu Nome Completo:")
    with c2: sexo_titular = st.selectbox("Seu Sexo:", ["Selecione...", "Mulher 🚺", "Homem 🚹"])

    fralda_t, formato_t, valor_t = None, "-", 0.0
    if sexo_titular != "Selecione...":
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

    st.markdown("<div class='secao-titulo'>2. Mimo Extra para o Bernardo</div>", unsafe_allow_html=True)
    st.info("Além das fraldinhas, preparamos uma vitrine com algumas sugestões de coisinhas que o Bernardo vai precisar.")
    quer_mimo = st.radio("**Deseja adicionar um mimo extra ao seu presente?**", ["Não, vou presentear apenas com as fraldas.", "Sim, quero escolher um mimo!"], index=0)

    mimo_escolhido = None
    formato_mimo = "-"
    valor_mimo = 0.0

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
                            <a class="preco-btn btn-buscape" href="{item['link_buscape']}" target="_blank">🔍 Buscapé</a>
                            <a class="preco-btn btn-google"  href="{item['link_google']}"  target="_blank">🛒 Google</a>
                            <a class="preco-btn btn-ml"      href="{item['link_mercadolivre']}" target="_blank">🛍 Mercado Livre</a>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)

        st.markdown("---")
        nomes_mimos = [m["nome"] for m in CATALOGO_MIMOS]
        mimo_selecionado = st.selectbox("**Qual mimo você escolheu da vitrine acima?**", ["Selecione um mimo..."] + nomes_mimos)
        if mimo_selecionado != "Selecione um mimo...":
            info_mimo = next(m for m in CATALOGO_MIMOS if m["nome"] == mimo_selecionado)
            st.success(f"Ótima escolha! **{info_mimo['nome']}** - R$ {info_mimo['valor']:.2f}")
            st.markdown(
                f"""🔎 **Compare preços antes de comprar:**  
&nbsp;&nbsp;[🔴 Buscapé]({info_mimo['link_buscape']})&nbsp;&nbsp;|&nbsp;&nbsp;
[🔵 Google Shopping]({info_mimo['link_google']})&nbsp;&nbsp;|&nbsp;&nbsp;
[🟡 Mercado Livre]({info_mimo['link_mercadolivre']})""",
                unsafe_allow_html=False
            )
            fisicos_comprados = checar_fisicos_comprados(info_mimo["id"])
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

    st.markdown("<div class='secao-titulo'>3. Finalizar Confirmação</div>", unsafe_allow_html=True)
    if st.button("Confirmar Tudo e Gerar Resumo 🚀"):
        if not nome_titular or sexo_titular == "Selecione...":
            st.error("Por favor, preencha o seu nome e sexo no topo da página.")
        elif quer_mimo == "Sim, quero escolher um mimo!" and not mimo_escolhido:
            st.error("Você marcou que deseja dar um mimo. Por favor, selecione-o na lista acima.")
        else:
            dados_rsvp = {
                "Nome Titular": nome_titular.strip(), "Sexo Titular": sexo_titular, "Fralda Titular": fralda_t,
                "Formato Titular": formato_t, "Valor PIX Titular": valor_t, "Leva Acompanhante": leva_acompanhante,
                "Nome Acompanhante": nome_acomp.strip() if leva_acompanhante == "Sim" else "-",
                "Sexo Acompanhante": sexo_acomp if leva_acompanhante == "Sim" else "-",
                "Fralda Acompanhante": fralda_a if leva_acompanhante == "Sim" else "-",
                "Formato Acompanhante": formato_a if leva_acompanhante == "Sim" else "-",
                "Valor PIX Acompanhante": valor_a if leva_acompanhante == "Sim" else 0.0,
                "Qtd Filhos": int(qtd_filhos), "Mensagem": mensagem
            }
            salvar_confirmacao_rsvp(dados_rsvp)
            if mimo_escolhido:
                salvar_mimo(nome_titular, mimo_escolhido["id"], mimo_escolhido["nome"], formato_mimo, valor_mimo)

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

if __name__ == "__main__":
    main()