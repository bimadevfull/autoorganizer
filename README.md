# AutoOrganizer ✨

AutoOrganizer é uma aplicação simples feita com Python + Streamlit para automatizar tarefas básicas em arquivos: organizar por extensão e renomear em lote. O app foca em usabilidade e visual agradável, permitindo pré-visualizar as alterações antes de executá-las.

## Recursos
- Organizar arquivos em subpastas por extensão (ex.: `.pdf` → `/pdf/`).
- Renomear arquivos em lote usando prefixo/sufixo e índice (índices com zeros).
- Modo de simulação (preview) para garantir que tudo está correto antes de mudanças.
- Opção de criar backup automático antes de mover/renomear.
- Visual limpo e responsivo com preview em tabela e log de execução.

## Requisitos
- Python 3.8+
- Recomendado rodar localmente (o app precisa de acesso ao sistema de arquivos local para operar pastas).

## Instalação
1. Clone o repositório ou copie os arquivos para uma pasta:
   - git clone <seu-repo>  (ou simplesmente crie a pasta e cole os arquivos)
2. Crie um ambiente virtual (opcional, recomendado):
   - python -m venv .venv
   - Linux/macOS: source .venv/bin/activate
   - Windows (PowerShell): .venv\Scripts\Activate.ps1
3. Instale dependências:
   - pip install -r requirements.txt

## Como rodar
Execute:
```bash
streamlit run streamlit_app.py
```

O Streamlit abrirá no navegador (normalmente http://localhost:8501). Se usar a opção "Pasta local", informe o caminho da pasta que deseja organizar.

## Uso rápido
1. Selecione a ação na barra lateral: "Organizar por extensão" ou "Renomear com padrão".
2. Escolha se usará uma pasta local ou fará upload de arquivos (apenas para testes rápidos).
3. Clique em "Gerar pré-visualização" para ver o plano de alterações.
4. Se estiver satisfeito, clique em "Executar". Se estiver em modo de simulação, nada será alterado.
5. Baixe o log gerado para conferir o histórico.

## Estrutura do projeto
- `streamlit_app.py` — aplicação principal.
- `requirements.txt` — dependências.
- `docs/USAGE.md` — instruções de uso (detalhadas).
- `scripts/start_local.sh` — script de ajuda para rodar localmente.
- `.gitignore` — arquivos/dirs ignorados.
- `LICENSE` — licença MIT.

## Segurança & Boas práticas
- Sempre teste em modo de simulação primeiro.
- Faça backup dos seus dados importantes antes de rodar o app.
- O modo de upload salva arquivos em pasta temporária para testes sem afetar disco.

## Próximas melhorias sugeridas
- Filtro por data/modificação.
- Suporte a regras customizadas (ex.: mover imagens para Images/).
- Renomeação baseada em metadados (EXIF para fotos).

Licença: MIT
