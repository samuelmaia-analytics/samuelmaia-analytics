# Samuel Maia

**Engenheiro de Dados Pleno | Analytics Engineering | SQL, Python e PySpark**

Construo soluções de dados para transformar informações brutas em dados confiáveis para análise e tomada de decisão.

Atuo na **Avanade** como **Analyst, Data Engineering | Engenheiro de Dados Pleno**, desde **out/2026**. Meu escopo técnico inclui pipelines ETL/ELT, ingestão, transformação, modelagem, qualidade e governança, com SQL, Python, PySpark, Azure Databricks e Delta Lake.

Minha trajetória conecta negócio, operações, BI e Analytics Engineering. Na **Samuel Maia Analytics**, como **Analytics Engineer | Data & BI Consultant**, entre **ago/2022 e set/2026**, desenvolvi pipelines, modelos dimensionais e aplicações analíticas com Python, SQL, dbt, DuckDB, PostgreSQL, Power BI e Streamlit.

Aprofundei essa base em um Lakehouse com PySpark e Delta Lake, validado localmente, e em projetos de **IA generativa e RAG**. No Governed Analytics Platform, o assistente consulta contratos técnicos aprovados, recupera evidências localmente e responde com citações. A chamada à OpenAI é opcional e depende do consentimento para cada consulta.

[LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/) · [Currículo em PDF](docs/assets/Samuel_Maia_Curriculo.pdf)

---

## Stack principal

**Engenharia de Dados:** Python · SQL · PySpark · Apache Spark · Delta Lake · ETL/ELT · Data Lake · Data Warehouse · Lakehouse · conhecimentos em Azure Databricks  
**Analytics Engineering e BI:** dbt · DuckDB · PostgreSQL · modelagem dimensional · Power BI · DAX · Power Query  
**Qualidade e governança:** Data Quality · Data Contracts · Data Lineage · Publication Gate · reconciliação · controles de privacidade  
**IA generativa e RAG:** OpenAI API opcional · TF-IDF local · contratos YAML aprovados · manifesto e SHA-256 · citações · consentimento por consulta  
**Automação e aplicações:** pandas · NumPy · Streamlit · FastAPI · APIs REST · GraphQL · workflows com n8n  
**Cloud e engenharia:** AWS · Git · GitHub Actions · CI/CD · pytest · Ruff · mypy

---

## Projetos em destaque

### 1. [Azure Databricks Governed Lakehouse](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse) | 2026

**Contexto:** em um fluxo analítico de pedidos e produtos, a publicação exige critérios de qualidade e integridade.

**Ação:** desenvolvi um Lakehouse em Python, PySpark e Delta Lake, com camadas Raw, Bronze, Silver, Gold e Quarantine, schemas explícitos, validações e Publication Gate.

**Resultado:** a execução local documentada publicou **seis datasets Silver e quatro tabelas Gold**, com reconciliações sem perdas ou multiplicações de registros. A execução local documentada registrou **186 testes automatizados**, conforme o currículo atualizado.

**Escopo:** execução validada localmente. Azure Databricks é a plataforma-alvo; a execução em nuvem permanece prevista.

[Ver repositório e evidências](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse)

### 2. [Governed Analytics Platform](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) | 2026

**Contexto:** dados de e-commerce precisam de qualidade e rastreabilidade para apoiar o consumo executivo.

**Ação:** construí uma plataforma com Python, SQL, dbt, DuckDB e PostgreSQL, incorporando Data Contracts, Data Quality, Data Lineage, Privacy Risk Score, Publication Gate, Streamlit, FastAPI e CI/CD. Acrescentei extração estruturada de atributos com OpenAI API opcional e um assistente RAG de governança com TF-IDF local, citações e contratos aprovados.

**Resultado:** o fluxo registra decisões de publicação **Approved, Needs Review ou Blocked**, mantém evidências de governança e disponibiliza dados e atributos estruturados para consumo analítico.

