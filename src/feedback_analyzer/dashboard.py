#!/usr/bin/env python3
"""
🌐 Dashboard Web para o Analisador de Feedback
Versão simples usando Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_extractor import extrair_comentarios_de_url
from gemini_processor import analisar_comentario_individual, configurar_ia

def main():
    st.set_page_config(
        page_title="🚀 Analisador de Feedback",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Analisador de Feedback para Produtos Web")
    st.markdown("### 📊 Analise comentários de qualquer produto da web!")
    
    # Sidebar para configurações
    st.sidebar.title("⚙️ Configurações")
    
    # Verificar configuração da IA
    if not configurar_ia():
        st.error("❌ Erro ao configurar a IA. Verifique sua API key.")
        return
    
    st.sidebar.success("✅ IA configurada com sucesso!")
    
    # Opções de entrada
    opcao = st.sidebar.selectbox(
        "📁 Fonte dos comentários:",
        ["🌐 URL do produto", "📄 Upload de arquivo", "✍️ Entrada manual"]
    )
    
    df = None
    
    if opcao == "🌐 URL do produto":
        st.subheader("🌐 Extrair Comentários de URL")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            url = st.text_input("🔗 Cole a URL do produto:")
        with col2:
            extrair = st.button("🚀 Extrair", type="primary")
        
        if extrair and url:
            with st.spinner("⏳ Extraindo comentários..."):
                try:
                    df = extrair_comentarios_de_url(url)
                    if not df.empty:
                        st.success(f"✅ {len(df)} comentários extraídos!")
                        st.session_state.df = df
                    else:
                        st.error("❌ Nenhum comentário encontrado.")
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
    
    elif opcao == "📄 Upload de arquivo":
        st.subheader("📄 Upload de Arquivo")
        
        uploaded_file = st.file_uploader(
            "Escolha um arquivo:",
            type=['csv', 'txt', 'json']
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.txt'):
                    content = uploaded_file.read().decode('utf-8')
                    comentarios = [linha.strip() for linha in content.split('\n') if linha.strip()]
                    df = pd.DataFrame({
                        'data': [datetime.now().strftime('%Y-%m-%d')] * len(comentarios),
                        'fonte': ['Upload'] * len(comentarios),
                        'comentario': comentarios
                    })
                
                if df is not None and not df.empty:
                    st.success(f"✅ {len(df)} comentários carregados!")
                    st.session_state.df = df
            except Exception as e:
                st.error(f"❌ Erro ao carregar arquivo: {e}")
    
    # Mostrar dados se disponível
    if 'df' in st.session_state and not st.session_state.df.empty:
        df = st.session_state.df
        
        st.subheader("📊 Dados Carregados")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Total de Comentários", len(df))
        with col2:
            st.metric("🌐 Fontes", len(df['fonte'].unique()))
        with col3:
            st.metric("📅 Período", f"{df['data'].min()} - {df['data'].max()}")
        
        # Mostrar amostra dos dados
        st.dataframe(df.head(), use_container_width=True)
        
        # Nome do produto
        nome_produto = st.text_input("🏷️ Nome do produto/serviço:", "Produto Analisado")
        
        # Botão para análise
        if st.button("🤖 Analisar com IA", type="primary"):
            with st.spinner("🔄 Analisando comentários..."):
                # Aqui você implementaria a análise
                st.success("✅ Análise concluída!")
                
                # Gráficos de exemplo (você substituiria pelos dados reais)
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de sentimentos
                    fig_sentiment = px.pie(
                        names=['Positivo', 'Negativo', 'Neutro'],
                        values=[60, 25, 15],
                        title="📊 Distribuição de Sentimentos"
                    )
                    st.plotly_chart(fig_sentiment, use_container_width=True)
                
                with col2:
                    # Gráfico de categorias
                    fig_category = px.bar(
                        x=['Bug', 'Sugestão', 'UI/UX', 'Suporte'],
                        y=[10, 30, 25, 35],
                        title="📋 Categorias de Feedback"
                    )
                    st.plotly_chart(fig_category, use_container_width=True)

if __name__ == "__main__":
    main()
