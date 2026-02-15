import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# CONEXÃO COM GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# ESTILIZAÇÃO CSS (Removi a parte da .badge-norma)
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-size: 0.82rem !important;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .main .stMarkdown p, .main h1, .main h2, .main h3, .main .stWidgetLabel {
        color: #000000 !important;
    }
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { 
        background-color: #EB5E28; 
        border-radius: 0 20px 20px 0; 
    }
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stWidgetLabel { 
        color: #FFFFFF !important;
        font-size: 0.82rem !important;
    }
    [data-testid="stSidebar"] hr { border: 0.5px solid #ff9e7d; margin: 10px 0; }
    .card-lei, .card-portaria { 
        padding: 15px; border-radius: 10px; margin-bottom: 8px; font-size: 0.82rem; color: #000000 !important;
    }
    .card-lei { background-color: #FFF5EE; border-left: 5px solid #FFB347; }
    .card-portaria { background-color: #FFFFF0; border-left: 5px solid #FFD700; }
    .res-box-clean { 
        background-color: #FFFFFF; padding: 10px; border-radius: 15px; border: 2px solid #EB5E28; 
        text-align: center; max-width: 280px; margin: 15px auto; 
    }
    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL
with st.sidebar:
    st.markdown("### 🏛️ Sobre o PTT")
    st.markdown("""
        <div style="color: white; text-align: justify; font-size: 0.82rem; margin-bottom: 10px;">
            Este produto técnico-tecnológico é resultante da dissertação de mestrado intitulada 
            <b>"A POLÍTICA DE SAÚDE MENTAL DA UNIVERSIDADE FEDERAL DE PERNAMBUCO: Entre a Normativa e a Realidade Laboral à Luz da Psicodinâmica do Trabalho"</b>, 
            do Mestrado Profissional em Gestão Pública para o Desenvolvimento Do Nordeste - CCSA da UFPE.
            <br><br>
            Ele funciona como uma calculadora para mensurar a aderência institucional às normativas federais de saúde mental no trabalho: 
            <b>Lei Nº 14.831/2024</b> (Certificado Empresa Promotora da Saúde Mental) e à 
            <b>Portaria SRH/MP Nº 1.261/2010</b> (Princípios, Diretrizes e Ações em Saúde Mental para os órgãos e entidades do Sistema de Pessoal Civil - SIPEC da Administração Pública Federal).
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📝 Instruções")
    st.markdown("""
        <div style="color: white; font-size: 0.82rem;">
            1. Clique na caixa de seleção para os itens que forem atendidos pela instituição.<br><br>
            2. Descreva a <b>Evidência</b>, caso o indicador seja atendido. Caso não seja, escreva o <b>Plano de Ação</b>.<br><br>
            3. Depois do preenchimento, clique em gerar Relatório para obter o resumo.<br><br>
            4. Quanto mais próximo o indicador estiver de <b>1,00</b>, mais próximo do total atendimento da normativa.
        </div>
        <div style
