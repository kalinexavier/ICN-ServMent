import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# ESTILIZAÇÃO CSS
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
    .res-box-clean { background-color: #FFFFFF; padding: 20px; border-radius: 20px; border: 2px solid #EB5E28; text-align: center; }
    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL
with st.sidebar:
    st.markdown("### 🏛️ Sobre o PTT")
    st.info('Este produto técnico-tecnológico é resultante da dissertação de mestrado intitulada "A POLÍTICA DE SAÚDE MENTAL DA UNIVERSIDADE FEDERAL DE PERNAMBUCO: Entre a Normativa e a Realidade Laboral à Luz da Psicodinâmica do Trabalho", do Mestrado Profissional em Gestão Pública da UFPE.')
    st.write("Ele funciona como uma calculadora para mensurar a aderência institucional às normativas federais de saúde mental no trabalho: **Lei Nº 14.831/2024** (Certificado Empresa Promotora da Saúde Mental) e à **Portaria SRH/MP Nº 1.261/2010** (Princípios, Diretrizes e Ações em Saúde Mental para os órgãos e entidades do Sistema de Pessoal Civil - SIPEC da Administração Pública Federal).")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📝 Instruções")
    st.write("1. Clique na caixa de seleção para os itens atendidos.")
    st.write("2. Descreva a **Evidência** (se atendido) ou o **Plano de Ação** (se não atendido).")
    st.write("3. Clique em **Gerar Relatório** ao finalizar.")
    st.write("4. O índice varia de 0 a 1,00.")
    
    # Alerta customizado solicitado
    st.markdown("""
        <div style="background-color: #FFFFFF; border: 2px solid #EB5E28; padding: 15px; border-radius: 10px;">
            <p style="color: #EB5E28; font-weight: bold; margin: 0; font-size: 0.85rem;">
                ⚠️ O instrumento serve como termômetro para a instituição, mas não deve ser utilizado para simples atendimento métrico. A saúde mental é um tema sério e deve ser tratado com responsabilidade.
            </p>
        </div>
    """, unsafe_allow_html=True)

# 3. IDENTIFICAÇÃO E TÍTULO
st.title("Índice de Conformidade às Normativas Federais de Saúde Mental")

c_id1, c_id2 = st.columns(2)
with c_id1:
    nome_inst = st.text_input("🏢 Nome da Instituição/Unidade:", placeholder="Ex: UFPE - Progepe")
with c_id2:
    contato_resp = st.text_input("📧 Contato do Responsável:", placeholder="Ex: gestor@ufpe.br")

st.write("---")

# 4. DADOS DOS INDICADORES
lei_grupos = {
    "Grupo I - Promoção da saúde mental": [
        "L1: implementação de programas de promoção da saúde mental no ambiente de trabalho;",
        "L2: oferta de acesso a recursos de apoio psicológico e psiquiátrico para seus trabalhadores;",
        "L3: promoção da conscientização sobre a importância da saúde mental por meio da realização de campanhas e de treinamentos;",
        "L4: promoção da conscientização direcionada à saúde mental da mulher;",
        "L5: capacitação de lideranças;",
        "L6: realização de treinamentos específicos que abordem temas de saúde mental de maior interesse dos trabalhadores;",
        "L7: combate à discriminação e ao assédio em todas as suas formas;",
        "L8: avaliação e acompanhamento regular das ações implementadas e seus ajustes;"
    ],
    "Grupo II - Bem-estar dos trabalhadores": [
        "L9: promoção de ambiente de trabalho seguro e saudável;",
        "L10: incentivo ao equilíbrio entre a vida pessoal e a profissional;",
        "L11: incentivo à prática de atividades físicas e de lazer;",
        "L12: incentivo à alimentação saudável;",
        "L13: incentivo à interação saudável no ambiente de trabalho;",
        "L14: incentivo à comunicação integrativa;"
    ],
    "Grupo III - Transparência e prestação de contas": [
        "L15: divulgação regular das ações e das políticas relacionadas à promoção da saúde mental e do bem-estar...",
        "L16: manutenção de canal para recebimento de sugestões e de avaliações;",
        "L17: promoção do desenvolvimento de metas e análises periódicas dos resultados relacionados à implementação..."
    ]
}

port_txt = [
    "P18: promover ações que mantenham e fortaleçam vínculos entre os servidores em sofrimento psíquico...",
    "P19: realizar programas e ações fundamentados em informações epidemiológicas...",
    "P20: realizar as ações de promoção inclusivas com respeito à pluralidade cultural...",
    "P21: promover a concepção ampliada de saúde mental...",
    "P22: planejar e direcionar as ações de promoção ao desenvolvimento humano...",
    "P23: ampliar a divulgação e integração dos serviços de saúde mental da rede pública...",
    "P24: detectar precocemente, acolher e monitorar o tratamento da pessoa com sofrimento psíquico",
    "P25: realizar ações com o objetivo de combater o estigma das pessoas com transtornos mentais...",
    "P26: estabelecer e registrar nexo causal entre os processos de trabalho e transtornos mentais...",
    "P27: identificar fatores de adoecimento e propor medidas de intervenção...",
    "P28: intervir em situações de conflito buscando soluções dialogadas...",
    "P29: oferecer suporte ao desenvolvimento das competências e habilidades do servidor...",
    "P30: disponibilizar espaços terapêuticos integrados à Política de Atenção...",
    "P31: garantir a realização das atividades de promoção à saúde no horário de trabalho",
    "P32: incentivar a implantação de Programas de Preparação à Aposentadoria - PPA",
    "P33: identificar situações de trabalho penosas do ponto de vista da saúde mental",
    "P34: privilegiar programas de promoção da qualidade de vida como fator de proteção",
    "P35: capacitar os gestores para identificar sofrimento psíquico no trabalho."
]

respostas_excel = []

def render_item(tag, texto, norma, classe):
    with st.container():
        st.markdown(f"<div class='{classe}'><span class='badge-norma'>{norma}</span>", unsafe_allow_html=True)
        check = st.checkbox(f"**{tag}**: {texto}", key=f"cb_{tag}")
        det = st.text_input("Evidência / Plano de Ação:", key=f"t_{tag}")
        respostas_excel.append({"ID": tag, "Indicador": texto, "Conformidade": "Sim" if check else "Não", "Evidência/Plano": det})
        return 1 if check else 0

# 5. INTERFACE DE COLETA
col_lei, col_port = st.columns(2)

with col_lei:
    st.header("🏛️ Lei 14.831/2024")
    scores_lei = {}
    idx_l = 1
    for grupo, indicadores in lei_grupos.items():
        st.subheader(f"🔹 {grupo}")
        soma_g = 0
        for txt in indicadores:
            soma_g += render_item(f"L{idx_l}", txt, "Lei 14.831", "card-lei")
            idx_l += 1
        scores_lei[grupo] = soma_g / len(indicadores)
    icl = sum(scores_lei.values()) / 3

with col_port:
    st.header("📋 Portaria 1.261/2010")
    icp = sum([render_item(f"P{i+18}", txt, "Portaria 1.261", "card-portaria") for i, txt in enumerate(port_txt)]) / 18

# 6. GRÁFICOS E RESULTADOS
st.write("---")
icn = (icl + icp) / 2
g1, g2, g3 = st.columns(3)

with g1:
    fig_l = go.Figure(go.Bar(x=['G-I', 'G-II', 'G-III', 'Total ICL'], y=list(scores_lei.values()) + [icl], marker_color='#FFB347', text=[f"{v:.2f}" for v in list(scores_lei.values()) + [icl]], textposition='auto'))
    fig_l.update_layout(title="Performance Lei 14.831", yaxis=dict(range=[0, 1.1]), height=300)
    st.plotly_chart(fig_l, use_container_width=True)

with g2:
    fig_p = go.Figure(go.Bar(x=['Média ICP'], y=[icp], marker_color='#FFD700', text=[f"{icp:.2f}"], textposition='auto'))
    fig_p.update_layout(title="Performance Portaria 1.261", yaxis=dict(range=[0, 1.1]), height=300)
    st.plotly_chart(fig_p, use_container_width=True)

with g3:
    fig_n = go.Figure(go.Bar(x=['Índice Geral (ICN)'], y=[icn], marker_color='#EB5E28', text=[f"{icn:.2f}"], textposition='auto'))
    fig_n.update_layout(title="Consolidado (ICN)", yaxis=dict(range=[0, 1.1]), height=300)
    st.plotly_chart(fig_n, use_container_width=True)

# 7. EXPORTAÇÃO EXCEL
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    workbook = writer.book
    worksheet_res = workbook.add_worksheet('Resumo e Identificação')
    header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#EB5E28', 'border': 1})
    
    worksheet_res.write(0, 0, 'IDENTIFICAÇÃO DA UNIDADE', header_fmt)
    worksheet_res.write(1, 0, f"Instituição: {nome_inst if nome_inst else 'Não informada'}")
    worksheet_res.write(2, 0, f"Responsável: {contato_resp if contato_resp else 'Não informado'}")
    worksheet_res.write(4, 0, 'RESULTADOS DOS ÍNDICES', header_fmt)
    worksheet_res.write(5, 0, f"ICL: {icl:.2f} | ICP: {icp:.2f} | ICN: {icn:.2f}")
    worksheet_res.set_column('A:A', 60)

    pd.DataFrame(respostas_excel).to_excel(writer, sheet_name='Diagnóstico Detalhado', index=False)

nome_arq = f"ICN_{nome_inst.replace(' ', '_')}.xlsx" if nome_inst else "ICN_Saude_Mental.xlsx"

st.download_button("📥 Gerar Relatório Profissional (Excel)", data=output.getvalue(), file_name=nome_arq, mime="application/vnd.ms-excel", type="primary", use_container_width=True)

# 8. RODAPÉ
st.markdown(f"""
    <div style='text-align: center; color: #444; font-size: 0.85rem; margin-top:40px;'>
        <p><b>Sistema idealizado por Kaline Xavier sob Orientação do docente Denilson Bezerra Marques.</b><br>
        Contatos: kaline.xavier@ufpe.br | denilson.marques@ufpe.br | gp.pdt@ufpe.br</p>
        <p>Gestão Pública, Prazer e Sofrimento no Trabalho <b>(@gp.pdt.ufpe)</b><br>
        Mestrado Profissional em Gestão Pública | UFPE</p>
    </div>
""", unsafe_allow_html=True)
