import streamlit as st
import hydralit_components as hc
import a_programar
import abir_coleta_de_dado_qualidade
import abrir_pedido
import agrupamento_cotacao
import alterar_nest
import ambiente
import aprovacao_pedido_comercial
import baixar_nest
import cadastrar_fornecedor
import cartao_ponto
import configuracao_conta
import criar_estrutura
import fallow_up
import finalizar_conferencia
import finalizar_pedido
import itens_comprado
import lista_geral_compras_almoxarifado
import lista_programados_prog
import lista_sci
import models as md
import conexao as cn
import apontamento
import import_carteiras
import carteira_prog
import lista_agrupa_almoxarifado
import ponto_rh
import precificacao_compras
import relatorios
import solicitacao_compra
import testes

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


if log == '' or senha == '':
    apontamento.apontamento()

if log != '' and senha != '':
    if verificador_log == 'CONSTA':
        rows = f""" select * from login where nome = '{log}' """
        cursor = cn.conexao_sql.cursor()
        cursor.execute(rows)
        rows = cursor.fetchall()
        for row in rows:
            md.conexao_linha = 'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=PC-13; DATABASE=Base_cl; UID=sa; PWD='

            if row[1] == 'Adm_geral':
                menu_opcao = [
                    {'icon': 'bi bi-building', 'label': 'Comercial',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Abrir Orçamento'},
                                 {'icon': 'bi bi-inboxes-fill', 'label': 'Finalizar Orçamento'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Precificação'},
                                 {'icon': 'bi bi-bag-check', 'label': 'Aprovação'}]},

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Engenharia',
                     'submenu': [{'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Códigos'},
                                 {'icon': 'bi bi-list-ol', 'label': 'Análise Crítica'},
                                 {'icon': 'bi bi-clock-history', 'label': 'Tempos e Métodos'}]},

                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Subir Carteiras'},
                                 {'icon': 'bi bi-list-ol', 'label': "Carteira OP's"},
                                 {'icon': 'bi bi-list-ol', 'label': 'Carteira Programação'},
                                 {'icon': 'bi bi-folder-x', 'label': 'Alterar - Excluir OP'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': 'Alterar Plano Nest'},
                                 {'icon': 'bi bi-person-lines-fill', 'label': 'Follow Up'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': 'Solicitar Reposição'}]},

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Programação',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Lista de Programados'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': "OP's á Programar"},
                                 {'icon': 'bi bi-cloud-download', 'label': "Baixar Nesting"}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista Geral'},
                                 {'icon': 'bi bi-ui-checks', 'label': 'Conferência Almoxarifado'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Conferência'},
                                 {'icon': 'bi bi-bag-check', 'label': 'Confirmar Recebimento'},
                                 {'icon': 'bi bi-ui-checks', 'label': 'Agrupar para Cotação'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Movimentação de Cotação'},
                                 {'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Itens Comprados'},
                                 {'icon': 'bi bi-box-arrow-in-down', 'label': 'Cadastrar Item'},
                                 {'icon': 'bi bi-building', 'label': 'Cadastrar Fornecedor'}]},

                    {'icon': 'bi bi-file-diff', 'label': 'Qualidade',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de PPM'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir SCI'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar - Finalizar SCI'},
                                 {'icon': 'bi bi-list-task', 'label': 'Lista de Instrumentos'},
                                 {'icon': 'bi bi-file-earmark-ruled', 'label': 'Relatórios Qualidade'}]},

                    {'icon': 'bi bi-send-plus', 'label': 'Serviço Externo',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Romaneio'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir Trabalho Externo'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Romaneio'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Romaneio'}]},

                    {'icon': 'bi bi-truck', 'label': 'Expedição',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Romaneio'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir Romaneio'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Romaneio'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Romaneio'}]},

                    {'icon': 'bi bi-person-raised-hand', 'label': 'RH',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Colaboradores'},
                                 {'icon': 'bi bi-calendar2-week', 'label': 'Cartão Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Cadastrar Colaborador'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Cadastrar Usuario'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Teste'}]

            if row[1] == 'Adm':
                menu_opcao = [
                    {'icon': 'bi bi-building', 'label': 'Comercial',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Abrir Orçamento'},
                                 {'icon': 'bi bi-inboxes-fill', 'label': 'Finalizar Orçamento'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Precificação'},
                                 {'icon': 'bi bi-bag-check', 'label': 'Aprovação'}]},

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Engenharia',
                     'submenu': [{'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Códigos'},
                                 {'icon': 'bi bi-list-ol', 'label': 'Análise Crítica'},
                                 {'icon': 'bi bi-clock-history', 'label': 'Tempos e Métodos'}]},

                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Subir Carteiras'},
                                 {'icon': 'bi bi-list-ol', 'label': "Carteira OP's"},
                                 {'icon': 'bi bi-list-ol', 'label': 'Carteira Programação'},
                                 {'icon': 'bi bi-folder-x', 'label': 'Alterar - Excluir OP'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': 'Alterar Plano Nest'},
                                 {'icon': 'bi bi-person-lines-fill', 'label': 'Follow Up'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': 'Solicitar Reposição'}]},

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Programação',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Lista de Programados'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': "OP's á Programar"},
                                 {'icon': 'bi bi-cloud-download', 'label': "Baixar Nesting"}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista Geral'},
                                 {'icon': 'bi bi-ui-checks', 'label': 'Conferência Almoxarifado'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Conferência'},
                                 {'icon': 'bi bi-bag-check', 'label': 'Confirmar Recebimento'},
                                 {'icon': 'bi bi-ui-checks', 'label': 'Agrupar para Cotação'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Movimentação de Cotação'},
                                 {'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Itens Comprados'},
                                 {'icon': 'bi bi-box-arrow-in-down', 'label': 'Cadastrar Item'},
                                 {'icon': 'bi bi-building', 'label': 'Cadastrar Fornecedor'}]},

                    {'icon': 'bi bi-file-diff', 'label': 'Qualidade',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de PPM'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir SCI'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar - Finalizar SCI'},
                                 {'icon': 'bi bi-list-task', 'label': 'Lista de Instrumentos'},
                                 {'icon': 'bi bi-file-earmark-ruled', 'label': 'Relatórios Qualidade'}]},

                    {'icon': 'bi bi-send-plus', 'label': 'Serviço Externo',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Romaneio'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir Trabalho Externo'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Romaneio'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Romaneio'}]},

                    {'icon': 'bi bi-truck', 'label': 'Expedição',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Romaneio'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir Romaneio'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Romaneio'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Romaneio'}]},

                    {'icon': 'bi bi-person-raised-hand', 'label': 'RH',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Colaboradores'},
                                 {'icon': 'bi bi-calendar2-week', 'label': 'Cartão Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Cadastrar Colaborador'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Cadastrar Usuario'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'pcp':
                menu_opcao = [
                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Subir Carteiras'},
                                 {'icon': 'bi bi-list-ol', 'label': "Carteira OP's"},
                                 {'icon': 'bi bi-list-ol', 'label': 'Carteira Programação'},
                                 {'icon': 'bi bi-folder-x', 'label': 'Alterar - Excluir OP'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': 'Alterar Plano Nest'},
                                 {'icon': 'bi bi-person-lines-fill', 'label': 'Follow Up'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': 'Solicitar Reposição'}]},

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Programação',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Lista de Programados'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': "OP's á Programar"},
                                 {'icon': 'bi bi-cloud-download', 'label': "Baixar Nesting"}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista Geral'},
                                 {'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'Compras':
                menu_opcao = [
                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': "Carteira OP's"}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista Geral'},
                                 {'icon': 'bi bi-ui-checks', 'label': 'Conferência Almoxarifado'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Conferência'},
                                 {'icon': 'bi bi-bag-check', 'label': 'Confirmar Recebimento'},
                                 {'icon': 'bi bi-ui-checks', 'label': 'Agrupar para Cotação'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Movimentação de Cotação'},
                                 {'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Itens Comprados'},
                                 {'icon': 'bi bi-box-arrow-in-down', 'label': 'Cadastrar Item'},
                                 {'icon': 'bi bi-building', 'label': 'Cadastrar Fornecedor'}]},


                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'Engenharia-Qualidade':
                menu_opcao = [
                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': "Carteira OP's"}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista Geral'}]},

                    {'icon': 'bi bi-file-diff', 'label': 'Qualidade',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de PPM'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir SCI'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar - Finalizar SCI'},
                                 {'icon': 'bi bi-list-task', 'label': 'Lista de Instrumentos'},
                                 {'icon': 'bi bi-file-earmark-ruled', 'label': 'Relatórios Qualidade'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'Almoxaridado':
                menu_opcao = [
                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': "Carteira OP's"}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista Geral'},
                                 {'icon': 'bi bi-ui-checks', 'label': 'Conferência Almoxarifado'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Conferência'},
                                 {'icon': 'bi bi-bag-check', 'label': 'Confirmar Recebimento'},
                                 {'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'RH':
                menu_opcao = [
                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'}]},

                    {'icon': 'bi bi-person-raised-hand', 'label': 'RH',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Colaboradores'},
                                 {'icon': 'bi bi-calendar2-week', 'label': 'Cartão Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Cadastrar Colaborador'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Cadastrar Usuario'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'Caldeiraria':
                menu_opcao = [
                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': "Carteira OP's"}]},

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Programação',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Lista de Programados'},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': "OP's á Programar"},
                                 {'icon': 'bi bi-cloud-download', 'label': "Baixar Nesting"}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista Geral'},
                                 {'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'}]},

                    {'icon': 'bi bi-send-plus', 'label': 'Serviço Externo',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Romaneio'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir Trabalho Externo'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Romaneio'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Romaneio'}]},

                    {'icon': 'bi bi-truck', 'label': 'Expedição',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Lista de Romaneio'},
                                 {'icon': 'bi bi-folder-plus', 'label': 'Abrir Romaneio'},
                                 {'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Romaneio'},
                                 {'icon': 'bi bi-check2-circle', 'label': 'Finalizar Romaneio'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'Engenharia':
                menu_opcao = [

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Engenharia',
                     'submenu': [{'icon': 'bi bi-arrow-repeat', 'label': 'Atualizar Códigos'},
                                 {'icon': 'bi bi-list-ol', 'label': 'Análise Crítica'},
                                 {'icon': 'bi bi-clock-history', 'label': 'Tempos e Métodos'}]},

                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': "Carteira OP's"},
                                 {'icon': 'bi bi-bootstrap-reboot', 'label': 'Solicitar Reposição'}]},


                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'}]},


                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            if row[1] == 'comercial':
                menu_opcao = [
                    {'icon': 'bi bi-building', 'label': 'Comercial',
                     'submenu': [{'icon': 'bi bi-list-ol', 'label': 'Abrir Orçamento'},
                                 {'icon': 'bi bi-inboxes-fill', 'label': 'Finalizar Orçamento'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Precificação'},
                                 {'icon': 'bi bi-bag-check', 'label': 'Aprovação'}]},

                    {'icon': 'bi bi-gear-wide-connected', 'label': 'Engenharia',
                     'submenu': [{'icon': 'bi bi-clock-history', 'label': 'Tempos e Métodos'}]},


                    {'icon': 'bi bi-list-columns-reverse', 'label': 'PCP',
                     'submenu': [{'icon': 'bi bi-person-lines-fill', 'label': 'Follow Up'}]},

                    {'icon': 'bi bi-cart3', 'label': 'Compras',
                     'submenu': [{'icon': 'bi bi-cart-plus', 'label': 'Solicitar Compra'},
                                 {'icon': 'bi bi-cash-coin', 'label': 'Itens Comprados'}]},

                    {'icon': 'bi bi-person-circle', 'label': 'Conta',
                     'submenu': [{'icon': 'bi bi-list-task', 'label': 'Ponto'},
                                 {'icon': 'bi bi-person-plus', 'label': 'Configuração da Conta'}]}]

            tema = {'txc_inactive': 'black', 'menu_background': '#eaeaea', 'txc_active': 'black', 'option_active': '#ffffff', 'gap': '0rem'}
            opcao = hc.nav_bar(menu_definition=menu_opcao, home_name='Ambiente', override_theme=tema, sticky_mode='sticky', sticky_nav=False)

        if opcao == 'Abrir Orçamento':
            abrir_pedido.abri_pedido()

        if opcao == 'Ponto':
            cartao_ponto.cartao_ponto()

        if opcao == 'Configuração da Conta':
            configuracao_conta.configuracao_conta()

        if opcao == 'Subir Carteiras':
            import_carteiras.import_carteiras()

        if opcao == 'Carteira Programação':
            carteira_prog.carteira_prog()

        if opcao == "OP's á Programar":
            a_programar.a_programar()

        if opcao == "Baixar Nesting":
            baixar_nest.bixar_nest()

        if opcao == 'Abrir SCI':
            abir_coleta_de_dado_qualidade.abir_coleta_de_dado()

        if opcao == 'Lista Geral':
            lista_geral_compras_almoxarifado.lista_geral_compras_almoxarifado()

        if opcao == 'Conferência Almoxarifado':
            lista_agrupa_almoxarifado.lista_agrupa_almoxarifado()

        if opcao == 'Finalizar Conferência':
            finalizar_conferencia.finalizar_conferencia()

        if opcao == 'Agrupar para Cotação':
            agrupamento_cotacao.agrupamento_cotacao()

        if opcao == 'Movimentação de Cotação':
            precificacao_compras.precificacao_compras()

        if opcao == 'Cartão Ponto':
            ponto_rh.ponto_rh()

        if opcao == 'Lista de Programados':
            lista_programados_prog.lista_programados_prog()

        if opcao == 'Ambiente':
            ambiente.ambiente()

        if opcao == 'Relatórios Qualidade':
            relatorios.relatorios()

        if opcao == 'Lista de PPM':
            lista_sci.lista_sci()

        if opcao == 'Follow Up':
            fallow_up.fallow_up()

        if opcao == 'Solicitar Compra':
            solicitacao_compra.solicitacao_compra()

        if opcao == 'Itens Comprados':
            itens_comprado.itens_comprado()

        if opcao == 'Alterar Plano Nest':
            alterar_nest.alterar_nest()

        if opcao == 'Cadastrar Fornecedor':
            cadastrar_fornecedor.cadastrar_fornecedor()

        if opcao == 'Tempos e Métodos':
            criar_estrutura.criar_estrutura()

        if opcao == 'Teste':
            testes.teste()

        if opcao == 'Finalizar Orçamento':
            finalizar_pedido.finalizar_pedido()

        if opcao == 'Aprovação':
            aprovacao_pedido_comercial.aprovacao_pedido_comercial()











