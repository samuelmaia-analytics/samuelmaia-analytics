from __future__ import annotations

import json

import streamlit as st

from app.ui.components import (
    render_bullet_card,
    render_hero_panel,
    render_info_card,
    render_kpi_grid,
    render_section_header,
)
from app.ui.theme import inject_theme
from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


PORTFOLIO_URL = "https://samuelmaia-analytics.github.io/samuelmaia-analytics/"
LINKEDIN_URL = "https://www.linkedin.com/in/samuelmaia-analytics/"
GITHUB_URL = "https://github.com/samuelmaia-analytics"
EMAIL = "samuelmaia.carreira@gmail.com"


def main() -> None:
    settings = get_settings()
    st.set_page_config(
        page_title="Samuel Maia | Analytics Engineer",
        page_icon="SM",
        layout="wide",
    )
    inject_theme()

    snapshot = build_portfolio_snapshot(settings)
    executive_summary = snapshot["genai_outputs"]["executive_summary"]
    change_drivers = snapshot["change_drivers"]
    quality_report = snapshot["quality_report"]

    st.sidebar.title("Samuel Maia")
    st.sidebar.caption("Analytics Engineer | Data, BI & Automation")
    st.sidebar.markdown(
        f"""
        **Contato profissional**  
        [{EMAIL}](mailto:{EMAIL})  
        [LinkedIn]({LINKEDIN_URL})  
        [GitHub]({GITHUB_URL})

        **Disponibilidade**  
        Projetos, posições full-time no Brasil e oportunidades remotas/internacionais.
        """
    )

    render_hero_panel(
        "Analytics Engineer | Data, BI & Automation",
        "Transformo dados e processos em soluções analíticas confiáveis, automações e produtos de dados que apoiam decisões de negócio.",
        "Samuel Maia",
        chips=[
            "Python · SQL · dbt · PostgreSQL",
            "Power BI · Streamlit · FastAPI",
            "Data Quality · Governance · Automation",
        ],
    )

    st.markdown(
        f"[LinkedIn]({LINKEDIN_URL}) · [GitHub]({GITHUB_URL}) · [E-mail](mailto:{EMAIL}) · [Portfólio]({PORTFOLIO_URL})"
    )

    render_section_header(
        "Como posso ajudar",
        "Soluções orientadas a confiabilidade, automação, clareza analítica e redução de trabalho manual.",
    )
    service_cols = st.columns(3)
    with service_cols[0]:
        render_info_card(
            "Analytics Engineering",
            "Pipelines ETL/ELT, modelagem analítica, dbt, SQL e camadas de dados preparadas para BI e aplicações.",
        )
    with service_cols[1]:
        render_info_card(
            "Qualidade & Governança",
            "Data Quality, Data Contracts, lineage, rastreabilidade, regras de publicação e controles de privacidade.",
        )
    with service_cols[2]:
        render_info_card(
            "BI & Automação",
            "Dashboards, KPIs, integrações com APIs e automação de processos com Python, Power BI, Streamlit e n8n.",
        )

    render_section_header(
        "Experiência independente desde 2022",
        "Projetos de Dados, BI, automação e tecnologia desenvolvidos de forma independente, inicialmente em demandas pontuais e estudos aplicados, evoluindo para soluções mais estruturadas de Analytics Engineering.",
    )
    experience_left, experience_right = st.columns((1.15, 0.85))
    with experience_left:
        render_info_card(
            "Analytics Engineer | Data & BI Consultant",
            "Atuação independente desde 2022 com pipelines ETL/ELT, modelagem analítica, Data Quality, governança, dashboards, APIs, automação e integração de dados. O foco evoluiu de demandas pontuais e estudos aplicados para projetos estruturados com práticas de engenharia e governança de dados.",
        )
    with experience_right:
        render_bullet_card(
            "Principais frentes",
            [
                "Pipelines e transformação com Python, SQL, dbt, DuckDB e PostgreSQL.",
                "Dashboards e aplicações com Power BI, Streamlit e FastAPI.",
                "Data Quality, Data Contracts, lineage e controles de publicação.",
                "Automação de fluxos e integrações com APIs e n8n.",
                "Testes, documentação e CI/CD com GitHub Actions.",
            ],
        )

    render_section_header(
        "Projetos principais",
        "Três projetos complementares que demonstram Analytics Engineering, automação operacional e cloud.",
    )

    project1, project2, project3 = st.columns(3)
    with project1:
        render_info_card(
            "Governed Analytics Platform",
            "Plataforma de Analytics Engineering com 4 camadas de dados, 3 estados de publicação e 7 workflows de automação/CI, combinando qualidade, governança, lineage e consumo executivo.",
        )
        st.markdown(
            "**Stack:** Python · SQL · dbt · DuckDB · PostgreSQL · FastAPI · Streamlit · GitHub Actions · n8n"
        )
        st.link_button(
            "Ver repositório",
            "https://github.com/samuelmaia-analytics/Governed-Analytics-Platform",
            width="stretch",
        )

    with project2:
        render_info_card(
            "Central de Automação e Operações",
            "Produto analítico para monitoramento de workflows, SLA, backlog, criticidade e saúde operacional, com integração Pipefy e alertas automáticos.",
        )
        st.markdown("**Stack:** Python · SQL · Streamlit · Pipefy GraphQL · regras de automação")
        st.link_button(
            "Ver demonstração",
            "https://central-automacao-operacoes.streamlit.app/",
            width="stretch",
        )

    with project3:
        render_info_card(
            "AWS Serverless Access Counter",
            "Arquitetura serverless construída no AWS re/Start utilizando 10 serviços AWS para entrega web, API, persistência, segurança, observabilidade e custos.",
        )
        st.markdown(
            "**Stack AWS:** CloudFront · S3 · API Gateway · Lambda · DynamoDB · CloudWatch · IAM · WAF · SNS · Budgets"
        )
        st.link_button(
            "Ver repositório",
            "https://github.com/samuelmaia-analytics/aws-serverless-access-counter",
            width="stretch",
        )

    render_section_header(
        "Impacto demonstrado",
        "Métricas abaixo descrevem escopo implementado nos projetos — não são percentuais fictícios de economia ou produtividade.",
    )
    impact_cols = st.columns(4)
    impact_cols[0].metric("Camadas de dados", "4")
    impact_cols[1].metric("Estados de publicação", "3")
    impact_cols[2].metric("Workflows GitHub Actions", "7")
    impact_cols[3].metric("Serviços AWS no TCC", "10")

    render_section_header(
        "Stack principal",
        "Tecnologias utilizadas para construir soluções de dados, BI, automação, qualidade e cloud.",
    )
    st.markdown(
        "**Dados & Analytics:** Python · SQL · pandas · DuckDB · PostgreSQL · MySQL/MariaDB  \n"
        "**Analytics Engineering:** dbt · ETL/ELT · modelagem dimensional · Bronze/Silver/Gold  \n"
        "**BI & Apps:** Power BI · Streamlit · Plotly · FastAPI  \n"
        "**Qualidade & Engenharia:** Pytest · Ruff · mypy · Git · GitHub Actions · Codecov  \n"
        "**Automação & Cloud:** n8n · APIs · AWS"
    )

    render_section_header(
        "Sobre meu trabalho",
        "Uma combinação de visão de negócio com engenharia aplicada a dados.",
    )
    about_left, about_right = st.columns((1.2, 0.8))
    with about_left:
        render_info_card(
            "Meu foco",
            "Desenvolvo soluções de ponta a ponta envolvendo ingestão, transformação, modelagem, qualidade, governança, automação e consumo analítico, sempre conectando decisão técnica ao problema de negócio.",
        )
    with about_right:
        render_bullet_card(
            "O que priorizo",
            [
                "Dados confiáveis antes do consumo.",
                "Automação para reduzir tarefas manuais.",
                "Rastreabilidade e documentação.",
                "Indicadores compreensíveis para áreas de negócio.",
            ],
        )

    with st.expander("Technical Portfolio Lab — arquitetura, qualidade, métricas e observabilidade"):
        st.caption(
            "Esta área mantém a demonstração técnica do próprio portfólio para revisão aprofundada por profissionais de dados e engenharia."
        )
        render_kpi_grid(snapshot["semantic_metrics"])

        overview_col, action_col = st.columns((1.15, 0.85))
        with overview_col:
            render_info_card("Executive Summary", executive_summary["narrative"])
            render_bullet_card("Executive Signals", executive_summary["bullets"])
        with action_col:
            render_info_card("Recommended Action", change_drivers.get("recommended_action", ""))

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Operating Surface", "Quality and Governance", "GenAI Insights", "Observability"]
        )

        with tab1:
            st.dataframe(snapshot["repository_registry"], width="stretch", hide_index=True)
            if change_drivers.get("drivers"):
                st.dataframe(change_drivers["drivers"], width="stretch", hide_index=True)

        with tab2:
            quality_left, quality_right = st.columns((0.8, 1.2))
            with quality_left:
                st.metric("Checks", f"{quality_report['total_checks']}")
                st.metric("Passed", f"{quality_report['passed_checks']}")
                st.metric("Pass Rate", f"{quality_report['pass_rate']:.1f}%")
            with quality_right:
                st.dataframe(quality_report["results"], width="stretch", hide_index=True)
            st.json(snapshot["metric_catalog"])

        with tab3:
            st.markdown(snapshot["genai_insight"]["narrative"])
            st.caption(f"Provider status: {snapshot['genai_insight']['provider_status']}")

        with tab4:
            st.code(json.dumps(snapshot["observability_event"], indent=2), language="json")
            recent_events = snapshot["operational_context"].get("recent_events", [])
            if recent_events:
                st.dataframe(recent_events, width="stretch", hide_index=True)

    st.divider()
    st.subheader("Vamos conversar?")
    st.write(
        "Disponível para projetos de Data Analytics, BI, Analytics Engineering e Automation, além de oportunidades full-time no Brasil e posições remotas/internacionais."
    )
    contact_cols = st.columns(3)
    contact_cols[0].link_button("E-mail", f"mailto:{EMAIL}", width="stretch")
    contact_cols[1].link_button("LinkedIn", LINKEDIN_URL, width="stretch")
    contact_cols[2].link_button("GitHub", GITHUB_URL, width="stretch")


if __name__ == "__main__":
    main()
