# Instalações por escolha

O núcleo são arquivos Markdown. Para automação, escolha um agente capaz de acessar a pasta; sem agente, os modelos ainda podem ser usados manualmente. Contas e programas são escolhas diferentes.

| Item / ID no configurador | Finalidade | Quando necessário | Verificação sem instalar | Fonte |
| --- | --- | --- | --- | --- |
| Codex / escolha de agente `codex` | Trabalhar com arquivos e tarefas pelo agente | Se for o cliente escolhido | Confirmar o app/cliente atual; CLI: `codex --version`, se usada | [Início oficial](https://learn.chatgpt.com/docs/quickstart) |
| Claude Code / agente `claude` | Alternativa de agente para a mesma estrutura | Se for o cliente escolhido | `claude --version`, quando aplicável | [Início oficial](https://code.claude.com/docs/en/overview) |
| Editor / `editor` | Ler e editar Markdown | Só se faltar um editor adequado | Abrir um arquivo de texto | Escolha um editor do seu sistema |
| Git / `git` | Histórico, comparação e reversão | Se quiser versionamento local | `git --version` | [Instalação](https://git-scm.com/install/) |
| GitHub CLI / `gh` | Operar GitHub no terminal | Se escolher a CLI; clonar/enviar Git exige Git | `gh --version` | [Site oficial](https://cli.github.com/) |
| Python / `python` | Executar os três scripts locais | Só para usar os scripts; Python 3.10+ | `python --version`, `python3 --version` ou `py --version` | [Instalação por sistema](https://docs.python.org/3/using/index.html) |
| Node.js/npm / `node` | Executar ferramentas escritas para esse runtime | Apenas se um cliente/MCP escolhido exigir | `node --version` e `npm --version` | [Download oficial](https://nodejs.org/en/download) |
| ripgrep / `rg` | Busca rápida em arquivos | Opcional; a busca Python e o editor substituem | `rg --version` | [Projeto oficial](https://github.com/BurntSushi/ripgrep#installation) |
| Backup/sincronização / `backup` | Cópia e continuidade entre máquinas | Se desejar | Conferir o cliente e um arquivo de teste | Documentação do serviço escolhido |

A conta GitHub não exige instalar a CLI. O kit não exige uma chave de API. O cliente de agente escolhido pode ter requisitos de conta, plano, organização ou cobrança próprios: consulte o fornecedor antes de contratar.

Não há comando universal de instalação neste kit. Após escolher o item e o sistema, consulte a fonte oficial atual, apresente o comando ou instalador apropriado e confirme a execução no escopo escolhido. Nenhum script baixa ou executa instaladores.

## Caminho manual, sem Python

1. Crie `workspace/`, com `START.md`, `context/` e `knowledge/`.
2. Copie [o modelo de configuração](../templates/setup.md) para `workspace/context/setup.md` e preencha apenas escolhas confirmadas.
3. Crie as subpastas que usar conforme [organização](organizacao.md); adicione um `INDEX.md` curto em cada coleção.
4. Para cada skill escolhida, crie `.agents/skills/NOME/SKILL.md` para Codex e/ou `.claude/skills/NOME/SKILL.md` para Claude Code. Preserve `name` e `description` da fonte em `skills/NOME/SKILL.md` e use o corpo abaixo como adaptador.
5. Confirme a descoberta no cliente. Se necessário, inicie uma nova sessão; registre como pendente até confirmar.

Corpo do adaptador (substitua NOME pelo ID escolhido):

```md
Leia a skill canônica em ../../../skills/NOME/SKILL.md e siga suas instruções.
```

Não altere configuração global para ativar uma rotina só neste projeto. O agente também pode ler uma rotina selecionada diretamente, sem adaptador; nesse caso registre uso manual, sem afirmar descoberta automática.

## Scripts opcionais

- `configure.py`: mostra uma prévia; com `--apply`, cria a configuração, área pessoal vazia e adaptadores selecionados. Não instala e não conecta.
- `search.py`: pesquisa somente Markdown de `workspace/`; não acessa nuvem.
- `validate.py`: verifica links locais, catálogo, skills e separação de dados. Não autentica nem testa comportamento de um modelo.

Não existe dependência de pip, servidor, banco, container ou assinatura de integração para rodar esses scripts.
