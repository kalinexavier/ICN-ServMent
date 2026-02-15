import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# ESTILIZAÇÃO CSS
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-size: 0.85rem !important;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { 
        background-color: #EB5E28; 
        border-radius: 0 25px 25px 0; 
        margin: 10px 0; 
    }
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] h1, h2, h3,
    [data-testid="stSidebar"] .stWidgetLabel { 
        color: white !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stSidebar"] hr { border: 0.5px solid #ff9e7d; }
    .card-lei { background-color: #FFF5EE; padding: 10px; border-radius: 12px; border-left: 5px solid #FFB347; margin-bottom: 10px; font-size: 0.85rem; }
    .card-portaria { background-color: #FFFFF0; padding: 10px; border-radius: 12px; border-left: 5px solid #FFD700; margin-bottom: 10px; font-size: 0.85rem; }
    .badge-norma { color: #555; font-size: 0.65rem; font-weight: bold; text-transform: uppercase; display: inline-block; margin-bottom: 3px; }
    h1 { color: #252422; font-weight: 800; text-align: center; font-size: 1.8rem !important; }
    h2 { font-size: 1.4rem !important; color: #252422; }
    .res-box-clean { 
        background-color: #FFFFFF; 
        padding: 15px; 
        border-radius: 20px; 
        border: 2px solid #EB5E28; 
        text-align: center; 
        max-width: 300px; 
        margin: 20px auto; 
    }
    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 8px !important; font-size: 0.85rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL
with st.sidebar:
    st.markdown("### 🏛️ Sobre o PTT")
    st.info("""
        Este produto técnico-tecnológico é resultante da dissertação de mestrado intitulada 
        "A POLÍTICA DE SAÚDE MENTAL DA UNIVERSIDADE FEDERAL DE PERNAMBUCO: Entre a Normativa e a Realidade Laboral à Luz da Psicodinâmica do Trabalho", 
        do Mestrado Profissional em Gestão Pública da UFPE.
        
        Ele funciona como uma calculadora para mensurar a aderência institucional às normativas federais de saúde mental no trabalho: 
        **Lei Nº 14.831/2024** (Certificado Empresa Promotora da Saúde Mental) e 
        **Portaria SRH/MP Nº 1.261/2010** (Princípios, Diretrizes e Ações em Saúde Mental para os órgãos e entidades do SIPEC).
    """)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📝 Instruções")
    st.write("1. Marque os itens atendidos.")
    st.write("2. Descreva a Evidência ou o Plano de Ação.")
    st.write("3. Clique em Gerar Relatório para exportar.")
    st.markdown("""
        <div style="background-color: white; border: 1px solid white; padding: 12px; border-radius: 10px; text-align: left; margin-top: 10px;">
            <span style="color: #EB5E28 !important; font-weight: bold; font-size: 0.75rem; line-height: 1.3;">
                ⚠️ O instrumento serve como termômetro para a instituição, mas não deve ser utilizado para simples atendimento métrico. A saúde mental é um tema sério e deve ser tratado com responsabilidade.
            </span>
        </div>
    """, unsafe_allow_html=True)

# 3. IDENTIFICAÇÃO
st.title("Índice de Conformidade às Normativas Federais de Saúde Mental")
c_id1, c_id2 = st.columns(2)
with c_id1:
    nome_inst = st.text_input("🏢 Nome da Instituição/Unidade:", placeholder="Ex: UFPE - Progepe")
with c_id2:
    contato_resp = st.text_input("📧 Contato do Responsável:", placeholder="Ex: gestor@ufpe.br")

# 4. INDICADORES (Simplificados para o código - mantenha as frases originais no seu arquivo)
lei_grupos = {
    "Grupo I - Promoção da saúde mental": ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"],
    "Grupo II - Bem-estar dos trabalhadores": ["L9", "L10", "L11", "L12", "L13", "L14"],
    "Grupo III - Transparência e prestação de contas": ["L15", "L16", "L17"]
}

respostas_excel = []
def render_item(tag, texto, norma, classe):
    with st.container():
        st.markdown(f"<div class='{classe}'><span class='badge-norma'>{norma}</span>", unsafe_allow_html=True)
        check = st.checkbox(f"**{tag}**", key=f"cb_{tag}")
        det = st.text_input("Evidência / Plano de Ação:", key=f"t_{tag}")
        respostas_excel.append({"ID": tag, "Conformidade": "Sim" if check else "Não", "Detalhes": det})
        return 1 if check else 0

col_l, col_p = st.columns(2)
with col_l:
    st.subheader("🏛️ Lei 14.831/2024")
    idx = 1
    scores_l = []
    for g, itens in lei_grupos.items():
        st.markdown(f"**{g}**")
        s = sum([render_item(f"L{idx+i}", f"Indicador {idx+i}", "Lei 14.831", "card-lei") for i, _ in enumerate(itens)])
        scores_l.append(s / len(itens))
        idx += len(itens)
    icl = sum(scores_l) / 3

with col_p:
    st.subheader("📋 Portaria 1.261/2010")
    icp = sum([render_item(f"P{i+18}", f"Indicador P{i+18}", "Portaria 1.261", "card-portaria") for i in range(18)]) / 18

# 5. RESULTADOS E GRÁFICOS
st.write("---")
icn = (icl + icp) / 2
g1, g2, g3 = st.columns(3)

with g1:
    fig1 = go.Figure(go.Bar(x=['G-I', 'G-II', 'G-III', 'ICL'], y=scores_l + [icl], marker_color='#FFB347', text=[f"{v:.2f}" for v in scores_l + [icl]], textposition='auto'))
    fig1.update_layout(title={'text': "Conformidade à Lei 14.831", 'x':0.5, 'xanchor': 'center'}, yaxis=dict(range=[0, 1.1]), height=300)
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    fig2 = go.Figure(go.Bar(x=['Média ICP'], y=[icp], marker_color='#FFD700', text=[f"{icp:.2f}"], textposition='auto'))
    fig2.update_layout(title={'text': "Conformidade à Portaria 1.261", 'x':0.5, 'xanchor': 'center'}, yaxis=dict(range=[0, 1.1]), height=300)
    st.plotly_chart(fig2, use_container_width=True)

with g3:
    fig3 = go.Figure(go.Bar(x=['Geral (ICN)'], y=[icn], marker_color='#EB5E28', text=[f"{icn:.2f}"], textposition='auto'))
    fig3.update_layout(title={'text': "Conformidade Geral (ICN)", 'x':0.5, 'xanchor': 'center'}, yaxis=dict(range=[0, 1.1]), height=300)
    st.plotly_chart(fig3, use_container_width=True)

# CAIXA DE DESTAQUE DO ICN (Retornada conforme solicitado)
st.markdown(f"""
    <div class='res-box-clean'>
        <p style='color: #444; font-weight: bold; margin-bottom: 5px; font-size: 0.9rem;'>Índice Geral de Conformidade</p>
        <h1 style='font-size: 3rem !important; color: #EB5E28; margin:0;'>{icn:.2f}</h1>
        <p style='font-size: 0.75rem; color: #666;'>Média consolidada das normativas</p>
    </div>
""", unsafe_allow_html=True)

# 6. EXPORTAÇÃO
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    pd.DataFrame(respostas_excel).to_excel(writer, index=False)

st.download_button("📥 Gerar Relatório Profissional (Excel)", data=output.getvalue(), file_name=f"ICN_{nome_inst}.xlsx", type="primary", use_container_width=True)

# 7. RODAPÉ
st.markdown(f"""
    <div style='text-align: center; color: #444; font-size: 0.75rem; margin-top:30px;'>
        <p><b>Sistema idealizado por Kaline Xavier sob Orientação do docente Denilson Bezerra Marques.</b><br>
        Mestrado Profissional em Gestão Pública | UFPE</p>
    </div>
""", unsafe_allow_html=True)