**Escopo:** a extração generativa exibe resultados previamente persistidos. O assistente RAG consulta somente três contratos YAML aprovados, validados por manifesto e SHA-256. TF-IDF local é o padrão; a chamada OpenAI é opcional, requer consentimento por consulta e usa evidências com citações. Sem evidência suficiente, o assistente se abstém; não executa SQL ou ações e não persiste histórico. A arquitetura Azure é proposta, ainda não implantada.

[Ver repositório](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) · [Abrir demonstração](https://governed-analytics-platform.streamlit.app/)

### 3. [Central de Automação e Operações](https://github.com/samuelmaia-analytics/central-automacao-operacoes) | 2026

**Contexto:** o acompanhamento de múltiplos workflows exige uma visão consolidada de prazos, responsáveis e prioridades.

**Ação:** desenvolvi uma central com Python, SQL, DuckDB e Streamlit, integrada ao Pipefy via API/GraphQL, com regras de criticidade, indicadores de SLA, backlog e alertas.

**Resultado:** a visão consolidada permite identificar demandas vencidas, sem responsável ou prioritárias e apoiar o acompanhamento operacional.

[Ver repositório](https://github.com/samuelmaia-analytics/central-automacao-operacoes) · [Abrir demonstração](https://central-automacao-operacoes.streamlit.app/)

---

## Projetos complementares

- **[AWS Serverless Access Counter](https://github.com/samuelmaia-analytics/aws-serverless-access-counter):** projeto em grupo do AWS re/Start com CloudFront, S3, API Gateway, Lambda, DynamoDB, IAM, WAF, CloudWatch, SNS e AWS Budgets.
- **[Churn Prediction Data Product](https://github.com/samuelmaia-analytics/churn-prediction):** preparação de features, treinamento e inferência com scikit-learn, priorização de clientes e monitoramento de drift com PSI/KS.
- **[Revenue Intelligence Platform Suite](https://github.com/samuelmaia-analytics/revenue-intelligence-platform-suite):** métricas governadas, camada semântica, Prefect, Pandera, qualidade, observabilidade e aplicações analíticas.

## Como apresento as entregas

Os projetos apresentam ferramentas, decisões técnicas, resultados e evidências verificáveis. Execuções locais, componentes opcionais e próximos passos ficam explicitados na documentação. As métricas descrevem o escopo implementado e os resultados das validações.

## Evidências da revisão de governança

As validações documentadas entre **24 e 31/10/2026** incluem as seguintes revisões e resultados:

| Projeto | Testes aprovados | Melhoria verificada | Alteração proposta |
|---|---:|---|---|
| Lakehouse | 186 | Seis datasets Silver e quatro tabelas Gold na execução local documentada | [Repositório](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse) |
| Governed Analytics | 1.111 testes · 92% cobertura | RAG com contratos aprovados, citações e abstinência; resultado registrado em 31/10/2026 | [Repositório](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) |
| Central de Automação | 27 | Bloqueio de inconsistências antes da publicação | [PR #1](https://github.com/samuelmaia-analytics/central-automacao-operacoes/pull/1) |

Os números são históricos e se referem às validações registradas em cada projeto; não foram reexecutados durante esta atualização do perfil. A execução em Azure Databricks permanece prevista, não validada em nuvem.

Os projetos são pessoais e independentes da atuação na Avanade; não representam entregas ou dados da empresa e de seus clientes.

## Formação

- Pós-graduação em Inovação e Transformação Digital — Gran Faculdade | out/2026
- Pós-graduação em Ciência de Dados — Gran Faculdade | abr/2026
- Bacharelado em Administração — FAEL | jul/2024
- AWS re/Start, Inteligência Artificial e No Code — Escola da Nuvem | 270h | jul/2026
- Databricks Certified Data Engineer Associate — **curso preparatório Udemy**, 13,5h | out/2026. Certificado de conclusão do curso.

## Contato profissional

Fortaleza/CE · [E-mail](mailto:samuelmaia.carreira@gmail.com) · [LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/)
