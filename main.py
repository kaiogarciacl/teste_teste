import streamlit as st


st.set_page_config(page_title="PROMETHEUS",layout="wide", initial_sidebar_state="collapsed")

with open("style.css") as f:st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.image(fr'D:\img_prometheus\logo_prometeus.jpeg')
    log = st.text_input('LOG', label_visibility='collapsed', placeholder='Login', key='Log')
    senha = st.text_input('senha', label_visibility='collapsed', placeholder='Senha', key='senha', type='password')

    def limpa_log():
        st.session_state['Log'] = ''
        st.session_state['senha'] = ''

    if log != '' and senha != '':
       # st.toast('**⚠️ Atenção as 09:00 H o sistema Será Reiniciado Voltando as 09:15 H**')
        md.usuario = log
        rows = f""" if exists (select nome from login where nome = '{log}' and senha = '{senha}') BEGIN select 'CONSTA' END ELSE  select 'NÃO CONSTA' """
        cursor = cn.conexao_sql.cursor()
        cursor.execute(rows)
        rows = cursor.fetchall()
        for row in rows:
            verificador_log = row[0]
            if verificador_log == 'NÃO CONSTA':
                st.info(' **:red[Usuário ou Senha Errado]**')
            else:
                deslogar = st.button('Deslogar', use_container_width=True, on_click=limpa_log)
                md.usuario = log











