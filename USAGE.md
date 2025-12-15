# Guia de Uso — AutoOrganizer

Este guia detalha as opções e fluxos de uso da aplicação AutoOrganizer.

## Modi operandi
- Simulação (simulate): mostra o que seria feito sem alterar arquivos. Use sempre primeiro.
- Backup: se habilitado e se não for upload, cria uma pasta `_backup_` dentro da pasta dos arquivos e move o original para lá antes de mover/renomear.

## Cenários de uso comuns

1) Organizar downloads
- Abrir app local.
- Inserir o caminho da pasta de Downloads.
- Selecionar "Organizar por extensão".
- Gerar pré-visualização.
- Se OK, desmarcar "Simular" e executar.

2) Renomear fotos
- Selecionar "Renomear com padrão".
- Definir prefixo, sufixo e marcar/desmarcar opções.
- Gerar pré-visualização.
- Executar (com backup se desejar).

3) Teste rápido sem tocar em disco do usuário
- Use a opção "Upload" para enviar alguns arquivos e testar a lógica sem afetar sua pasta local.

## Solução de problemas
- App não encontra arquivos ao fornecer caminho: verifique permissões e se o caminho está correto.
- Erros ao mover arquivos: verifique se outro processo não está bloqueando os arquivos.
- Permissões no Windows: execute o terminal como administrador se necessário.

## Extensões e melhorias sugeridas
- Integração com filtros por data/modificação.
- Undo (desfazer) usando o log de backup.
- Interface para regras customizadas (ex.: mover imagens para `Images/` se tamanho < X).

Obrigado por usar AutoOrganizer! Contribuições e sugestões são bem-vindas.