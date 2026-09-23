# Samuel Maia

**Data Engineer | Analytics Engineering | Data Quality & Governance**

Construo soluções de dados para transformar informações brutas em dados confiáveis para análise e tomada de decisão.

Fui contratado pela **Avanade** para atuar como **Data Engineer**, com início em **outubro de 2026**, ampliando minha atuação em Engenharia de Dados com **Databricks, PySpark, SQL, Python, Delta Lake, qualidade e governança de dados**.

Minha trajetória combina visão de negócio, Analytics Engineering e práticas de engenharia de software aplicadas a dados: ingestão, transformação, modelagem, testes, observabilidade, governança e publicação controlada.

Entre 2022 e 2026 também desenvolvi projetos de forma independente pela **Samuel Maia Analytics**, com foco em Dados, BI, Analytics Engineering e automação.

[LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/) · [GitHub](https://github.com/samuelmaia-analytics)

---

## Foco profissional

- Engenharia de Dados com Databricks, PySpark, SQL e Python
- Arquiteturas Lakehouse e pipelines ETL/ELT
- Modelagem e transformação de dados
- Data Quality, Data Contracts, Data Lineage e governança
- Testes automatizados, CI/CD e observabilidade
- Analytics Engineering e disponibilização confiável de dados para consumo analítico

## Stack principal

**Data Engineering:** Databricks · PySpark · Apache Spark · Delta Lake · Python · SQL  
**Analytics Engineering:** dbt · ETL/ELT · modelagem dimensional · Raw/Bronze/Silver/Gold  
**Dados:** DuckDB · PostgreSQL · pandas  
**Qualidade e governança:** Data Quality · Data Contracts · Data Lineage · Publication Gate  
**Engenharia:** Pytest · Ruff · mypy · Git · GitHub Actions · CI/CD  
**Cloud e aplicações:** Azure · AWS · Streamlit · FastAPI · Power BI

---

## Projetos em destaque

### 1. [Azure Databricks Governed Lakehouse](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse)

**Contexto:** pipelines analíticos precisam impedir que dados fora dos critérios de qualidade avancem para camadas utilizadas pelo negócio.

**Ação:** desenvolvi uma arquitetura Lakehouse com **PySpark 3.5, Delta Lake e SQL**, estruturada em **Raw → Bronze → Silver → Gold**, com Quarantine, regras de Data Quality, testes automatizados e Publication Gate antes da Silver. O projeto possui execução local e preparação para Azure Databricks.

**Resultado:** a arquitetura estabelece critérios objetivos para controlar a progressão dos dados entre camadas e torna explícito o tratamento de registros inválidos, criando uma base reproduzível para qualidade e governança em pipelines de Engenharia de Dados.

[Ver repositório](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse)

---

### 2. [Governed Analytics Platform](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform)

**Contexto:** dados podem chegar ao consumo analítico mesmo quando apresentam inconsistências ou não possuem critérios claros de qualidade, rastreabilidade e publicação.

**Ação:** construí uma plataforma de Analytics Engineering com Python, SQL, dbt, DuckDB e PostgreSQL, incorporando Data Contracts, Data Quality, Data Lineage, Privacy Risk Score, Publication Gate, FastAPI, Streamlit e CI/CD.

**Resultado:** o fluxo classifica cada execução como **Approved, Needs Review ou Blocked**, criando um critério explícito antes da publicação. O projeto possui **4 camadas de dados**, **3 estados de publicação** e **7 workflows no GitHub Actions**, além de testes automatizados para reduzir o risco de regressões em regras de qualidade e governança.

[Ver repositório](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) · [Abrir demonstração](https://governed-analytics-platform.streamlit.app/)

---

### 3. [Central de Automação e Operações](https://github.com/samuelmaia-analytics/central-automacao-operacoes)

**Contexto:** operações com múltiplos workflows podem perder visibilidade de SLA, backlog, criticidade e gargalos quando as informações ficam dispersas.

**Ação:** desenvolvi uma solução analítica com Python, SQL e Streamlit, integração ao Pipefy via API/GraphQL, regras de criticidade, alertas e indicadores operacionais.

**Resultado:** a solução centraliza acompanhamento e priorização em uma única visão, facilitando a identificação de situações que exigem atenção antes que se transformem em violações de SLA ou acúmulo de backlog.

[Ver repositório](https://github.com/samuelmaia-analytics/central-automacao-operacoes) · [Abrir demonstração](https://central-automacao-operacoes.streamlit.app/)

---

## Projetos complementares

### [AWS Serverless Access Counter](https://github.com/samuelmaia-analytics/aws-serverless-access-counter)

Arquitetura serverless desenvolvida durante o AWS re/Start, integrando serviços AWS para entrega web, API, processamento, persistência, segurança, observabilidade e acompanhamento de custos.

### [Churn Prediction Data Product](https://github.com/samuelmaia-analytics/churn-prediction)

Produto de dados para priorização de clientes com risco de churn, combinando pipeline em camadas, Machine Learning, inferência, monitoramento de drift, Streamlit e FastAPI.

### [Revenue Intelligence Platform Suite](https://github.com/samuelmaia-analytics/revenue-intelligence-platform-suite)

Plataforma de Revenue Intelligence com ingestão, transformação, métricas governadas, qualidade, insights executivos e aplicações analíticas.

---

## Como construo os projetos

Cada projeto procura demonstrar não apenas código, mas também o raciocínio por trás da solução:

- problema e contexto de negócio;
- arquitetura e fluxo dos dados;
- decisões técnicas;
- qualidade, validações e governança;
- documentação e rastreabilidade;
- testes e automação;
- consumo analítico quando aplicável.

As métricas apresentadas descrevem o **escopo realmente implementado**. Não utilizo percentuais fictícios de economia, produtividade ou impacto financeiro quando eles não foram medidos em ambiente real.

---

## Contato e networking

📩 **Email:** samuelmaia.carreira@gmail.com  
💼 **LinkedIn:** https://www.linkedin.com/in/samuelmaia-analytics/  
🌐 **Portfólio:** https://samuelmaia-analytics.github.io/samuelmaia-analytics/
