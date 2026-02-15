import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ICN - Kaline Xavier", layout="wide", page_icon="📊")

# CONEXÃO COM GOOGLE SHEETS (Posicionada corretamente no topo)
conn = st.connection("gsheets", type=GSheetsConnection)

# ESTILIZAÇÃO CSS (Suas cores e tamanhos de fonte preservados)
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
        padding: 10px; border-radius: 10px; margin-bottom: 8px; font-size: 0.82rem; color: #000000 !important;
    }
    .card-lei { background-color: #FFF5EE; border-left: 5px solid #FFB347; }
    .card-portaria { background-color: #FFFFF0; border-left: 5px solid #FFD700; }
    .badge-norma { color: #555; font-size: 0.65rem; font-weight: bold; text-transform: uppercase; display: inline-block; margin-bottom: 3px; }
    .res-box-clean { 
        background-color: #FFFFFF; padding: 10px; border-radius: 15px; border: 2px solid #EB5E28; 
        text-align: center; max-width: 280px; margin: 15px auto; 
    }
    button[kind="primary"] { background-color: #EB5E28 !important; border: none !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (Seus textos originais completos)
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
        <div style="background-color: white; padding: 10px; border-radius: 8px; text-align: left; margin-top: 15px;">
            <span style="color: #EB5E28 !important; font-weight: bold; font-size: 0.72rem; line-height: 1.2;">
                ⚠️ O instrumento serve como termômetro para a instituição, mas não deve ser utilizado para simples atendimento métrico. A saúde mental é um tema sério e deve ser tratado com responsabilidade.
            </span>
        </div>
    """, unsafe_allow_html=True)

# 3. PÁGINA PRINCIPAL
st.markdown("<h1>Índice de Conformidade às Normativas Federais de Saúde Mental</h1>", unsafe_allow_html=True)
c_id1, c_id2 = st.columns(2)
with c_id1:
    nome_inst = st.text_input("🏢 Nome da Instituição/Unidade:", placeholder="Ex: UFPE - Progepe")
with c_id2:
    contato_resp = st.text_input("📧 Contato do Responsável:", placeholder="Ex: gestor@ufpe.br")

st.write("---")

# 4. DICIONÁRIOS COMPLETOS
lei_grupos = {
    "Grupo I - Promoção da saúde mental": [
        "implementação de programas de promoção da saúde mental no ambiente de trabalho",
        "oferta de acesso a recursos de apoio psicológico e psiquiátrico para seus trabalhadores",
        "promoção da conscientização sobre a importância da saúde mental por meio da realização de campanhas e de treinamentos",
        "promoção da conscientização direcionada à saúde mental da mulher",
        "capacitação de lideranças",
        "realização de treinamentos específicos que abordem temas de saúde mental de maior interesse dos trabalhadores",
        "combate à discriminação e ao assédio em todas as suas formas",
        "avaliação e acompanhamento regular das ações implementadas e seus ajustes"
    ],
    "Grupo II - Bem-estar dos trabalhadores": [
        "promoção de ambiente de trabalho seguro e saudável",
        "incentivo ao equilíbrio entre a vida pessoal e a profissional",
        "incentivo à prática de atividades físicas e de lazer",
        "incentivo à alimentação saudável",
        "incentivo à interação saudável no ambiente de trabalho",
        "incentivo à comunicação integrativa"
    ],
    "Grupo III - Transparência e prestação de contas": [
        "divulgação regular das ações e das políticas relacionadas à promoção da saúde mental e do bem-estar de seus trabalhadores nos meios de comunicação utilizados pela empresa",
        "manutenção de canal para recebimento de sugestões e de avaliações",
        "promoção do desenvolvimento de metas e análises periódicas dos resultados relacionados à implementação das ações de saúde mental"
    ]
}

port_txt = [
    "promover ações que mantenham e fortaleçam vínculos entre os servidores em sofrimento psíquico, seus familiares, seus representantes, na sua comunidade e no trabalho, tornandoos parceiros no planejamento do tratamento e na constituição de redes de apoio e integração social a todos os envolvidos",
    "realizar programas e ações fundamentados em informações epidemiológicas, considerando as especificidades e as vulnerabilidades do público-alvo",
    "realizar as ações de promoção inclusivas com respeito à pluralidade cultural e às diferenças de religião, gênero, orientação sexual, cor/raça/etnia, habilidade física ou intelectual, classe e idade/geração, buscando combater o estigma das pessoas com sofrimento psíquico",
    "promover a concepção ampliada de saúde mental, integrada à saúde física e ao bem-estar socioeconômico dos servidores",
    "planejar e direcionar as ações de promoção ao desenvolvimento humano, ao incentivo à educação para a vida saudável, com acesso aos bens culturais",
    "ampliar a divulgação e integração dos serviços de saúde mental da rede pública, dos órgãos da APF e da rede conveniada, assim como gerir em nível local a forma de procurálos e utilizálos",
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
    "capacitar os gestores para identificar sofrimento psíquico no trabalho"
]

respostas_excel = []
def render_item(tag, texto, norma, classe):
    with st.container():
        st.markdown(f"<div class='{classe}'><span class='badge-norma'>{norma}</span>", unsafe_allow_html=True)
        check = st.checkbox(f"**{tag}**: {texto}", key=f"cb_{tag}")
        det = st.text_input("Evidência / Plano de Ação:", key=f"t_{tag}", placeholder="Detalhe aqui...")
        respostas_excel.append({"ID": tag, "Indicador": texto, "Conformidade": "Sim" if check else "Não", "Detalhes": det})
        return 1 if check else 0

col_l, col_p = st.columns(2)
with col_l:
    st.markdown("## 🏛️ Lei 14.831/2024")
    idx_l, scores_l = 1, []
    for g, itens in lei_grupos.items():
        st.markdown(f"### {g}")
        s = sum([render_item(f"L{idx_l+i}", txt, "Lei 14.831", "card-lei") for i, txt in enumerate(itens)])
        scores_l.append(s / len(itens))
        idx_l += len(itens)
    icl = sum(scores_l) / 3

with col_p:
    st.markdown("## 📋 Portaria 1.261/2010")
    icp = sum([render_item(f"P{i+18}", txt, "Portaria 1.261", "card-portaria") for i, txt in enumerate(port_txt)]) / 18

# 5. RESULTADOS E GRÁFICOS
st.write("---")
icn = (icl + icp) / 2
g1, g2, g3 = st.columns(3)
layout_c = {'x':0.5, 'xanchor': 'center', 'font': {'color': 'black'}}

with g1:
    f1 = go.Figure(go.Bar(x=['G-I', 'G-II', 'G-III', 'ICL'], y=scores_l + [icl], marker_color='#FFB347', text=[f"{v:.2f}" for v in scores_l + [icl]], textposition='auto'))
    f1.update_layout(title={'text': "Conformidade à Lei 14.831", **layout_c}, yaxis=dict(range=[0, 1.1]), height=280)
    st.plotly_chart(f1, use_container_width=True)

with g2:
    f2 = go.Figure(go.Bar(x=['Média ICP'], y=[icp], marker_color='#FFD700', text=[f"{icp:.2f}"], textposition='auto'))
    f2.update_layout(title={'text': "Conformidade à Portaria 1.261", **layout_c}, yaxis=dict(range=[0, 1.1]), height=280)
    st.plotly_chart(f2, use_container_width=True)

with g3:
    f3 = go.Figure(go.Bar(x=['Geral (ICN)'], y=[icn], marker_color='#EB5E28', text=[f"{icn:.2f}"], textposition='auto'))
    f3.update_layout(title={'text': "Conformidade Geral (ICN)", **layout_c}, yaxis=dict(range=[0, 1.1]), height=280)
    st.plotly_chart(f3, use_container_width=True)

st.markdown(f"<div class='res-box-clean'><p style='color: #000; font-weight: bold; margin-bottom: 2px; font-size: 0.85rem;'>Índice Geral de Conformidade</p><h1 style='font-size: 2.5rem !important; color: #EB5E28; margin:0;'>{icn:.2f}</h1></div>", unsafe_allow_html=True)

# 6. EXPORTAÇÃO E SALVAMENTO (SISTEMA ANTI-SOBREPOSIÇÃO)
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    pd.DataFrame(respostas_excel).to_excel(writer, index=False)

if st.download_button("📥 Gerar Relatório Profissional (Excel)", 
                      data=output.getvalue(), 
                      file_name=f"ICN_{nome_inst}.xlsx", 
                      type="primary", 
                      use_container_width=True):
    try:
        url_planilha = st.secrets["connections"]["gsheets"]["spreadsheet"]
        
        # 1. Preparamos o dado novo
        nova_linha = pd.DataFrame([{
            "Data": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
            "Instituicao": str(nome_inst),
            "Contato": str(contato_resp),
            "ICL": float(icl),
            "ICP": float(icp),
            "ICN": float(icn)
        }])
        
        # 2. LEMOS o que já está lá (MUITO IMPORTANTE)
        # O clear_cache garante que ele pegue os dados mais recentes, não uma cópia antiga
        existentes = conn.read(spreadsheet=url_planilha, worksheet="Página1", ttl=0)
        
        # 3. JUNTAMOS o passado com o presente
        if existentes is not None and not existentes.empty:
            # O concat "empilha" a nova_linha embaixo dos existentes
            df_final = pd.concat([existentes, nova_linha], ignore_index=True)
        else:
            df_final = nova_linha
            
        # 4. SALVAMOS o bloco inteiro atualizado
        conn.update(spreadsheet=url_planilha, worksheet="Página1", data=df_final)
        
        st.success("✅ Diagnóstico registrado com sucesso!")

    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# 7. RODAPÉ ORIGINAL RESTAURADO
st.write("<br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='text-align: center; color: #444; font-size: 0.82rem; line-height: 1.6;'>
        <p><b>Sistema idealizado por Kaline Mirele Silva Xavier sob Orientação do docente Denilson Bezerra Marques.</b><br>
        Contatos: kaline.xavier@ufpe.br | denilson.marques@ufpe.br | gp.pdt@ufpe.br</p>
        <p>Gestão Pública, Prazer e Sofrimento no Trabalho <b>(@gp.pdt.ufpe)</b><br>
        Mestrado Profissional em Gestão Pública | UFPE</p>
    </div>
""", unsafe_allow_html=True)





