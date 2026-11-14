# Samuel Maia

**Engenheiro de Dados Pleno na Avanade | Engenharia de Dados, Analytics Engineering e Governança**

Estruturo pipelines e produtos analíticos com foco em qualidade, rastreabilidade e critérios claros de publicação. Minha trajetória combina entendimento de processos e negócio com Python, SQL, dbt, testes automatizados e arquitetura de dados.

Atuo como **Engenheiro de Dados Pleno na Avanade desde outubro de 2026**. Os projetos apresentados neste perfil são iniciativas pessoais, independentes da empresa e de seus clientes.

[Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/) · [LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Currículo em PDF](https://samuelmaia-analytics.github.io/samuelmaia-analytics/assets/Samuel_Maia_Curriculo.pdf)

## Projetos em destaque

### [Governed Analytics Platform](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform)

Dados analíticos sem contratos e verificações podem chegar ao consumo executivo com inconsistências difíceis de rastrear. Desenvolvi uma plataforma demonstrativa em **Python, SQL, dbt e DuckDB** com camadas Bronze, Silver, Gold e Quarantine; contratos YAML, controles de qualidade e privacidade, lineage e **Publication Gate** com decisões explícitas de aprovação, revisão ou bloqueio. Integrei uma interface **Streamlit com visão executiva e navegação organizada**, uma API FastAPI com autenticação Bearer para endpoints sensíveis e um assistente RAG de governança com recuperação TF-IDF local e evidências citadas.

A validação **local de 13/11/2026** registrou **1.353 testes aprovados**, **92% de cobertura em `src + app`** e nenhuma falha. A modernização visual de 14/11/2026 recebeu correção de tipagem e teve CI, lint, segurança, política e workflow de deploy aprovados. As métricas de testes são históricas e não correspondem automaticamente à cobertura medida no CI.

[Explorar o código](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform) · [Abrir Streamlit](https://governed-analytics-platform.streamlit.app/)

### [Azure Databricks Governed Lakehouse](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse)

Pipelines de pedidos e produtos precisam preservar integridade entre ingestão e consumo. Implementei um Lakehouse com **PySpark, Delta Lake e Python**, camadas Raw/Bronze/Silver/Gold/Quarantine, schemas explícitos, reconciliações e controle de publicação. A execução local documentada produziu **seis datasets Silver e quatro tabelas Gold**, com **186 testes automatizados**. A arquitetura tem Azure Databricks como plataforma-alvo; a implantação em nuvem não está comprovada.

[Consultar a implementação e as evidências](https://github.com/samuelmaia-analytics/azure-databricks-governed-lakehouse)

### [Central de Automação e Operações](https://github.com/samuelmaia-analytics/central-automacao-operacoes)

Acompanhar workflows dispersos dificulta identificar atrasos, pendências sem responsável e prioridades. Desenvolvi uma aplicação com **Python, SQL, DuckDB e Streamlit**, integrada ao Pipefy via **API/GraphQL**, que consolida SLA, backlog, alertas e regras de criticidade. O projeto oferece demonstração com dados de exemplo quando a integração não está disponível, sem atribuir ganhos quantitativos não medidos.

[Consultar o repositório](https://github.com/samuelmaia-analytics/central-automacao-operacoes) · [Abrir demonstração](https://central-automacao-operacoes.streamlit.app/)

## Competências técnicas

- **Engenharia de dados:** Python, SQL, PySpark, ETL/ELT, modelagem analítica, dbt, DuckDB, Delta Lake.
- **Qualidade e governança:** Data Contracts, Data Quality, lineage, validações, reconciliação, Publication Gate e controles de privacidade.
- **Aplicações e automação:** Streamlit, FastAPI, Power BI, APIs REST/GraphQL, n8n.
- **Ferramentas e cloud:** Azure Databricks, AWS, Git, GitHub Actions, pytest, Ruff e mypy.
- **IA aplicada:** assistente RAG com TF-IDF local, citações e integração opcional à OpenAI mediante consentimento.

As tecnologias estão distribuídas entre projetos distintos: **PySpark e Delta Lake são utilizados no Lakehouse, não no GAP**.

## Formação

- Pós-graduação em Inovação e Transformação Digital — Gran Faculdade, 2026.
- Pós-graduação em Ciência de Dados — Gran Faculdade, 2026.
- Bacharelado em Administração — FAEL, 2024.
- AWS re/Start — Escola da Nuvem, 2026.

## Outros projetos e contato

Outros estudos e implementações estão disponíveis na [lista de repositórios](https://github.com/samuelmaia-analytics?tab=repositories). Seus escopos, resultados e limitações são descritos nas respectivas documentações.

**Fortaleza, CE** · [LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/) · [E-mail](mailto:samuelmaia.carreira@gmail.com)
