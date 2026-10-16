# Primeira conversa: monte seu próprio modo de trabalhar

Este é um roteiro para o agente conduzir com um novo usuário. Apresente escolhas; não execute instalações ou conecte serviços antes da escolha correspondente. “Depois” e “nenhum” são respostas válidas.

## Abertura obrigatória

Explique em linguagem simples:

> Esta pasta é um kit de organização. Você escolhe o que quer usar. Primeiro vou mostrar para que serve cada ferramenta; depois escolhemos suas rotinas e integrações. Podemos começar apenas com os arquivos e um agente que consiga trabalhar nesta pasta.

Na primeira resposta, apresente a tabela resumida abaixo. Não comece executando o configurador.

| Opção | Para que serve | Precisa instalar agora? |
| --- | --- | --- |
| Um agente com acesso a arquivos, como Codex ou Claude Code | Conversar e manter os arquivos com sua autorização | Só se você ainda não tiver um ambiente adequado; escolha um |
| Editor de texto | Ler e editar Markdown manualmente | Use o que já possui; editor extra é opcional |
| Git | Histórico local e recuperação de versões | Opcional |
| Conta GitHub | Guardar um repositório remoto e compartilhar o kit | Opcional; é conta, não programa |
| GitHub CLI (`gh`) | Operar repositórios e issues pelo terminal | Só se escolher esse modo de uso |
| Python 3.10+ | Executar a configuração, busca e validação deste kit | Opcional; existe caminho manual |
| Node.js/npm | Executar uma ferramenta ou servidor que realmente dependa deles | Só diante dessa dependência; o kit não depende |
| ripgrep (`rg`) | Buscar texto rapidamente | Opcional; há alternativas |
| Cliente de backup/sincronização | Levar arquivos a outro equipamento ou manter cópias | Opcional; escolha destino e escopo |

Mostre também que há sete skills prontas de organização e conectores opcionais de arquivos, código, agenda e comunicação. Explique que uma skill ensina uma rotina e um conector dá acesso a um sistema; escolher uma coisa não exige a outra.

Faça apenas a próxima pergunta:

> Em qual sistema você vai usar este kit, e já está usando algum agente? Pode responder, por exemplo, “Windows e Codex” ou “ainda não escolhi”.

## Descoberta e instalações

1. Identifique o ambiente e o que a pessoa quer organizar primeiro. Pergunte um assunto por vez: projetos, reuniões, processos, estudos ou desenvolvimento; aceite outros.
2. Consulte [instalações](docs/instalacao.md). Se houver terminal, faça apenas verificações de presença/versão relevantes, sem instalar. Sem acesso, informe “não verificado”.
3. Monte uma tabela com ferramenta, finalidade para o caso da pessoa, estado atual, necessidade e decisão: usar existente / instalar / depois / não usar.
4. Recomende o menor conjunto suficiente e pergunte o que a pessoa quer instalar. Apresente custo/acesso como “verificar no fornecedor” quando desconhecido; não presuma assinatura, licença corporativa ou necessidade de API paga.
5. Para cada item escolhido, consulte a documentação oficial atual do sistema operacional, explique as alterações e execute dentro do escopo autorizado. Não instalar Node, Git ou uma CLI apenas por aparecerem no catálogo.
6. Login, compra, consentimento e permissões administrativas ficam na interface oficial. Se houver bloqueio, registre o ponto exato e continue o que for independente.

A primeira conversa serve também para quem não instala nada: o agente pode criar os arquivos manualmente, ou a pessoa pode preencher os modelos num editor.

## Escolha das skills

Mostre as sete opções em [skills](docs/skills.md), com o resultado que cada uma produz. Sugira apenas as que resolvem o primeiro caso escolhido. Pergunte quais a pessoa quer ativar, deixar para depois ou dispensar. Aceite seleção vazia.

Depois pergunte se ela quer criar alguma skill própria. Descubra uma rotina concreta, quando deve disparar, entradas, saída, arquivos/sistemas envolvidos e limite de ação. Mostre a proposta e implemente quando escolhida. Não importe skills de plugins ou de outra instalação sem conferir origem e condições de uso.

As skills prontas estão em `skills/`, fora das pastas de descoberta automática. Ative apenas as selecionadas; o configurador pode criar os adaptadores locais. Uma escolha salva não prova carregamento: confirme no cliente ou registre a validação pendente.

## Escolha dos conectores

Leia [conectores](docs/conectores.md). Pergunte onde já está a informação útil; ofereça apenas opções pertinentes e mantenha a opção “nenhum agora”. Para cada opção escolhida, explique finalidade, dados expostos, leitura/escrita, conta necessária e eventuais dependências.

Registre a escolha como “selecionado”. Só marque “conectado” depois de autenticação confirmada e “verificado” depois de uma leitura pequena autorizada. Não leia a conta inteira para testar. Nunca peça credencial no chat. Se o cliente oferecer acesso maior que o necessário, explique o acesso real antes do consentimento; a preferência “somente leitura” no kit não altera as permissões técnicas do fornecedor.

Escolher GitHub não exige Google Drive; escolher uma skill de reunião não exige email, calendário ou mensagens. Cada decisão é independente.

## Materialize e teste a configuração escolhida

- Use [o modelo de configuração](templates/setup.md) para guardar respostas e pendências em `workspace/context/setup.md`.
- Com Python disponível, apresente a prévia de `scripts/configure.py` com apenas os IDs escolhidos do [catálogo](catalogs/options.json). `--tools` e `--connectors` registram escolhas; não executam instalação ou conexão. Depois da aprovação das escolhas, use `--apply`.
- Sem Python, siga [o caminho manual](docs/instalacao.md). Registre as mesmas escolhas; não invente uma etapa instalada.
- Preencha `workspace/START.md` com objetivo e próximo passo. Registre capacidades confirmadas, pendentes e dispensadas, separadamente.
- Faça uma tarefa pequena escolhida pela pessoa: por exemplo, criar uma memória de projeto fictício e retomar o próximo passo. Se houver Python, rode `python scripts/validate.py`.
- Só considere o início concluído quando a pessoa souber onde estão seus arquivos e houver um próximo passo. Pendências opcionais não bloqueiam o uso.

## Retomada

Leia a configuração local e o registro manual; continue da última escolha pendente. Não reinstale, não recrie adaptadores e não reinicie o questionário porque o agente mudou. O configurador preserva arquivos existentes e recusa sobrescrita conflitante.

Ao encerrar, entregue: o que foi escolhido, o que foi realmente instalado/ativado/conectado, o que falta, onde ficou salvo e um próximo passo. Não transforme seleções em resultados executados.
