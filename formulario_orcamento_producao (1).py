"""
Formulário de Orçamento de Produção - GDA 2027
================================================
Aplicativo Streamlit para que um usuário externo (terceiro) preencha os dados
mensais de produção e, ao clicar em "Enviar", os dados sejam enviados em
formato JSON via POST para uma URL de Webhook (ex.: Power Automate, Make,
Zapier, n8n, um endpoint próprio, etc.).

Como executar:
    pip install streamlit requests
    streamlit run formulario_orcamento_producao.py
"""

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO DO WEBHOOK
# ---------------------------------------------------------------------------
# >>> COLE AQUI A URL DO SEU WEBHOOK <<<
# Exemplo: "https://hooks.zapier.com/hooks/catch/123456/abcdef/"
WEBHOOK_URL = "https://defaulta620ebd674a048e199e1c7ea3d43dc.17.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/27/workflows/2be2b5a5b06a45e09a804ecf39e9492a/triggers/manual/paths/invoke?api-version=1"
# ---------------------------------------------------------------------------

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

st.set_page_config(page_title="Orçamento de Produção - GDA 2027", page_icon="📊")

st.title("📊 Formulário de Orçamento de Produção - GDA 2027")
st.markdown(
    "Preencha os campos abaixo referentes ao mês de produção e clique em "
    "**Enviar** para registrar as informações."
)

with st.form("form_orcamento_producao", clear_on_submit=False):

    mes = st.selectbox("Mês", MESES)

    horas_operacao = st.number_input(
        "Horas em Operação", min_value=0.0, max_value=744.0, step=1.0, format="%.2f"
    )

    fator_pcs_9400 = st.number_input(
        "Fator conversão - PCS 9400", min_value=0.0, step=0.0001, format="%.4f"
    )

    fator_biogas_biometano = st.number_input(
        "Fator conversão - Biogás x Biometano", min_value=0.0, step=0.0001, format="%.4f"
    )

    fator_biometano_cbios = st.number_input(
        "Fator conversão Biometano/CBIOS", min_value=0.0, step=0.0001, format="%.4f"
    )

    fator_biometano_biorec = st.number_input(
        "Fator conversão Biometano/BioRec", min_value=0.0, step=0.0001, format="%.4f"
    )

    producao_biogas = st.number_input(
        "Produção de Biogás", min_value=0.0, step=0.01, format="%.2f"
    )

    volume_diario_cdgn = st.number_input(
        "Volume Diário (CDGN/Postos)", min_value=0.0, step=0.01, format="%.2f"
    )

    volume_diario_neogas = st.number_input(
        "Volume Diário (Neogás/Postos)", min_value=0.0, step=0.01, format="%.2f"
    )

    volume_diario_ultra = st.number_input(
        "Volume Diário (Ultra)", min_value=0.0, step=0.01, format="%.2f"
    )

    enviado = st.form_submit_button("Enviar")

if enviado:
    # Monta o payload em JSON com os dados preenchidos no formulário
    payload = {
        "mes": mes,
        "horas_em_operacao": horas_operacao,
        "fator_conversao_pcs_9400": fator_pcs_9400,
        "fator_conversao_biogas_x_biometano": fator_biogas_biometano,
        "fator_conversao_biometano_cbios": fator_biometano_cbios,
        "fator_conversao_biometano_biorec": fator_biometano_biorec,
        "producao_de_biogas": producao_biogas,
        "volume_diario_cdgn_postos": volume_diario_cdgn,
        "volume_diario_neogas_postos": volume_diario_neogas,
        "volume_diario_ultra": volume_diario_ultra,
    }

    if not WEBHOOK_URL or WEBHOOK_URL == "COLE_AQUI_A_URL_DO_SEU_WEBHOOK":
        st.error(
            "⚠️ A URL do Webhook ainda não foi configurada. "
            "Edite a variável WEBHOOK_URL no início do código."
        )
    else:
        try:
            response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
            # Levanta uma exceção se o status HTTP indicar erro (4xx ou 5xx)
            response.raise_for_status()
            st.success("✅ Dados enviados com sucesso!")
            with st.expander("Ver dados enviados"):
                st.json(payload)
        except requests.exceptions.Timeout:
            st.error("❌ Tempo de espera esgotado ao tentar enviar os dados. Tente novamente.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Não foi possível conectar ao Webhook. Verifique a URL e sua conexão com a internet.")
        except requests.exceptions.HTTPError as http_err:
            st.error(f"❌ O servidor do Webhook retornou um erro: {http_err}")
        except requests.exceptions.RequestException as err:
            st.error(f"❌ Ocorreu um erro inesperado ao enviar os dados: {err}")
