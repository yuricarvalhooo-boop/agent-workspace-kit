# Conectores opcionais

Um conector permite acessar um serviço; MCP é uma das formas técnicas de disponibilizar esse acesso. O cliente pode oferecer plugins, apps, conectores ou servidores MCP. A disponibilidade depende do ambiente e da conta; nenhuma integração desta tabela vem instalada ou garantida.

| Opção / ID | Para que escolher | Dados e acesso a discutir antes de conectar |
| --- | --- | --- |
| GitHub / `github` | Consultar repositórios, issues e PRs | Quais repositórios; leitura ou também escrita |
| Arquivos e documentos / `documents` | Consultar Drive, OneDrive, SharePoint ou outro acervo | Qual serviço, conta, pasta/arquivo; leitura ou edição |
| Agenda / `calendar` | Preparar o dia e reuniões | Qual conta/calendário; consulta ou criação de eventos |
| Email / `email` | Consultar mensagens relevantes | Qual conta e escopo; envio exige ação autorizada |
| Mensagens / `messaging` | Consultar conversas de trabalho | Qual serviço/canal; enviar exige ação autorizada |
| Gestão de tarefas / `tasks` | Trabalhar com issues, quadros e tarefas existentes | Qual sistema/projeto; consulta ou alteração |
| Documentação oficial / `docs` | Consultar referências técnicas atuais | Qual fornecedor; MCP ou busca oficial se disponível |
| Serviço próprio / `custom` | Acessar uma API necessária à rotina | URL, dono, autenticação, operações e escopo a definir |

Começar com **nenhum conector** é uma opção completa. Arquivos fornecidos manualmente continuam funcionando.

## Roteiro de conexão

1. Descubra o sistema realmente usado e a tarefa concreta. Registre serviço, conta identificada apenas pelo necessário, finalidade e acesso desejado.
2. Verifique se o cliente oferece a integração. Se faltar, explique as alternativas, incluindo continuar sem ela. Não invente ferramenta disponível.
3. Confira documentação oficial atual, fornecedor, dependências, preço/conta quando aplicável e permissões reais. Preferência de leitura no kit não restringe tecnicamente um token amplo.
4. Depois da escolha, conduza login e consentimento pelo mecanismo oficial. Não peça tokens no chat ou nos arquivos versionados. Não copie configurações autenticadas de outra máquina.
5. Faça uma leitura pequena autorizada de um recurso escolhido. Registre resultado, limites e data; só então marque “verificado”.
6. Para ações de escrita/envio, use autorização compatível com a ação. A conexão por si só não concede essa autorização.

Estados: não escolhido → selecionado → autenticação pendente → conectado → verificado; ou indisponível / dispensado. Não confunda a lista de escolhas em `.local/setup.json` com conexão real.

## Registro local

Use `workspace/context/setup.md` para o serviço específico, recurso permitido, leitura/escrita, estado confirmado e próximo passo. Não registre segredos nem um inventário da conta inteira.

A configuração técnica varia por cliente. Consulte [MCP no Codex](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) ou a documentação oficial do cliente escolhido no momento de conectar. O kit não grava configurações MCP ou OAuth automaticamente.
