# Agent Workspace Kit

Um ponto de partida em português para organizar trabalho com agentes: contexto em arquivos, decisões rastreáveis, modelos e rotinas reutilizáveis.

## Comece aqui

1. Baixe este repositório como ZIP e extraia, ou clone com Git.
2. Abra a pasta em um agente com acesso autorizado aos arquivos locais.
3. Envie a mensagem abaixo. Você também pode ler o roteiro e preencher os modelos manualmente.

> Leia AGENTS.md e conduza a PRIMEIRA-CONVERSA.md. Explique as instalações, skills e conectores disponíveis; faça uma pergunta por vez e espere minhas escolhas antes de configurar.

A primeira conversa mostra o que cada ferramenta faz, o que já existe na máquina e o que pode ficar para depois. Você escolhe quais skills ativar, quais criar e quais serviços conectar. Tudo pode começar sem conector e sem instalar Python, Git ou Node.js.

## O que vem no kit

- [Primeira conversa](PRIMEIRA-CONVERSA.md): descoberta e configuração por escolha.
- [Instalações](docs/instalacao.md): necessidade, finalidade e fonte oficial.
- [Skills](docs/skills.md): sete rotinas prontas e roteiro para criar outras.
- [Conectores](docs/conectores.md): opções, acesso e confirmação de funcionamento.
- [Organização](docs/organizacao.md): onde guardar e como relacionar os arquivos.
- [Modelos](templates/INDEX.md) e [roteiros](workflows/INDEX.md).
- Scripts opcionais em Python, sem pacotes externos, para configurar, buscar e validar.
- [Privacidade](docs/privacidade.md) e [origem do material](docs/origem.md).

## Configuração opcional por terminal

Python 3.10 ou superior é necessário apenas para estes scripts. No Windows, use `py` se esse for o comando disponível; em outros ambientes pode ser `python3`.

```sh
python scripts/configure.py --agent codex --skills retomar registrar-sessao
```

Esse comando só mostra uma prévia. Depois de escolher e revisar, acrescente `--apply` para criar a área pessoal e os adaptadores das skills selecionadas. Use `--agent claude`, `both` ou `manual` conforme sua escolha. Sem `--skills`, nenhuma skill é ativada.

```sh
python scripts/validate.py
python scripts/search.py "próximo passo" --limit 5
python -m unittest discover -s tests -v
```

Escolher um conector no configurador registra uma intenção; não instala software, não autentica e não concede acesso a contas.

## Seus registros ficam separados

`workspace/` guarda dados e notas pessoais; `.local/` guarda a configuração local. Ambas são ignoradas pelo Git deste kit. Skills ativadas em `.agents/skills/` e `.claude/skills/` também são locais. A base distribuída chega sem registros de trabalho e sem skills ativadas.

O Git deste repositório versiona o método. Para versionar seus dados, escolha separadamente um repositório privado ou outro backup. Um arquivo ignorado continua no disco e pode ser sincronizado pelo serviço que você usar.

## Distribuição

Este kit não inclui pacotes de plugins nem skills de terceiros instaladas em outra máquina. Links oficiais são referências; cada ferramenta mantém suas próprias condições de uso. Não foi escolhida uma licença de código aberto nesta versão; tornar um repositório público não concede automaticamente permissão de redistribuição. Veja [origem e licença](docs/origem.md).
