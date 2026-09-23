<a id="top"></a>

# Samuel Maia | Data Engineer

<p align="left">
  <a href="https://github.com/samuelmaia-analytics/samuelmaia-analytics/actions/workflows/ci.yml"><img src="https://github.com/samuelmaia-analytics/samuelmaia-analytics/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://codecov.io/gh/samuelmaia-analytics/samuelmaia-analytics"><img src="https://codecov.io/gh/samuelmaia-analytics/samuelmaia-analytics/branch/main/graph/badge.svg" alt="Cobertura" /></a>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+" />
</p>

**Engenharia de Dados · Analytics Engineering · Qualidade e Governança**

Construo soluções para transformar dados brutos em dados confiáveis para análise e tomada de decisão.

Fui contratado pela **Avanade** para atuar como **Data Engineer**, com início em **outubro de 2026**, trabalhando com **Databricks, PySpark, SQL, Python e Delta Lake**.

## Foco
- Engenharia de Dados e pipelines ETL/ELT
- Databricks, PySpark, Apache Spark e Delta Lake
- Arquiteturas Raw, Bronze, Silver e Gold
- Data Quality, Data Contracts, Data Lineage e governança
- Testes automatizados, CI/CD e observabilidade
- Analytics Engineering e consumo analítico

## Projetos em destaque

### 1) Azure Databricks Governed Lakehouse
**Contexto:** pipelines precisam impedir que dados fora dos critérios de qualidade avancem para consumo.

**Ação:** arquitetura Lakehouse com PySpark, Delta Lake e SQL, estruturada em Raw → Bronze → Silver → Gold, com Quarantine, Data Quality, testes automatizados e Publication Gate.

**Resultado:** critérios explícitos para controlar a progressão dos dados entre camadas e tratar registros inválidos de forma rastreável.

Repositório: https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse

---

### 2) Governed Analytics Platform
**Contexto:** dados inconsistentes ou sem regras claras de publicação aumentam o risco de decisões baseadas em informação pouco confiável.

**Ação:** plataforma com Python, SQL, dbt, DuckDB e PostgreSQL, incorporando Data Contracts, Data Quality, Data Lineage, Publication Gate e CI/CD.

**Resultado:** cada execução recebe um estado explícito de publicação — Approved, Needs Review ou Blocked — antes do consumo analítico.

Repositório: https://github.com/samuelmaia-analytics/Governed-Analytics-Platform  
Demo: https://governed-analytics-platform.streamlit.app/

---

### 3) Central de Automação e Operações
**Contexto:** workflows operacionais dispersos dificultam acompanhamento de SLA, backlog e criticidade.

**Ação:** solução com Python, SQL, Streamlit e integração Pipefy via API/GraphQL, com alertas e indicadores operacionais.

**Resultado:** centralização do acompanhamento e priorização de situações que exigem atenção operacional.

Repositório: https://github.com/samuelmaia-analytics/central-automacao-operacoes  
Demo: https://central-automacao-operacoes.streamlit.app/

## Stack principal
Databricks · PySpark · Apache Spark · Delta Lake · Python · SQL · dbt · PostgreSQL · DuckDB · Pytest · GitHub Actions · Azure · AWS · Power BI · Streamlit

## Trajetória recente
Entre 2022 e 2026 desenvolvi projetos de forma independente pela **Samuel Maia Analytics**, conectando Dados, BI, Analytics Engineering, automação, qualidade e governança. Em outubro de 2026 inicio uma nova etapa profissional como **Data Engineer na Avanade**.

## Contato
GitHub: https://github.com/samuelmaia-analytics  
LinkedIn: https://www.linkedin.com/in/samuelmaia-analytics  
Portfólio: https://samuelmaia-analytics.github.io/samuelmaia-analytics/

[⬆ Voltar ao topo](#top)
