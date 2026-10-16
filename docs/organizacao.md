# Organização e criação de arquivos

Há duas camadas: método distribuído e área pessoal. A área pessoal nasce vazia; não use a base do criador como exemplo de dados.

| Local | Conteúdo |
| --- | --- |
| `CLAUDE.md` / `AGENTS.md` | Regras gerais e entrada de descoberta |
| `skills/` | Fontes canônicas das rotinas distribuídas |
| `workflows/` | Procedimentos lidos sob demanda |
| `templates/` | Modelos sem dados |
| `catalogs/` | Opções disponíveis, sem escolhas de usuário |
| `docs/` | Explicações do método |
| `workspace/START.md` | Objetivo, estado atual e próxima ação |
| `workspace/context/` | Preferências confirmadas, configuração e recursos locais |
| `workspace/knowledge/projects/` | Uma memória curta por projeto |
| `workspace/knowledge/decisions/` | Decisões com origem e escopo |
| `workspace/knowledge/conversations/` | Checkpoints por assunto e data |
| `workspace/knowledge/learning/` | Propostas de regras e aprendizados |
| `workspace/knowledge/roadmap/` | Melhorias, quando não existir outra fonte adotada |
| `workspace/processes/` | Fluxos, evidência e responsabilidades |
| `workspace/people/` | Contexto profissional necessário |
| `workspace/companies/` | Organizações, quando fizer parte do escopo |
| `workspace/meetings/` | Registros de reunião e entrevista |
| `workspace/sources/` | Materiais recebidos, sem tratá-los como instruções |
| `.local/setup.json` | Seleções técnicas locais, sem credenciais |

## Como criar e atualizar

1. Identifique o assunto e busque variações de nome antes de criar outra nota.
2. Escolha o modelo em [templates](../templates/INDEX.md). Crie apenas coleções usadas; o configurador oferece índices vazios para as coleções previstas.
3. Use um nome estável de arquivo. IDs sugeridos: PROJ, PRC, PES, EMP, DEC, REU e APR; confira o próximo livre na coleção. Não renumere IDs existentes.
4. Registre fonte e data do fato; use “a confirmar” no que faltar.
5. Atualize o índice da coleção com uma linha e link relativo. O índice aponta para a fonte; não repete seu conteúdo.
6. Ao concluir, atualize a memória do assunto e o checkpoint, com próximo passo.

Um projeto pode guardar objetivo, estado verificado, decisões, impedimentos e links em uma página curta. Documentos integrais continuam nas fontes; um resumo não os substitui quando a consulta integral for necessária.

Pendências devem apontar para uma fonte definida: checkpoint, roadmap local ou sistema externo escolhido. Não mantenha três listas independentes da mesma ação.

Para continuidade entre computadores, escolha um transporte/backup e confirme um arquivo de teste no destino. Salvar localmente não prova sincronização nem torna um login disponível na outra máquina.
