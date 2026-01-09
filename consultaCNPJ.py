import streamlit as st
import pandas as pd

# --- Configuração inicial ---
st.set_page_config(page_title="Consulta de CNPJ", layout="centered")

# --- Função para carregar a planilha ---
URL_CSV = "https://github.com/Augusto05/consulta-cnpj/raw/refs/heads/main/01-Santander_LeadsE1_2025_08-01.csv"

@st.cache_data
def carregar_dados(url):
    return pd.read_csv(url, sep=";", dtype=str, encoding="ISO-8859-1", on_bad_lines="skip")

# --- Carregar dados (substitua pelo nome do arquivo atualizado diariamente) ---
dados = carregar_dados(URL_CSV)  # ou "clientes.csv"

# --- Entrada do usuário ---
st.title("🔎 Sistema de Consulta de CNPJ")
cnpj = st.text_input("Digite o CNPJ do cliente:")

# --- Inicializar histórico de consultas ---
if "historico" not in st.session_state:
    st.session_state["historico"] = []

# --- Pesquisa ---
if st.button("Consultar"):
    if cnpj:
        resultado = dados[dados["CNPJ"] == cnpj]
        if not resultado.empty:
            st.success("Cliente encontrado!")
            for _, row in resultado.iterrows(): 
                st.markdown(f"""
                **CNPJ:** {row['CNPJ']}  
                **Razão Social:** {row['RAZAO SOCIAL']}  
                **Sócio:** {row['SOCIO']}  
                **CPF:** {row['CPF']}  
                **Data de Abertura:** {row['Data Abertura']}  
                **E-mail:** {row['E-mail']}  
                **Telefone:** {row['TELEFONE 1']}  
                """)

            # Adicionar ao histórico
            if cnpj not in st.session_state["historico"]:
                st.session_state["historico"].append(cnpj)
        else:
            st.error("CNPJ não encontrado na base de dados.")
    else:
        st.warning("Digite um CNPJ válido.")

# --- Exibir histórico ---
st.subheader("📌 Últimas consultas")
if st.session_state["historico"]:
    for c in st.session_state["historico"]:
        st.write(f"- {c}")
else:
    st.write("Nenhuma consulta realizada ainda.")
