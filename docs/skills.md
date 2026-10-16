# Escolha e criação de skills

Uma skill descreve uma rotina reutilizável. Ela não instala ferramentas, não conecta contas e não autoriza publicação. O catálogo em [options.json](../catalogs/options.json) contém os IDs aceitos pelo configurador.

| Skill | Use quando | Saída |
| --- | --- | --- |
| `retomar` | Continuar um assunto ou trocar de agente/máquina | Objetivo, estado com evidência e próximo passo |
| `registrar-sessao` | Salvar um resultado durável ou passagem de trabalho | Fonte atualizada e checkpoint curto |
| `processar-reuniao` | Receber reunião, entrevista ou material | Fatos, decisões, compromissos e lacunas nas fontes |
| `mapear-processo` | Entender como um trabalho acontece | Fluxo atual, evidências, exceções e responsabilidades |
| `mapear-pessoas` | Documentar interfaces profissionais | Perfis confirmados e relações sem duplicação |
| `planejar-periodo` | Preparar dia, semana ou acompanhamento | Prioridades confirmadas, bloqueios e pauta |
| `revisar-contexto` | Revisar fontes e estados antigos | Divergências, atualizações e índices coerentes |

Sugestões para começar, sempre sujeitas à escolha: continuidade → retomar + registrar-sessao; reuniões → processar-reuniao; descoberta → mapear-processo. Nenhuma é obrigatória.

## Criar uma skill própria

Comece por uma rotina que se repete. Exemplos de ideias: investigar falhas antes de editar, corrigir um bug com prova da regressão, revisar uma mudança, preparar uma homologação ou produzir um relatório. São ideias para desenhar com o usuário; não são pacotes incluídos nem dependem de um fornecedor.

Pergunte uma coisa por vez: qual problema; qual pedido deve ativar a rotina; entradas; saída verificável; quais arquivos e sistemas pode acessar; ações que exigem autorização. Use [o modelo de skill](../templates/skill.md) como apoio.

Antes de criar outra, confira se uma skill selecionada já cobre a necessidade. Mostre nome, descrição, saída e limites. Quando o usuário escolher a criação, escreva `skills/nome-da-rotina/SKILL.md` com frontmatter `name` e `description` e instruções curtas. Use minúsculas, números e hífens; pasta e nome devem coincidir. Acrescente referências/scripts apenas se necessários.

Uma skill personalizada que contenha contexto real pertence à área pessoal, por exemplo `workspace/skills/`, e não deve entrar no Git do método. Sua ativação local pode apontar para essa fonte. O configurador cobre apenas as sete opções distribuídas; para skills próprias, crie o adaptador após a escolha e valide os caminhos. Use escopo local, sem sobrescrever skills globais.

Confirme o funcionamento com um pedido representativo e dados fictícios ou autorizados. Um validador de frontmatter não prova o comportamento do agente. Não copie pacotes de terceiros sem conferir licença, dependências e permissões.
