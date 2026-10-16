# Privacidade e publicação

A distribuição contém método, catálogos e exemplos explicitamente fictícios. Não copie o workspace de origem, seu histórico Git, arquivos importados ou configurações autenticadas.

Dados criados no uso ficam em `workspace/` e `.local/`, ignorados pelo Git do kit. Isso não criptografa os arquivos e não impede backup ou sincronização pelo sistema operacional. ZIPs criados manualmente podem incluir arquivos ignorados: revise o conteúdo ou exporte apenas os arquivos versionados.

Antes de publicar alterações no método, confira `git status`, o diff e os arquivos preparados para commit. Não use `git add -f` para incluir a área pessoal. O validador verifica links e alguns padrões de credencial; não é uma auditoria completa de segredos ou de privacidade.

Conecte apenas os recursos necessários, conhecendo as permissões reais. Não grave tokens, chaves, dumps, cookies, logs completos ou transcrições desnecessárias. Registre “autenticação confirmada”, sem o valor da credencial.

Para guardar registros pessoais no Git, escolha separadamente um repositório privado e revise o que vai entrar. Alterar a visibilidade de um repositório ou compartilhar uma pasta é uma decisão própria, com revisão do conteúdo.
