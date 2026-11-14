# Samuel Maia

**Engenheiro de Dados Pleno | Analytics Engineering | SQL, Python e PySpark**

Desenvolvo projetos de dados com foco em ingestão, transformação, qualidade e publicação controlada, conectando Python, SQL, Analytics Engineering e automação.

Atuo na **Avanade** como **Analyst, Data Engineering | Engenheiro de Dados Pleno**, desde **out/2026**. Meu escopo técnico inclui pipelines ETL/ELT, ingestão, transformação, modelagem, qualidade e governança, com SQL, Python, PySpark, Azure Databricks e Delta Lake.

Minha trajetória conecta negócio, operações, BI e Analytics Engineering. Na **Samuel Maia Analytics**, como **Analytics Engineer | Data & BI Consultant**, entre **ago/2022 e set/2026**, desenvolvi pipelines, modelos dimensionais e aplicações analíticas com Python, SQL, dbt, DuckDB, PostgreSQL, Power BI e Streamlit.

Aprofundei essa base em um Lakehouse com PySpark e Delta Lake, validado localmente, e em projetos de **IA generativa e RAG**. No Governed Analytics Platform, o assistente consulta contratos técnicos aprovados, recupera evidências localmente e responde com citações. A chamada à OpenAI é opcional e depende do consentimento para cada consulta.

[LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/) · [Currículo em PDF](https://samuelmaia-analytics.github.io/samuelmaia-analytics/assets/Samuel_Maia_Curriculo.pdf)

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

### 1. [Governed Analytics Platform](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) | 2026

**Contexto:** dados analíticos sem contratos e critérios de publicação tendem a gerar inconsistências e dificultar auditoria e consumo confiável.

**Ação:** desenvolvi uma plataforma demonstrativa com camadas Bronze/Silver/Gold e Quarantine, Data Contracts, Data Quality, governança e rastreabilidade, com Publication Gate para decisões de publicação. Inclui interface Streamlit e APIs FastAPI para exploração e observabilidade.

**Resultado:** validação local em **13/11/2026** com **1.353 testes aprovados**, **92% de cobertura total** em `src + app` e **nenhuma falha**. O repositório documenta evidências, limites e componentes opcionais (projeto de portfólio; sem implantação corporativa comprovada).

[Ver repositório](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) · [Abrir demonstração](https://governed-analytics-platform.streamlit.app/)

### 2. [Azure Databricks Governed Lakehouse](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse) | 2026

**Contexto:** em um fluxo analítico de pedidos e produtos, a publicação exige critérios de qualidade e integridade.

**Ação:** desenvolvi um Lakehouse em Python, PySpark e Delta Lake com camadas Raw/Bronze/Silver/Gold/Quarantine, schemas explícitos e Publication Gate. Inclui validações e reconciliações para evitar perdas ou multiplicações de registros.

**Resultado:** a execução local documentada publicou **seis datasets Silver** e **quatro tabelas Gold**, com **186 testes automatizados** (conforme currículo). Azure Databricks é a plataforma-alvo; a execução em nuvem permanece prevista.

[Ver repositório e evidências](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse)

### 3. [Central de Automação e Operações](https://github.com/samuelmaia-analytics/central-automacao-operacoes) | 2026

**Contexto:** o acompanhamento de múltiplos workflows exige visibilidade de prazos, responsáveis, backlog e criticidade.

**Ação:** desenvolvi uma central com Python, SQL, DuckDB e Streamlit, integrada ao Pipefy via API/GraphQL, com regras de criticidade, indicadores de SLA, backlog e alertas. Estruturei a navegação para destacar demandas vencidas, sem responsável ou prioritárias.

**Resultado:** entrega uma visão consolidada para acompanhamento operacional e identificação de pontos de atenção, sem extrapolar métricas não comprovadas. A demonstração depende de configuração de acesso à API e pode operar com dados de exemplo.

[Ver repositório](https://github.com/samuelmaia-analytics/central-automacao-operacoes) · [Abrir demonstração](https://central-automacao-operacoes.streamlit.app/)

---

## Projetos complementares

- **[Contador de Acessos Serverless na AWS](https://github.com/samuelmaia-analytics/aws-serverless-access-counter) (AWS re/Start):** participei do desenvolvimento de um contador de acessos com frontend estático e função Lambda em Python que incrementa o contador atomicamente no DynamoDB. A arquitetura documentada reúne entrega web, API, persistência, segurança, observabilidade e acompanhamento de custos. O frontend ainda precisa receber o endpoint real do API Gateway; a infraestrutura como código está planejada; o conteúdo versionado não comprova implantação dos dez serviços da arquitetura.
- **[Churn Prediction Data Product](https://github.com/samuelmaia-analytics/churn-prediction):** preparação de features, treinamento e inferência com scikit-learn, priorização de clientes e monitoramento de drift com PSI/KS.
- **[Revenue Intelligence Platform Suite](https://github.com/samuelmaia-analytics/revenue-intelligence-platform-suite):** métricas governadas, camada semântica, Prefect, Pandera, qualidade, observabilidade e aplicações analíticas.

## Como apresento as entregas

Os projetos apresentam ferramentas, decisões técnicas, resultados e evidências verificáveis. Execuções locais, componentes opcionais e próximos passos ficam explicitados na documentação. As métricas descrevem o escopo implementado e os resultados das validações.

## Evidências da revisão de governança

Além dos marcos históricos de revisão, a execução local mais recente do **Governed Analytics Platform** em **13/11/2026** registrou **1.353 testes aprovados**, **92% de cobertura total** em `src + app` e **nenhuma falha**. Esse resultado é de validação local e não deve ser interpretado como métrica automática de GitHub Actions/Codecov.

As validações documentadas incluem as seguintes revisões e resultados:

| Projeto | Testes aprovados | Melhoria verificada | Alteração proposta |
|---|---:|---|---|
| Lakehouse | 186 | Seis datasets Silver e quatro tabelas Gold na execução local documentada | [Repositório](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse) |
| Governed Analytics | 1.353 testes · 92% cobertura | Validação local em 13/11/2026 sem falhas; histórico anterior em 31/10/2026 registrou 1.111 testes | [Repositório](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) |
| Central de Automação | 27 | Bloqueio de inconsistências antes da publicação | [PR #1](https://github.com/samuelmaia-analytics/central-automacao-operacoes/pull/1) |

Os números são históricos e se referem às validações registradas em cada projeto; não foram reexecutados durante esta atualização do perfil. A execução em Azure Databricks permanece prevista, não validada em nuvem.

Os projetos são pessoais e independentes da atuação na Avanade; não representam entregas ou dados da empresa e de seus clientes.

## Formação

- Pós-graduação em Inovação e Transformação Digital — Gran Faculdade | out/2026
- Pós-graduação em Ciência de Dados — Gran Faculdade | abr/2026
- Bacharelado em Administração — FAEL | jul/2024
- AWS re/Start, Inteligência Artificial e No Code — Escola da Nuvem | 270h | jul/2026
- Curso preparatório para **Databricks Certified Data Engineer Associate** — Udemy, 13,5h | out/2026. Certificado de conclusão do curso (curso preparatório; não é a certificação obtida).

## Contato profissional

Fortaleza/CE · [E-mail](mailto:samuelmaia.carreira@gmail.com) · [LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/)
