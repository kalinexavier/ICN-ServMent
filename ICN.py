import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# ESTILIZAÇÃO CSS (Orange & Clean - Padrão UFPE/CCSA)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #EB5E28; border-radius: 0 25px 25px 0; margin: 10px 0; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] hr { border: 0.5px solid #ff9e7d; }
    .card-lei { background-color: #FFF5EE; padding: 15px; border-radius: 12px; border-left: 6px solid #FFB347; margin-bottom: 12px; }
    .card-portaria { background-color: #FFFFF0; padding: 15px; border-radius: 12px; border-left: 6px solid #FFD700; margin-bottom: 12px; }
    .badge-norma { color: #555; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; display: inline-block; margin-bottom: 5px; }
    h1 { color: #252422; font-weight: 800; text-align: center; }
    .res-box-clean { background-color: #FFFFFF; padding: 25px; border-radius: 20px; border: 2px solid #F0F0F0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (TEXTOS ATUALIZADOS)
with st.sidebar:
    st.markdown("### 🏛️ Sobre o PTT")
    st.info("""Este produto técnico-tecnológico é resultante da dissertação de mestrado intitulada "A POLÍTICA DE SAÚDE MENTAL DA UNIVERSIDADE FEDERAL DE PERNAMBUCO: Entre a Normativa e a Realidade Laboral à Luz da Psicodinâmica do Trabalho", do Mestrado Profissional em Gestão Pública da UFPE.""")
    st.write("Ele funciona como uma calculadora para mensurar a aderência institucional às normativas federais de saúde mental no trabalho: Lei Nº 14.831/2024 e Portaria SRH/MP Nº 1.261/2010.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📝 Instruções")
    st.write("1. Clique na caixa de seleção para os itens que forem atendidos pela instituição.")
    st.write("2. Descreva a **Evidência**, caso o indicador seja atendido. Caso não seja, escreva o **Plano de Ação**.")
    st.write("3. Depois do preenchimento, clique em gerar Relatório para obter o resumo.")
    st.write("4. Quanto mais próximo o indicador estiver de **1,00**, mais próximo do total atendimento da normativa.")
    st.warning("⚠️ O instrumento serve como termômetro para a instituição, mas não deve ser utilizado para simples atendimento métrico. A saúde mental é um tema sério e deve ser tratado com responsabilidade.")

st.title("Índice de Conformidade às Normativas Federais de Saúde Mental")

# 3. DADOS DOS INDICADORES (FRASES COMPLETAS E GRUPOS)
lei_grupos = {
    "Grupo I - Promoção da saúde mental": [
        "implementação de programas de promoção da saúde mental no ambiente de trabalho;",
        "oferta de acesso a recursos de apoio psicológico e psiquiátrico para seus trabalhadores;",
        "promoção da conscientização sobre a importância da saúde mental por meio da realização de campanhas e de treinamentos;",
        "promoção da conscientização direcionada à saúde mental da mulher;",
        "capacitação de lideranças;",
        "realização de treinamentos específicos que abordem temas de saúde mental de maior interesse dos trabalhadores;",
        "combate à discriminação e ao assédio em todas as suas formas;",
        "avaliação e acompanhamento regular das ações implementadas e seus ajustes;"
    ],
    "Grupo II - Bem-estar dos trabalhadores": [
        "promoção de ambiente de trabalho seguro e saudável;",
        "incentivo ao equilíbrio entre a vida pessoal e a profissional;",
        "incentivo à prática de atividades físicas e de lazer;",
        "incentivo à alimentação saudável;",
        "incentivo à interação saudável no ambiente de trabalho;",
        "incentivo à comunicação integrativa;"
    ],
    "Grupo III - Transparência e prestação de contas": [
        "divulgação regular das ações e das políticas relacionadas à promoção da saúde mental e do bem-estar de seus trabalhadores nos meios de comunicação utilizados pela empresa;",
        "manutenção de canal para recebimento de sugestões e de avaliações;",
        "promoção do desenvolvimento de metas e análises periódicas dos resultados relacionados à implementação das ações de saúde mental."
    ]
}

portaria_lista = [
    "promover ações que mantenham e fortaleçam vínculos entre os servidores em sofrimento psíquico, seus familiares, seus representantes, na sua comunidade e no trabalho, tornando-os parceiros no planejamento do tratamento e na constituição de redes de apoio e integração social a todos os envolvidos",
    "realizar programas e ações fundamentados em informações epidemiológicas, considerando as especificidades e as vulnerabilidades do público-alvo",
    "realizar as ações de promoção inclusivas com respeito à pluralidade cultural e às diferenças de religião, gênero, orientação sexual, cor/raça/etnia, habilidade física ou intelectual, classe e idade/geração, buscando combater o estigma das pessoas com sofrimento psíquico",
    "promover a concepção ampliada de saúde mental, integrada à saúde física e ao bem-estar socioeconômico dos servidores",
    "planejar e direcionar as ações de promoção ao desenvolvimento humano, ao incentivo à educação para a vida saudável, com acesso aos bens culturais",
    "ampliar a divulgação e integração dos serviços de saúde mental da rede pública, dos órgãos da APF e da rede conveniada, assim como gerir em nível local a forma de procurá-los e utilizá-los",
    "detectar precocemente, acolher e monitorar o tratamento da pessoa com sofrimento psíquico",
    "realizar ações, em vários níveis de interlocução, com o objetivo de combater o estigma das pessoas com transtornos mentais, incluindo orientação aos demais trabalhadores da instituição sobre sofrimento psíquico e doenças mentais e o apoio à criação e ao fortalecimento de associações da rede social e familiar",
    "estabelecer e registrar nexo causal entre os processos de trabalho, o sofrimento psíquico e os transtornos mentais e comportamentais",
    "identificar nos locais de trabalho os fatores envolvidos no adoecimento mental, mapear os locais e os tipos de atividades e propor medidas de intervenção no ambiente e na organização do trabalho no intuito de valorizar o servidor e diminuir o sofrimento psíquico",
    "intervir nas situações de conflito vivenciadas no local de trabalho, buscando soluções dialogadas e ações mediadas pela equipe multiprofissional, constituindo comissões de ética onde não existirem, como instâncias de mediação no âmbito institucional",
    "oferecer suporte ao desenvolvimento das competências e habilidades do servidor, ao encontro das metas e objetivos a serem alcançados, auxiliando-o inclusive no desenvolvimento eficaz de seus projetos de vida",
    "disponibilizar espaços terapêuticos nos ambientes de trabalho quando as ações estiverem integradas à Política de Atenção à Saúde dos Servidores",
    "garantir a realização das atividades de promoção à saúde no horário de trabalho",
    "incentivar na Administração Pública Federal a implantação de Programas de Preparação à Aposentadoria - PPA",
    "identificar situações de trabalho penosas do ponto de vista da saúde mental, propondo as intervenções necessárias",
    "privilegiar programas de promoção da qualidade de vida, como meio de ampliar os fatores de proteção aos portadores de transtornos mentais e de diminuir a recorrência das crises",
    "capacitar os gestores para identificar sofrimento psíquico no trabalho."
]

respostas_excel = []

def render_item(tag, texto, norma, classe):
    with st.container():
        st.markdown(f"<div class='{classe}'><span class='badge-norma'>{norma}</span>", unsafe_allow_html=True)
        check = st.checkbox(f"**{tag}**: {texto}", key=f"cb_{tag}")
        det = st.text_input("Evidência / Plano de Ação:", key=f"t_{tag}")
        status = "Sim" if check else "Não"
        respostas_excel.append({"ID": tag, "Indicador": texto, "Conformidade": status, "Evidência/Plano de Ação": det})
        return 1 if check else 0

# 4. INTERFACE PRINCIPAL
col_lei, col_port = st.columns(2)

with col_lei:
    st.header("🏛️ Lei 14.831/2024")
    scores_lei = {}
    idx_l = 1
    for grupo, indicadores in lei_grupos.items():
        st.markdown(f"##### {grupo}")
        soma_g = 0
        for txt in indicadores:
            soma_g += render_item(f"L{idx_l}", txt, "Lei 14.831", "card-lei")
            idx_l += 1
        scores_lei[grupo] = soma_g / len(indicadores)
    icl = sum(scores_lei.values()) / 3

with col_port:
    st.header("📋 Portaria 1.261/2010")
    soma_p = 0
    for i, txt in enumerate(portaria_lista):
        soma_p += render_item(f"P{i+18}", txt, "Portaria 1.261", "card-portaria")
    icp = soma_p / 18

# 5. CÁLCULO E GRÁFICOS
icn = (icl + icp) / 2
st.write("---")
c_g1, c_g2, c_res = st.columns([1, 1, 1])

with c_g1:
    fig_l = go.Figure(go.Bar(
        x=['Grupo I', 'Grupo II', 'Grupo III', 'Média ICL'],
        y=[scores_lei["Grupo I - Promoção da saúde mental"], scores_lei["Grupo II - Bem-estar dos trabalhadores"], scores_lei["Grupo III - Transparência e prestação de contas"], icl],
        marker_color='#FFB347', text=[f"{v:.2f}" for v in list(scores_lei.values()) + [icl]], textposition='auto'
    ))
    fig_l.update_layout(title="Performance Lei 14.831", yaxis=dict(range=[0, 1.1]), height=350)
    st.plotly_chart(fig_l, use_container_width=True)

with c_g2:
    fig_p = go.Figure(go.Bar(x=['Média ICP'], y=[icp], marker_color='#FFF9A6', text=[f"{icp:.2f}"], textposition='auto'))
    fig_p.update_layout(title="Performance Portaria 1.261", yaxis=dict(range=[0, 1.1]), height=350)
    st.plotly_chart(fig_p, use_container_width=True)

with c_res:
    st.markdown(f"""
        <div class='res-box-clean'>
            <p style='color: #444; font-weight: bold;'>Índice de Conformidade Geral</p>
            <h1 style='font-size: 85px !important; color: #EB5E28; margin:0;'>{icn:.2f}</h1>
            <p style='font-size: 0.9rem; color: #666;'>Média ICL + ICP</p>
        </div>
    """, unsafe_allow_html=True)

# 6. EXPORTAÇÃO EXCEL
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df = pd.DataFrame(respostas_excel)
    df.to_excel(writer, index=False, sheet_name='Diagnóstico')
    # (O código de formatação Excel anterior pode ser mantido aqui para o download)

st.download_button("📥 Gerar Relatório Profissional (Excel)", data=output.getvalue(), file_name="ICN_Saude_Mental.xlsx", mime="application/vnd.ms-excel", type="primary", use_container_width=True)

# 7. RODAPÉ (CRÉDITOS ATUALIZADOS)
st.write("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #4
