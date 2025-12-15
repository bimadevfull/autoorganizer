import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AutoOrganizer ✨",
    page_icon="🧰",
    layout="wide",
)

# ---------- CSS (visual bonito) ----------
CSS = """
<style>
[data-testid="stHeader"] {visibility: hidden;}
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #0b1222 100%);
    color: #E6EEF8;
    font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial;
}
.card {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.04);
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(2,6,23,0.6);
}
.small-muted {
    color: #9fb0d6;
    font-size:12px;
}
.ext-badge {
    background: rgba(255,255,255,0.03);
    color: #9fb0d6;
    padding: 4px 8px;
    border-radius: 8px;
    font-size: 12px;
    margin-right: 6px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------- Header ----------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("## ✨ AutoOrganizer — Automação simples para organizar e renomear arquivos")
    st.markdown("Organize arquivos por extensão, renomeie em lote e visualize antes de executar. Feito com Streamlit para uso local.")
with col2:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=80)

st.markdown("---")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    mode = st.selectbox("Ação", ["Organizar por extensão", "Renomear com padrão"])
    simulate = st.checkbox("Simular somente (preview)", value=True, help="Não faz alterações, apenas mostra o que aconteceria.")
    backup = st.checkbox("Criar backup (mover para pasta _backup_ antes)", value=False)
    keep_originals = st.checkbox("Adicionar sufixo ao renomear em lote (_orig disponível)", value=False)
    st.markdown("---")
    st.markdown("### Entradas")
    use_upload = st.radio("Fonte de arquivos", ("Pasta local (recomendado ao rodar localmente)", "Upload (teste rápido)"))
    folder_path = ""
    if use_upload.startswith("Pasta"):
        folder_path = st.text_input("Caminho da pasta (ex: /home/user/Downloads)", value="")
    uploaded_files = st.file_uploader("Ou faça upload de arquivos (múltiplos)", accept_multiple_files=True)

# ---------- Helper functions ----------
def list_files_from_path(path: str):
    p = Path(path)
    if not p.exists() or not p.is_dir():
        return []
    files = [f for f in p.iterdir() if f.is_file()]
    return files

def prepare_temp_from_uploads(files):
    tmp = Path(tempfile.mkdtemp(prefix="autoorg_"))
    saved = []
    for fu in files:
        target = tmp / fu.name
        with open(target, "wb") as f:
            f.write(fu.getbuffer())
        saved.append(target)
    return tmp, saved

def organize_by_extension(files, base_folder: Path):
    plan = []
    for f in files:
        ext = f.suffix.lower().lstrip(".") or "no_ext"
        target_dir = base_folder / ext
        target_dir.mkdir(parents=True, exist_ok=True)
        new_path = target_dir / f.name
        plan.append((f, new_path))
    return plan

def rename_with_pattern(files, base_folder: Path, prefix="", suffix="", keep_original=False):
    plan = []
    for idx, f in enumerate(files, start=1):
        stem = f.stem
        ext = f.suffix
        # índice formatado com zeros à esquerda
        index = f"{idx:03d}"
        new_name = f"{prefix}{stem}{suffix}{index}{ext}"
        new_path = base_folder / new_name
        plan.append((f, new_path))
    return plan

def execute_plan(plan, simulate=True, backup=False, backup_folder_name="_backup"):
    executed = []
    for src, dest in plan:
        try:
            os.makedirs(dest.parent, exist_ok=True)
            if simulate:
                status = "simulado"
            else:
                if backup:
                    bdir = src.parent / backup_folder_name
                    bdir.mkdir(exist_ok=True)
                    shutil.move(str(src), str(bdir / src.name))
                    shutil.move(str(bdir / src.name), str(dest))
                else:
                    shutil.move(str(src), str(dest))
                status = "feito"
            executed.append({"original": str(src), "destino": str(dest), "status": status})
        except Exception as e:
            executed.append({"original": str(src), "destino": str(dest), "status": f"erro: {e}"})
    return executed

# ---------- Main UI logic ----------
st.markdown("### Preview e Execução")
left, right = st.columns([2, 1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 1) Fonte de arquivos")
    files = []
    tmp_dir = None
    if use_upload.startswith("Pasta"):
        st.markdown("Pasta local:" if folder_path else "Digite o caminho de uma pasta local para processar arquivos.")
        folder_path = st.text_input("Caminho da pasta", value=folder_path, key="folder_path_input")
        if folder_path:
            files = list_files_from_path(folder_path)
        else:
            files = []
    else:
        if uploaded_files:
            tmp_dir, saved_files = prepare_temp_from_uploads(uploaded_files)
            files = saved_files
            st.info(f"{len(files)} arquivo(s) salvos em {tmp_dir} para processamento de teste.")
        else:
            files = []

    st.markdown(f"**Arquivos encontrados:** {len(files)}")
    if len(files) > 0:
        sample = [{"nome": f.name, "tamanho (bytes)": f.stat().st_size} for f in files[:50]]
        st.table(pd.DataFrame(sample))

    st.markdown("#### 2) Opções específicas")
    if mode == "Renomear com padrão":
        prefix = st.text_input("Prefixo", value="novo_")
        suffix = st.text_input("Sufixo (antes do índice)", value="_")
    else:
        prefix = suffix = ""

    st.markdown("#### 3) Pré-visualizar plano")
    if st.button("Gerar pré-visualização"):
        base = Path(folder_path) if folder_path else (tmp_dir if tmp_dir else Path.cwd())
        if not files:
            st.warning("Nenhum arquivo para pré-visualizar.")
        else:
            if mode == "Organizar por extensão":
                plan = organize_by_extension(files, base)
            else:
                plan = rename_with_pattern(files, base, prefix=prefix, suffix=suffix, keep_original=keep_originals)
            df = pd.DataFrame([{"original": str(a), "destino": str(b)} for a,b in plan])
            st.dataframe(df)
            st.session_state["plan"] = plan
            st.success("Pré-visualização gerada. Confira antes de executar.")

    st.markdown("#### 4) Executar plano")
    if st.button("Executar"):
        if "plan" not in st.session_state:
            st.error("Gere a pré-visualização primeiro.")
        else:
            plan = st.session_state["plan"]
            with st.spinner("Executando..."):
                executed = execute_plan(plan, simulate=simulate, backup=backup)
            df2 = pd.DataFrame(executed)
            st.dataframe(df2)
            st.success("Operação finalizada.")
            # log
            log_lines = [f"{datetime.now().isoformat()} - {row['original']} -> {row['destino']} ({row['status']})" for row in executed]
            st.download_button("Baixar log (.txt)", data="\n".join(log_lines), file_name="autoorganizer_log.txt", mime="text/plain")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Resumo rápido")
    st.metric("Arquivos", len(files), delta=None)
    st.markdown("#### Ações disponíveis")
    st.markdown("- Organizar por extensão (mover para subpastas por extensão)")
    st.markdown("- Renomear em lote com padrão + índice")
    st.markdown("#### Dicas")
    st.markdown("<div class='small-muted'>• Rode este app localmente (streamlit run streamlit_app.py) para que ele tenha acesso ao seu sistema de arquivos.<br>• Use a simulação primeiro para evitar mudanças indesejadas.<br>• Faça backup se quiser manter cópias.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
