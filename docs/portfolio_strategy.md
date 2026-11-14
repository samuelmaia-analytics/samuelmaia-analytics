# Diretrizes editoriais do portfólio

## Posicionamento

Samuel Maia atua como Engenheiro de Dados Pleno na Avanade. Seus projetos pessoais demonstram capacidade de construir e explicar produtos analíticos com contratos, qualidade, rastreabilidade e critérios de publicação. A experiência corporativa e os experimentos pessoais devem permanecer claramente separados.

## Hierarquia pública

1. **Governed Analytics Platform:** projeto principal; demonstra governança e publicação controlada com evidências de validação local.
2. **Azure Databricks Governed Lakehouse:** especialização complementar em PySpark, Delta Lake e processamento por camadas; execução local comprovada, nuvem como alvo.
3. **Central de Automação e Operações:** integração de APIs e acompanhamento operacional.

Os demais projetos apoiam essa narrativa, sem competir por destaque com os três principais.

## Regras de apresentação

- Começar pelo problema e pelo efeito de resolvê-lo; explicar a implementação e indicar o resultado verificável em linguagem natural.
- Não usar subtítulos artificiais como “Contexto”, “Ação”, “Resultado” ou nomes de métodos dentro das descrições públicas.
- Distinguir implementação de simulação, referência arquitetural e trabalho futuro.
- Não inventar ganhos percentuais, implantação corporativa, certificações ou métricas.
- Sempre contextualizar resultados de testes com data, ambiente e escopo. O resultado do GAP em 13/11/2026 foi local: 1.353 testes, 92% de cobertura em `src + app`.
- Não atribuir PySpark e Delta Lake ao GAP; são do Lakehouse.
- Preferir descrições curtas, links funcionais e capturas de tela reais do produto.
- Unificar conteúdos duplicados em uma fonte principal; manter inglês sincronizado quando existir.
- Não apresentar o perfil como busca de emprego: o profissional está empregado e mantém o portfólio para demonstrar entregas e compartilhar conhecimento.

## Verificações antes de publicar

Conferir README principal, README traduzido, GitHub Pages, links dos projetos, métricas datadas, estado dos workflows, screenshots e arquivo de currículo. Revisar o diff antes de registrar mudanças relacionadas em um único commit por repositório.
