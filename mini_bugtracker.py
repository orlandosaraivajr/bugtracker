import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import datetime
import os

# ─────────────────────────────────────────────
#  DATABASE
# ─────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bugs.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bugs (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo              TEXT NOT NULL,
                descricao           TEXT NOT NULL,
                projeto             TEXT NOT NULL,
                prioridade          TEXT NOT NULL,
                severidade          TEXT NOT NULL DEFAULT 'Media',
                status              TEXT NOT NULL DEFAULT 'Aberto',
                ambiente            TEXT,
                passos              TEXT,
                resultado_esperado  TEXT,
                resultado_obtido    TEXT,
                frequencia          TEXT DEFAULT 'Sempre (100%)',
                tipo_defeito        TEXT DEFAULT 'Logica',
                reportado_por       TEXT,
                responsavel         TEXT,
                criado_em           TEXT NOT NULL,
                atualizado_em       TEXT,
                fechado_em          TEXT,
                notas_fechamento    TEXT
            )
        """)
        # migração para banco existente
        cols = [r[1] for r in conn.execute("PRAGMA table_info(bugs)").fetchall()]
        migrate = {
            "severidade":        "TEXT NOT NULL DEFAULT 'Media'",
            "ambiente":          "TEXT",
            "passos":            "TEXT",
            "resultado_esperado":"TEXT",
            "resultado_obtido":  "TEXT",
            "frequencia":        "TEXT DEFAULT 'Sempre (100%)'",
            "tipo_defeito":      "TEXT DEFAULT 'Logica'",
        }
        for col, defn in migrate.items():
            if col not in cols:
                conn.execute(f"ALTER TABLE bugs ADD COLUMN {col} {defn}")


def inserir_bug(titulo, descricao, projeto, prioridade, severidade,
                ambiente, passos, resultado_esperado, resultado_obtido,
                frequencia, tipo_defeito, reportado_por, responsavel):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO bugs
              (titulo,descricao,projeto,prioridade,severidade,status,
               ambiente,passos,resultado_esperado,resultado_obtido,
               frequencia,tipo_defeito,reportado_por,responsavel,
               criado_em,atualizado_em)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (titulo, descricao, projeto, prioridade, severidade, "Aberto",
              ambiente, passos, resultado_esperado, resultado_obtido,
              frequencia, tipo_defeito, reportado_por, responsavel, agora, agora))


def atualizar_bug(bug_id, titulo, descricao, projeto, prioridade, severidade,
                  ambiente, passos, resultado_esperado, resultado_obtido,
                  frequencia, tipo_defeito, reportado_por, responsavel):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_conn() as conn:
        conn.execute("""
            UPDATE bugs SET titulo=?,descricao=?,projeto=?,prioridade=?,
              severidade=?,ambiente=?,passos=?,resultado_esperado=?,
              resultado_obtido=?,frequencia=?,tipo_defeito=?,
              reportado_por=?,responsavel=?,atualizado_em=?
            WHERE id=?
        """, (titulo, descricao, projeto, prioridade, severidade,
              ambiente, passos, resultado_esperado, resultado_obtido,
              frequencia, tipo_defeito, reportado_por, responsavel, agora, bug_id))


def mudar_status(bug_id, novo_status, notas=None):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    fechado = agora if novo_status == "Fechado" else None
    with get_conn() as conn:
        if notas is not None:
            conn.execute("""UPDATE bugs SET status=?,atualizado_em=?,
                fechado_em=?,notas_fechamento=? WHERE id=?""",
                (novo_status, agora, fechado, notas, bug_id))
        else:
            conn.execute("""UPDATE bugs SET status=?,atualizado_em=?,
                fechado_em=COALESCE(?,fechado_em) WHERE id=?""",
                (novo_status, agora, fechado, bug_id))


def reabrir_bug(bug_id):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_conn() as conn:
        conn.execute("""UPDATE bugs SET status='Aberto',fechado_em=NULL,
            notas_fechamento=NULL,atualizado_em=? WHERE id=?""", (agora, bug_id))


def deletar_bug(bug_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM bugs WHERE id=?", (bug_id,))


def listar_bugs(filtro_status=None, filtro_projeto=None,
                filtro_severidade=None, busca=None):
    q = "SELECT * FROM bugs WHERE 1=1"
    p = []
    if filtro_status and filtro_status != "Todos":
        q += " AND status=?"; p.append(filtro_status)
    if filtro_projeto and filtro_projeto != "Todos":
        q += " AND projeto=?"; p.append(filtro_projeto)
    if filtro_severidade and filtro_severidade != "Todos":
        q += " AND severidade=?"; p.append(filtro_severidade)
    if busca:
        q += " AND (titulo LIKE ? OR descricao LIKE ?)"
        p += [f"%{busca}%", f"%{busca}%"]
    q += " ORDER BY id DESC"
    with get_conn() as conn:
        return conn.execute(q, p).fetchall()


def get_projetos():
    with get_conn() as conn:
        return [r[0] for r in conn.execute(
            "SELECT DISTINCT projeto FROM bugs ORDER BY projeto").fetchall()]


def get_bug(bug_id):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM bugs WHERE id=?", (bug_id,)).fetchone()


def stats():
    with get_conn() as conn:
        def n(q): return conn.execute(q).fetchone()[0]
        return {
            "total":    n("SELECT COUNT(*) FROM bugs"),
            "aberto":   n("SELECT COUNT(*) FROM bugs WHERE status='Aberto'"),
            "analise":  n("SELECT COUNT(*) FROM bugs WHERE status='Em analise'"),
            "correcao": n("SELECT COUNT(*) FROM bugs WHERE status='Em correcao'"),
            "verif":    n("SELECT COUNT(*) FROM bugs WHERE status='Verificado'"),
            "fechado":  n("SELECT COUNT(*) FROM bugs WHERE status='Fechado'"),
            "critico":  n("SELECT COUNT(*) FROM bugs WHERE severidade='Critica' AND status!='Fechado'"),
        }


# ─────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────
BG       = "#0d1117"
SURFACE  = "#161b22"
SURFACE2 = "#21262d"
BORDER   = "#30363d"
ACCENT   = "#f78166"
ACCENT2  = "#56d364"
ACCENT3  = "#e3b341"
ACCENT4  = "#58a6ff"
ACCENT5  = "#bc8cff"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"
TEXT_MUT = "#484f58"

PRIORIDADES  = ["Critica", "Alta", "Media", "Baixa"]
SEVERIDADES  = ["Critica", "Alta", "Media", "Baixa"]
TIPOS        = ["Logica", "Interface", "Desempenho", "Seguranca",
                "Integracao", "Dados", "Outro"]
FREQUENCIAS  = ["Sempre (100%)", "Frequente (~75%)",
                "Ocasional (~50%)", "Raro (~10%)"]
STATUS_LIST  = ["Aberto", "Em analise", "Em correcao", "Verificado", "Fechado"]
STATUS_LABEL = {
    "Aberto":      "Aberto",
    "Em analise":  "Em análise",
    "Em correcao": "Em correção",
    "Verificado":  "Verificado",
    "Fechado":     "Fechado",
}
PROJETOS_SUGERIDOS = ["Calculadora Notas", "Backend", "Frontend", "Mobile", "DevOps", "QA", "Docs"]

PRIO_COLORS = {
    "Critica": "#f85149",
    "Alta":    "#e3b341",
    "Media":   "#58a6ff",
    "Baixa":   "#56d364",
}
STATUS_COLORS = {
    "Aberto":      "#f78166",
    "Em analise":  "#e3b341",
    "Em correcao": "#bc8cff",
    "Verificado":  "#58a6ff",
    "Fechado":     "#56d364",
}
STATUS_NEXT = {
    "Aberto":      "Em analise",
    "Em analise":  "Em correcao",
    "Em correcao": "Verificado",
    "Verificado":  "Fechado",
}

FONT_MONO   = ("Courier New", 10)
FONT_MONO_S = ("Courier New", 9)
FONT_BODY   = ("Courier New", 11)
FONT_SMALL  = ("Courier New", 9)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def _combo_style():
    s = ttk.Style()
    try: s.theme_use("default")
    except: pass
    s.configure("Dark.TCombobox",
        fieldbackground=SURFACE2, background=SURFACE2,
        foreground=TEXT_PRI, selectbackground=BORDER,
        selectforeground=TEXT_PRI, arrowcolor=TEXT_SEC, borderwidth=0)


def styled_btn(parent, text, cmd, color=ACCENT, **kw):
    b = tk.Button(parent, text=text, command=cmd,
        bg=color, fg=BG, font=("Courier New", 10, "bold"),
        relief="flat", cursor="hand2",
        activebackground=TEXT_PRI, activeforeground=BG,
        padx=14, pady=6, bd=0, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=TEXT_PRI))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b


def ghost_btn(parent, text, cmd, **kw):
    b = tk.Button(parent, text=text, command=cmd,
        bg=SURFACE2, fg=TEXT_SEC, font=("Courier New", 10),
        relief="flat", cursor="hand2",
        activebackground=BORDER, activeforeground=TEXT_PRI,
        padx=12, pady=5, bd=0, **kw)
    b.bind("<Enter>", lambda e: b.config(fg=TEXT_PRI, bg=BORDER))
    b.bind("<Leave>", lambda e: b.config(fg=TEXT_SEC, bg=SURFACE2))
    return b


def mk_entry(parent, width=40):
    return tk.Entry(parent, width=width,
        bg=SURFACE2, fg=TEXT_PRI, insertbackground=TEXT_PRI,
        font=FONT_BODY, relief="flat",
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=ACCENT4, bd=4)


def mk_text(parent, width=55, height=4):
    return tk.Text(parent, width=width, height=height,
        bg=SURFACE2, fg=TEXT_PRI, insertbackground=TEXT_PRI,
        font=FONT_BODY, relief="flat",
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=ACCENT4, bd=4, wrap="word", spacing1=2, spacing3=2)


def mk_combo(parent, values, width=20, editable=False):
    _combo_style()
    c = ttk.Combobox(parent, values=values, width=width,
        font=FONT_BODY, style="Dark.TCombobox",
        state="normal" if editable else "readonly")
    c.option_add("*TCombobox*Listbox.background", SURFACE2)
    c.option_add("*TCombobox*Listbox.foreground", TEXT_PRI)
    c.option_add("*TCombobox*Listbox.selectBackground", ACCENT4)
    c.option_add("*TCombobox*Listbox.font", FONT_BODY)
    return c


def mk_label(parent, text, color=TEXT_PRI, size=10, bold=False, **kw):
    return tk.Label(parent, text=text, bg=parent["bg"],
        fg=color, font=("Courier New", size, "bold" if bold else "normal"), **kw)


def mk_frame(parent, bg=SURFACE, **kw):
    return tk.Frame(parent, bg=bg, **kw)


def get_text(w): return w.get("1.0", "end").strip()
def set_text(w, v):
    w.delete("1.0", "end")
    w.insert("1.0", v or "")


def scrolled_canvas(parent, bg=BG):
    """Returns (canvas, inner_frame) with vertical scrollbar."""
    outer = mk_frame(parent, bg=bg)
    outer.pack(fill="both", expand=True)
    canvas = tk.Canvas(outer, bg=bg, bd=0, highlightthickness=0)
    sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner = mk_frame(canvas, bg=bg)
    inner.bind("<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    canvas.bind_all("<MouseWheel>",
        lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
    return canvas, inner


# ─────────────────────────────────────────────
#  FORMULÁRIO COMPLETO DE BUG
# ─────────────────────────────────────────────
class BugForm(tk.Toplevel):
    def __init__(self, master, on_save, bug=None):
        super().__init__(master)
        self.on_save = on_save
        self.bug     = bug
        editing      = bug is not None

        self.title("Editar Bug" if editing else "Novo Bug")
        self.configure(bg=BG)
        self.resizable(True, True)

        # cabeçalho
        head = mk_frame(self, bg=SURFACE)
        head.pack(fill="x")
        tk.Frame(head, bg=ACCENT4 if editing else ACCENT, height=3).pack(fill="x")
        tk.Label(head,
            text="  ✎ EDITAR BUG" if editing else "  ◆ REGISTRAR BUG",
            bg=SURFACE, fg=ACCENT4 if editing else ACCENT,
            font=("Courier New", 14, "bold"), anchor="w", pady=10
        ).pack(fill="x", padx=16)

        # corpo scrollável
        _, self.body = scrolled_canvas(self, bg=BG)

        self._build_fields()
        if editing:
            self._populate(bug)

        # rodapé botões
        foot = mk_frame(self, bg=BG)
        foot.pack(fill="x", padx=20, pady=(4, 14))
        ghost_btn(foot, "✕  Cancelar", self.destroy).pack(side="right", padx=(6, 0))
        cor = ACCENT4 if editing else ACCENT
        styled_btn(foot,
            "✔  Salvar Alterações" if editing else "✔  Registrar Bug",
            self._save, color=cor).pack(side="right")

        self._center()
        self.grab_set()

    # ── helpers internos ─────────────────────
    def _sec(self, title):
        f = mk_frame(self.body, bg=BG)
        f.pack(fill="x", padx=20, pady=(14, 2))
        tk.Frame(f, bg=ACCENT4, width=3).pack(side="left", fill="y")
        tk.Label(f, text=f"  {title}", bg=BG, fg=ACCENT4,
            font=("Courier New", 9, "bold")).pack(side="left")
        tk.Frame(self.body, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 2))

    def _field(self, label_text, widget):
        r = mk_frame(self.body, bg=BG)
        r.pack(fill="x", padx=20, pady=3)
        mk_label(r, label_text, color=TEXT_SEC, size=9).pack(anchor="w")
        widget.pack(fill="x", pady=(2, 0))
        return widget

    def _two_col(self):
        r = mk_frame(self.body, bg=BG)
        r.pack(fill="x", padx=20, pady=3)
        left  = mk_frame(r, bg=BG)
        right = mk_frame(r, bg=BG)
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        right.pack(side="left", fill="x", expand=True)
        return left, right

    def _three_col(self):
        r = mk_frame(self.body, bg=BG)
        r.pack(fill="x", padx=20, pady=3)
        c1 = mk_frame(r, bg=BG); c2 = mk_frame(r, bg=BG); c3 = mk_frame(r, bg=BG)
        for c in (c1, c2, c3):
            c.pack(side="left", fill="x", expand=True, padx=(0, 6))
        return c1, c2, c3

    def _lf(self, parent, text):
        mk_label(parent, text, color=TEXT_SEC, size=9).pack(anchor="w")

    def _build_fields(self):
        p = self.body

        # ── IDENTIFICAÇÃO ────────────────────
        
        self._sec("IDENTIFICAÇÃO")
        self.e_titulo = self._field("TÍTULO  *", mk_entry(p, width=72))

        c1, c2 = self._two_col()
        self._lf(c1, "PROJETO  *")
        proj_vals = sorted(set(PROJETOS_SUGERIDOS + get_projetos()))
        self.e_projeto = mk_combo(c1, proj_vals, width=28, editable=True)
        self.e_projeto.pack(fill="x", pady=(2, 0))

        self._lf(c2, "TIPO DE DEFEITO  *")
        self.e_tipo = mk_combo(c2, TIPOS, width=22)
        self.e_tipo.pack(fill="x", pady=(2, 0))

        c1, c2, c3 = self._three_col()
        self._lf(c1, "SEVERIDADE  *")
        self.e_sev = mk_combo(c1, SEVERIDADES, width=16)
        self.e_sev.pack(fill="x", pady=(2, 0))

        self._lf(c2, "PRIORIDADE  *")
        self.e_prio = mk_combo(c2, PRIORIDADES, width=16)
        self.e_prio.pack(fill="x", pady=(2, 0))

        self._lf(c3, "FREQUÊNCIA  *")
        self.e_freq = mk_combo(c3, FREQUENCIAS, width=22)
        self.e_freq.pack(fill="x", pady=(2, 0))

        # ── RESPONSÁVEIS ─────────────────────
        self._sec("RESPONSÁVEIS")
        c1, c2 = self._two_col()
        self._lf(c1, "REPORTADO POR")
        self.e_rep = mk_entry(c1, width=32)
        self.e_rep.pack(fill="x", pady=(2, 0))

        self._lf(c2, "RESPONSÁVEL")
        self.e_resp = mk_entry(c2, width=32)
        self.e_resp.pack(fill="x", pady=(2, 0))

        # ── AMBIENTE ─────────────────────────
        self._sec("AMBIENTE")
        self.e_amb = self._field(
            "Sistema operacional, navegador, versão do software, dispositivo",
            mk_text(p, height=3))

        # ── DESCRIÇÃO DO DEFEITO ──────────────
        self._sec("DESCRIÇÃO DO DEFEITO")
        self.e_desc   = self._field("DESCRIÇÃO GERAL  *", mk_text(p, height=4))
        self.e_passos = self._field(
            "PASSOS PARA REPRODUZIR  * (numere cada passo)", mk_text(p, height=7))
        self.e_esp    = self._field(
            "RESULTADO ESPERADO  *", mk_text(p, height=3))
        self.e_obt    = self._field(
            "RESULTADO OBTIDO  *", mk_text(p, height=3))

        mk_frame(p, bg=BG, height=12).pack()

    def _populate(self, b):
        (bid, titulo, descricao, projeto, prioridade, severidade, status,
         ambiente, passos, res_esp, res_obt, frequencia, tipo,
         rep, resp, criado, atualizado, fechado, notas) = b
        self.e_titulo.insert(0, titulo)
        self.e_projeto.set(projeto)
        self.e_tipo.set(tipo or TIPOS[0])
        self.e_sev.set(severidade or SEVERIDADES[2])
        self.e_prio.set(prioridade)
        self.e_freq.set(frequencia or FREQUENCIAS[0])
        self.e_rep.insert(0, rep or "")
        self.e_resp.insert(0, resp or "")
        set_text(self.e_amb,    ambiente)
        set_text(self.e_desc,   descricao)
        set_text(self.e_passos, passos)
        set_text(self.e_esp,    res_esp)
        set_text(self.e_obt,    res_obt)

    def _center(self):
        w, h = 800, 740
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _save(self):
        titulo  = self.e_titulo.get().strip()
        desc    = get_text(self.e_desc)
        projeto = self.e_projeto.get().strip()
        prio    = self.e_prio.get()
        sev     = self.e_sev.get()
        tipo    = self.e_tipo.get()
        freq    = self.e_freq.get()
        amb     = get_text(self.e_amb)
        passos  = get_text(self.e_passos)
        esp     = get_text(self.e_esp)
        obt     = get_text(self.e_obt)
        rep     = self.e_rep.get().strip()
        resp    = self.e_resp.get().strip()

        if not all([titulo, desc, projeto, prio, sev]):
            messagebox.showwarning("Campos obrigatórios",
                "Preencha: Título, Descrição, Projeto, Severidade e Prioridade.",
                parent=self)
            return

        if self.bug:
            atualizar_bug(self.bug[0], titulo, desc, projeto, prio, sev,
                          amb, passos, esp, obt, freq, tipo, rep, resp)
        else:
            inserir_bug(titulo, desc, projeto, prio, sev,
                        amb, passos, esp, obt, freq, tipo, rep, resp)
        self.on_save()
        self.destroy()


# ─────────────────────────────────────────────
#  DIALOG AVANÇAR STATUS / FECHAR
# ─────────────────────────────────────────────
class MudarStatusDialog(tk.Toplevel):
    def __init__(self, master, bug_id, titulo, novo_status, on_done):
        super().__init__(master)
        self.bug_id     = bug_id
        self.novo_status= novo_status
        self.on_done    = on_done
        self.title(f"Mover para: {STATUS_LABEL[novo_status]}")
        self.configure(bg=BG)
        self.resizable(False, False)

        cor = STATUS_COLORS[novo_status]
        head = mk_frame(self, bg=SURFACE)
        head.pack(fill="x")
        tk.Frame(head, bg=cor, height=3).pack(fill="x")
        tk.Label(head,
            text=f"  → {STATUS_LABEL[novo_status].upper()}",
            bg=SURFACE, fg=cor,
            font=("Courier New", 13, "bold"), anchor="w", pady=10
        ).pack(fill="x", padx=16)

        body = mk_frame(self, bg=BG)
        body.pack(fill="both", padx=20, pady=10)
        mk_label(body, f"Bug #{bug_id} — {titulo[:54]}",
            color=TEXT_SEC, size=9).pack(anchor="w", pady=(0, 8))

        lbl_nota = ("NOTAS DE FECHAMENTO / SOLUÇÃO APLICADA"
                    if novo_status == "Fechado" else
                    "OBSERVAÇÕES (opcional)")
        mk_label(body, lbl_nota, color=TEXT_SEC, size=9).pack(anchor="w")
        self.t_notas = mk_text(body, width=56, height=5)
        self.t_notas.pack(fill="x", pady=(4, 0))

        foot = mk_frame(self, bg=BG)
        foot.pack(fill="x", padx=20, pady=(4, 14))
        ghost_btn(foot, "✕ Cancelar", self.destroy).pack(side="right", padx=(6, 0))
        styled_btn(foot, "✔ Confirmar", self._confirmar, color=cor).pack(side="right")

        self._center()
        self.grab_set()

    def _center(self):
        w, h = 520, 300
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _confirmar(self):
        notas = get_text(self.t_notas) or None
        mudar_status(self.bug_id, self.novo_status, notas)
        self.on_done()
        self.destroy()


# ─────────────────────────────────────────────
#  JANELA DE RELATÓRIO DE BUG
# ─────────────────────────────────────────────
class RelatorioWindow(tk.Toplevel):
    def __init__(self, master, bug_id):
        super().__init__(master)
        self.title("Relatório de Bug")
        self.configure(bg=BG)
        self.resizable(True, True)

        bug = get_bug(bug_id)
        if not bug:
            self.destroy(); return

        (bid, titulo, descricao, projeto, prioridade, severidade, status,
         ambiente, passos, res_esp, res_obt, frequencia, tipo,
         rep, resp, criado, atualizado, fechado, notas) = bug

        cor_sev = PRIO_COLORS.get(severidade, ACCENT4)
        cor_st  = STATUS_COLORS.get(status, TEXT_SEC)

        # cabeçalho
        head = mk_frame(self, bg=SURFACE)
        head.pack(fill="x")
        tk.Frame(head, bg=cor_sev, height=4).pack(fill="x")
        top = mk_frame(head, bg=SURFACE)
        top.pack(fill="x", padx=16, pady=8)
        tk.Label(top, text=f"  RELATÓRIO DE BUG  ·  #{bid}",
            bg=SURFACE, fg=cor_sev,
            font=("Courier New", 13, "bold")).pack(side="left")
        tk.Label(top,
            text=f"  [{STATUS_LABEL.get(status, status)}]",
            bg=SURFACE, fg=cor_st,
            font=("Courier New", 11, "bold")).pack(side="left")

        # área de texto scrollável
        body = mk_frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        self.txt = scrolledtext.ScrolledText(body,
            bg=SURFACE, fg=TEXT_PRI,
            font=("Courier New", 10),
            relief="flat", bd=0, wrap="word",
            selectbackground=ACCENT4, selectforeground=BG,
            insertbackground=TEXT_PRI,
            padx=24, pady=18, spacing1=2, spacing3=5)
        self.txt.pack(fill="both", expand=True)

        # tags de formatação
        self.txt.tag_configure("h",   foreground=ACCENT4,  font=("Courier New", 10, "bold"))
        self.txt.tag_configure("v",   foreground=TEXT_PRI, font=("Courier New", 10))
        self.txt.tag_configure("lbl", foreground=TEXT_SEC, font=("Courier New", 9,  "bold"))
        self.txt.tag_configure("div", foreground=TEXT_MUT, font=("Courier New", 9))
        self.txt.tag_configure("tit", foreground=TEXT_PRI, font=("Courier New", 13, "bold"))
        self.txt.tag_configure("sev", foreground=cor_sev,  font=("Courier New", 10, "bold"))
        self.txt.tag_configure("st",  foreground=cor_st,   font=("Courier New", 10, "bold"))
        self.txt.tag_configure("ok",  foreground=ACCENT2,  font=("Courier New", 10, "italic"))
        self.txt.tag_configure("err", foreground=ACCENT,   font=("Courier New", 10, "italic"))
        self.txt.tag_configure("passo",foreground=TEXT_PRI,font=("Courier New", 10))

        ins = self.txt.insert

        def ln(text="", tag="v"):
            ins("end", text + "\n", tag)

        def sep(char="─", tag="div"):
            ln(char * 70, tag)

        def field(label_text, value, vtag="v"):
            ins("end", f"  {label_text:<26}", "lbl")
            ins("end", f"{value or '—'}\n", vtag)

        # conteúdo do relatório
        ln()
        sep()
        ins("end", f"\n  BUG #{bid}  —  {titulo}\n", "tit")
        sep()
        ln()

        field("STATUS",          STATUS_LABEL.get(status, status), "st")
        field("SEVERIDADE",      severidade,   "sev")
        field("PRIORIDADE",      prioridade,   "sev")
        field("TIPO DE DEFEITO", tipo or "—")
        field("PROJETO",         projeto,      "v")
        field("REPORTADO POR",   rep or "—")
        field("RESPONSÁVEL",     resp or "—")
        field("CRIADO EM",       criado)
        field("ATUALIZADO EM",   atualizado or "—")
        if fechado:
            field("FECHADO EM",  fechado)
        ln()

        # AMBIENTE
        sep()
        ln("  AMBIENTE", "h")
        sep()
        for line in (ambiente or "Não informado").splitlines():
            ln(f"  {line}")
        ln()

        # DESCRIÇÃO
        sep()
        ln("  DESCRIÇÃO", "h")
        sep()
        for line in (descricao or "—").splitlines():
            ln(f"  {line}")
        ln()

        # PASSOS
        sep()
        ln("  PASSOS PARA REPRODUZIR", "h")
        sep()
        if passos:
            for line in passos.splitlines():
                ln(f"  {line}", "passo")
        else:
            ln("  Não informado")
        ln()

        # RESULTADOS
        sep()
        ln("  RESULTADO ESPERADO", "h")
        sep()
        for line in (res_esp or "Não informado").splitlines():
            ln(f"  {line}", "ok")
        ln()

        sep()
        ln("  RESULTADO OBTIDO", "h")
        sep()
        for line in (res_obt or "Não informado").splitlines():
            ln(f"  {line}", "err")
        ln()

        # FREQUÊNCIA
        sep()
        ln("  FREQUÊNCIA DE OCORRÊNCIA", "h")
        sep()
        ln(f"  {frequencia or 'Não informado'}")
        ln()

        # NOTAS DE FECHAMENTO
        if notas:
            sep()
            ln("  NOTAS DE FECHAMENTO / SOLUÇÃO", "h")
            sep()
            for line in notas.splitlines():
                ln(f"  {line}", "ok")
            ln()

        sep()
        ln()

        self.txt.configure(state="disabled")

        # botões
        foot = mk_frame(self, bg=BG)
        foot.pack(fill="x", padx=16, pady=(0, 12))
        ghost_btn(foot, "✕  Fechar", self.destroy).pack(side="right", padx=(6, 0))
        styled_btn(foot, "⎘  Copiar Relatório",
            self._copiar, color=ACCENT4).pack(side="right")

        self._center()
        self.grab_set()

    def _copiar(self):
        self.txt.configure(state="normal")
        conteudo = self.txt.get("1.0", "end")
        self.txt.configure(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(conteudo)
        messagebox.showinfo("Copiado",
            "Relatório copiado para a área de transferência!", parent=self)

    def _center(self):
        w, h = 700, 720
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")


# ─────────────────────────────────────────────
#  PAINEL DE DETALHES DO BUG
# ─────────────────────────────────────────────
class DetalhesBug(tk.Toplevel):
    def __init__(self, master, bug_id, on_change):
        super().__init__(master)
        self.bug_id    = bug_id
        self.on_change = on_change
        self.configure(bg=BG)
        self.resizable(True, True)
        self._build()
        self._center()
        self.grab_set()

    def _build(self):
        bug = get_bug(self.bug_id)
        if not bug:
            self.destroy(); return

        (bid, titulo, descricao, projeto, prioridade, severidade, status,
         ambiente, passos, res_esp, res_obt, frequencia, tipo,
         rep, resp, criado, atualizado, fechado, notas) = bug

        self.title(f"Bug #{bid}")
        cor_sev = PRIO_COLORS.get(severidade, TEXT_SEC)
        cor_st  = STATUS_COLORS.get(status, TEXT_SEC)

        for w in self.winfo_children():
            w.destroy()

        # ── cabeçalho ────────────────────────
        head = mk_frame(self, bg=SURFACE)
        head.pack(fill="x")
        tk.Frame(head, bg=cor_sev, height=4).pack(fill="x")
        htop = mk_frame(head, bg=SURFACE)
        htop.pack(fill="x", padx=16, pady=8)
        tk.Label(htop, text=f"#{bid} ", bg=SURFACE, fg=TEXT_MUT,
            font=("Courier New", 10)).pack(side="left")
        tk.Label(htop, text=f"● {STATUS_LABEL.get(status,status)}  ",
            bg=SURFACE, fg=cor_st, font=("Courier New", 10, "bold")).pack(side="left")
        tk.Label(htop, text=f"SEV: {severidade}  ",
            bg=SURFACE, fg=cor_sev, font=("Courier New", 10, "bold")).pack(side="left")
        tk.Label(htop, text=f"[{prioridade}]",
            bg=SURFACE, fg=PRIO_COLORS.get(prioridade, TEXT_SEC),
            font=("Courier New", 10)).pack(side="left")
        tk.Label(head, text=titulo,
            bg=SURFACE, fg=TEXT_PRI,
            font=("Courier New", 13, "bold"),
            anchor="w", padx=16, pady=4,
            wraplength=600, justify="left").pack(fill="x")

        # ── fluxo de status ──────────────────
        flow_fr = mk_frame(self, bg=SURFACE2)
        flow_fr.pack(fill="x")
        tk.Frame(flow_fr, bg=BORDER, height=1).pack(fill="x")
        fi = mk_frame(flow_fr, bg=SURFACE2)
        fi.pack(fill="x", padx=12, pady=6)
        mk_label(fi, "FLUXO  ", color=TEXT_MUT, size=8).pack(side="left")
        for s in STATUS_LIST:
            is_cur = (s == status)
            sc = STATUS_COLORS[s]
            tk.Label(fi, text=f" {STATUS_LABEL[s]} ",
                bg=sc if is_cur else SURFACE2,
                fg=BG if is_cur else TEXT_MUT,
                font=("Courier New", 8, "bold" if is_cur else "normal"),
                padx=4, pady=2, relief="flat"
            ).pack(side="left", padx=1)
            if s != STATUS_LIST[-1]:
                mk_label(fi, " › ", color=TEXT_MUT, size=9).pack(side="left")

        # ── corpo scrollável ─────────────────
        _, body = scrolled_canvas(self, bg=BG)

        def block(title_text, value, vtag=TEXT_PRI):
            hf = mk_frame(body, bg=BG)
            hf.pack(fill="x", padx=16, pady=(10, 1))
            mk_label(hf, title_text, color=TEXT_MUT, size=8, bold=True).pack(anchor="w")
            vf = mk_frame(body, bg=SURFACE2)
            vf.pack(fill="x", padx=16)
            tk.Label(vf, text=value or "—",
                bg=SURFACE2, fg=vtag,
                font=FONT_BODY, anchor="nw", justify="left",
                wraplength=580, padx=10, pady=8).pack(fill="x")

        # meta grid
        meta = mk_frame(body, bg=SURFACE)
        meta.pack(fill="x", padx=16, pady=(12, 0))
        meta.columnconfigure((0,1,2,3), weight=1)

        def mcell(row, col, lbl_t, val, vc=TEXT_PRI):
            tk.Label(meta, text=lbl_t, bg=SURFACE, fg=TEXT_MUT,
                font=FONT_SMALL).grid(row=row*2, column=col,
                sticky="w", padx=10, pady=(8,0))
            tk.Label(meta, text=val or "—",
                bg=SURFACE, fg=vc,
                font=FONT_MONO_S, wraplength=130, justify="left"
            ).grid(row=row*2+1, column=col, sticky="w", padx=10, pady=(0,8))

        mcell(0,0, "PROJETO",      projeto,       ACCENT4)
        mcell(0,1, "TIPO",         tipo or "—",   TEXT_PRI)
        mcell(0,2, "REPORTADO POR",rep or "—")
        mcell(0,3, "RESPONSÁVEL",  resp or "—")
        mcell(1,0, "CRIADO EM",    criado,        TEXT_SEC)
        mcell(1,1, "ATUALIZADO",   atualizado,    TEXT_SEC)
        mcell(1,2, "FECHADO EM",   fechado or "—",
              ACCENT2 if fechado else TEXT_MUT)
        mcell(1,3, "FREQUÊNCIA",   frequencia or "—", TEXT_SEC)

        block("AMBIENTE",            ambiente)
        block("DESCRIÇÃO",           descricao)
        block("PASSOS PARA REPRODUZIR", passos)
        block("RESULTADO ESPERADO",  res_esp,  ACCENT2)
        block("RESULTADO OBTIDO",    res_obt,  ACCENT)

        if notas:
            hf = mk_frame(body, bg=BG)
            hf.pack(fill="x", padx=16, pady=(10, 1))
            mk_label(hf, "NOTAS DE FECHAMENTO", color=TEXT_MUT, size=8, bold=True).pack(anchor="w")
            nf = mk_frame(body, bg=SURFACE2)
            nf.pack(fill="x", padx=16)
            tk.Frame(nf, bg=ACCENT2, width=3).pack(side="left", fill="y")
            tk.Label(nf, text=notas, bg=SURFACE2, fg=ACCENT2,
                font=FONT_BODY, anchor="nw", justify="left",
                wraplength=560, padx=10, pady=8).pack(fill="x")

        mk_frame(body, bg=BG, height=10).pack()

        # ── botões ───────────────────────────
        foot = mk_frame(self, bg=BG)
        foot.pack(fill="x", padx=16, pady=(0, 12))

        # esquerda
        styled_btn(foot, "📋  Relatório",
            lambda: RelatorioWindow(self, self.bug_id),
            color=ACCENT4).pack(side="left")
        styled_btn(foot, "🗑  Deletar",
            self._deletar, color="#f85149").pack(side="left", padx=(6,0))

        # direita
        ghost_btn(foot, "✕  Fechar", self.destroy).pack(side="right", padx=(6,0))
        styled_btn(foot, "✎  Editar",
            self._editar, color=ACCENT3).pack(side="right", padx=(6,0))

        if status == "Fechado":
            styled_btn(foot, "↺  Reabrir",
                self._reabrir, color=ACCENT3).pack(side="right", padx=(6,0))
        else:
            prox = STATUS_NEXT.get(status)
            if prox:
                cor = STATUS_COLORS.get(prox, ACCENT2)
                label_prox = STATUS_LABEL.get(prox, prox)
                styled_btn(foot, f"→  {label_prox}",
                    lambda p=prox, t=titulo: self._avancar(p, t),
                    color=cor).pack(side="right", padx=(6,0))

    def _center(self):
        w, h = 720, 680
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _refresh(self):
        self.on_change()
        self._build()

    def _avancar(self, novo_status, titulo):
        MudarStatusDialog(self, self.bug_id, titulo, novo_status, self._refresh)

    def _editar(self):
        BugForm(self, self._refresh, bug=get_bug(self.bug_id))

    def _reabrir(self):
        reabrir_bug(self.bug_id)
        self._refresh()

    def _deletar(self):
        if messagebox.askyesno("Confirmar",
                "Deletar este bug permanentemente?",
                parent=self, icon="warning"):
            deletar_bug(self.bug_id)
            self.on_change()
            self.destroy()


# ─────────────────────────────────────────────
#  JANELA PRINCIPAL
# ─────────────────────────────────────────────
class BugTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        init_db()
        self.title("BugTracker")
        self.configure(bg=BG)
        self.minsize(1080, 640)
        _combo_style()
        self.bind("<Control-n>", lambda e: self._novo_bug())
        self._build_ui()
        self._refresh()
        self._center()

    def _center(self):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = 1240, 740
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        self.sidebar = mk_frame(self, bg=SURFACE, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()
        main = mk_frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        self._build_topbar(main)
        self._build_table(main)

    # ── SIDEBAR ──────────────────────────────

    def _build_sidebar(self):
        logo = mk_frame(self.sidebar, bg=SURFACE)
        logo.pack(fill="x")
        tk.Frame(logo, bg=ACCENT, height=4).pack(fill="x")
        tk.Label(logo, text="⬡  BugTracker",
            bg=SURFACE, fg=ACCENT,
            font=("Courier New", 15, "bold"),
            pady=16, padx=16, anchor="w").pack(fill="x")
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x")

        self.stats_frame = mk_frame(self.sidebar, bg=SURFACE)
        self.stats_frame.pack(fill="x", pady=4)
        self._build_stats()
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", pady=4)

        filt = mk_frame(self.sidebar, bg=SURFACE)
        filt.pack(fill="x", padx=14, pady=4)
        mk_label(filt, "FILTROS", color=TEXT_MUT, size=8, bold=True
            ).pack(anchor="w", pady=(4,6))

        mk_label(filt, "Status", color=TEXT_SEC, size=9).pack(anchor="w")
        self.var_status = tk.StringVar(value="Todos")
        for s in ["Todos"] + STATUS_LIST:
            c = STATUS_COLORS.get(s, TEXT_PRI)
            label_s = STATUS_LABEL.get(s, s)
            tk.Radiobutton(filt,
                text=f" {label_s}",
                variable=self.var_status, value=s,
                bg=SURFACE, fg=c, selectcolor=SURFACE,
                activebackground=SURFACE, activeforeground=TEXT_PRI,
                font=FONT_MONO_S, command=self._refresh
            ).pack(anchor="w", padx=4)

        mk_label(filt, "Severidade", color=TEXT_SEC, size=9
            ).pack(anchor="w", pady=(8,0))
        self.var_sev = tk.StringVar(value="Todos")
        for s in ["Todos"] + SEVERIDADES:
            tk.Radiobutton(filt,
                text=f" {s}",
                variable=self.var_sev, value=s,
                bg=SURFACE, fg=PRIO_COLORS.get(s, TEXT_PRI),
                selectcolor=SURFACE,
                activebackground=SURFACE, activeforeground=TEXT_PRI,
                font=FONT_MONO_S, command=self._refresh
            ).pack(anchor="w", padx=4)

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", pady=8)
        btn_f = mk_frame(self.sidebar, bg=SURFACE)
        btn_f.pack(fill="x", padx=14, pady=4)
        styled_btn(btn_f, "+  Novo Bug", self._novo_bug).pack(fill="x")

        tk.Label(self.sidebar,
            text=f"db: {os.path.basename(DB_PATH)}",
            bg=SURFACE, fg=TEXT_MUT,
            font=("Courier New", 8)).pack(side="bottom", pady=8)

    def _build_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        s = stats()
        mk_label(self.stats_frame, "VISÃO GERAL", color=TEXT_MUT,
            size=8, bold=True).pack(anchor="w", padx=14, pady=(6,4))

        data = [
            ("Total de bugs",    s["total"],    ACCENT4),
            ("Abertos",          s["aberto"],   ACCENT),
            ("Em análise",       s["analise"],  ACCENT3),
            ("Em correção",      s["correcao"], ACCENT5),
            ("Verificados",      s["verif"],    ACCENT4),
            ("Fechados",         s["fechado"],  ACCENT2),
            ("Críticos abertos", s["critico"],  "#f85149"),
        ]
        for label_text, val, color in data:
            c = mk_frame(self.stats_frame, bg=SURFACE2)
            c.pack(fill="x", padx=10, pady=2)
            tk.Frame(c, bg=color, width=3).pack(side="left", fill="y")
            inn = mk_frame(c, bg=SURFACE2)
            inn.pack(side="left", padx=8, pady=4)
            tk.Label(inn, text=str(val), bg=SURFACE2, fg=color,
                font=("Courier New", 16, "bold")).pack(anchor="w")
            tk.Label(inn, text=label_text, bg=SURFACE2, fg=TEXT_MUT,
                font=FONT_SMALL).pack(anchor="w")

    # ── TOPBAR ───────────────────────────────
    def _build_topbar(self, parent):
        bar = mk_frame(parent, bg=SURFACE)
        bar.pack(fill="x")
        tk.Frame(bar, bg=BORDER, height=1).pack(fill="x")
        inner = mk_frame(bar, bg=SURFACE)
        inner.pack(fill="x", padx=16, pady=8)
        btn_f = mk_frame(self.sidebar, bg=SURFACE)
        styled_btn(btn_f, "+  Novo Bug", self._novo_bug).pack(fill="x")
        mk_label(inner, "🔍", color=TEXT_MUT, size=12).pack(side="left")
        self.busca_var = tk.StringVar()
        tk.Entry(inner, textvariable=self.busca_var,
            bg=SURFACE2, fg=TEXT_PRI, insertbackground=TEXT_PRI,
            font=FONT_BODY, relief="flat",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT4, bd=4, width=38
        ).pack(side="left", padx=8)
        self.busca_var.trace_add("write", lambda *_: self._refresh())

        mk_label(inner, "Projeto:", color=TEXT_SEC, size=9
            ).pack(side="left", padx=(12,4))
        self.var_proj = tk.StringVar(value="Todos")
        self.proj_menu = mk_combo(inner, ["Todos"], width=16)
        self.proj_menu.configure(textvariable=self.var_proj)
        self.proj_menu.pack(side="left")
        self.proj_menu.bind("<<ComboboxSelected>>", lambda _: self._refresh())

        self.lbl_count = tk.Label(inner, text="", bg=SURFACE,
            fg=TEXT_MUT, font=FONT_SMALL)
        self.lbl_count.pack(side="right")

    # ── TABELA ───────────────────────────────
    def _build_table(self, parent):
        wrap = mk_frame(parent, bg=BG)
        wrap.pack(fill="both", expand=True)

        # cabeçalhos
        cols = [
            ("#",         4),  ("Título",    34), ("Projeto", 12),
            ("Tipo",     11),  ("Sev.",      10), ("Status",  14),
            ("Responsável",13),("Criado em", 14),
        ]
        head_row = mk_frame(wrap, bg=SURFACE2)
        head_row.pack(fill="x")
        for col, w in cols:
            tk.Label(head_row, text=col, bg=SURFACE2,
                fg=TEXT_MUT, font=("Courier New", 9, "bold"),
                width=w, anchor="w", padx=6, pady=6
            ).pack(side="left")
        tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x")

        sf = mk_frame(wrap, bg=BG)
        sf.pack(fill="both", expand=True)
        canvas = tk.Canvas(sf, bg=BG, bd=0, highlightthickness=0)
        sb = ttk.Scrollbar(sf, orient="vertical", command=canvas.yview)
        self.rows_frame = mk_frame(canvas, bg=BG)
        self.rows_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

    # ── REFRESH ──────────────────────────────
    def _refresh(self):
        fs   = getattr(self, "var_status", None)
        fp   = getattr(self, "var_proj",   None)
        fsev = getattr(self, "var_sev",    None)
        fb   = getattr(self, "busca_var",  None)

        bugs = listar_bugs(
            filtro_status    = fs.get()   if fs   else None,
            filtro_projeto   = fp.get()   if fp   else None,
            filtro_severidade= fsev.get() if fsev else None,
            busca            = fb.get()   if fb   else None,
        )

        self._build_stats()

        projs = ["Todos"] + get_projetos()
        if hasattr(self, "proj_menu"):
            cur = self.var_proj.get()
            self.proj_menu["values"] = projs
            if cur not in projs:
                self.var_proj.set("Todos")

        if hasattr(self, "lbl_count"):
            self.lbl_count.config(text=f"{len(bugs)} resultado(s)")

        for w in self.rows_frame.winfo_children():
            w.destroy()

        if not bugs:
            tk.Label(self.rows_frame,
                text="Nenhum bug encontrado.",
                bg=BG, fg=TEXT_MUT,
                font=("Courier New", 12), pady=40).pack()
            return

        for i, bug in enumerate(bugs):
            (bid, titulo, descricao, projeto, prioridade, severidade, status,
             ambiente, passos, res_esp, res_obt, frequencia, tipo,
             rep, resp, criado, atualizado, fechado, notas) = bug

            row_bg  = BG if i % 2 == 0 else SURFACE
            cor_sev = PRIO_COLORS.get(severidade, TEXT_SEC)
            cor_st  = STATUS_COLORS.get(status, TEXT_SEC)

            row = mk_frame(self.rows_frame, bg=row_bg)
            row.pack(fill="x")
            row.bind("<Button-1>", lambda e, b=bid: self._open(b))
            row.bind("<Enter>",    lambda e, r=row: r.config(bg=SURFACE2))
            row.bind("<Leave>",    lambda e, r=row, rb=row_bg: r.config(bg=rb))

            def cell(text, color, width, fnt=FONT_MONO_S):
                lbl_ = tk.Label(row, text=text,
                    bg=row["bg"], fg=color, font=fnt,
                    width=width, anchor="w", padx=6, pady=9)
                lbl_.pack(side="left")
                lbl_.bind("<Button-1>", lambda e, b=bid: self._open(b))
                lbl_.bind("<Enter>",    lambda e, r=row: r.config(bg=SURFACE2))
                lbl_.bind("<Leave>",    lambda e, r=row, rb=row_bg: r.config(bg=rb))

            cell(f"#{bid}",  TEXT_MUT,  4)
            cell(titulo[:46]+("…" if len(titulo)>46 else ""),
                 TEXT_PRI, 34, fnt=("Courier New", 10))
            cell(projeto[:13],               ACCENT4, 12)
            cell((tipo or "—")[:12],         TEXT_SEC, 11)
            cell(severidade,                 cor_sev,  10)
            cell(STATUS_LABEL.get(status, status)[:14], cor_st, 14)
            cell((resp or "—")[:13],         TEXT_SEC, 13)
            cell(criado[:16],                TEXT_MUT, 14)

            tk.Frame(self.rows_frame, bg=BORDER, height=1).pack(fill="x")

    def _novo_bug(self):
        form = BugForm(self, self._refresh)
        self._center()
        self.lift()
        self.focus_force()
        self.grab_set()
        

    def _open(self, bug_id):
        DetalhesBug(self, bug_id, self._refresh)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = BugTracker()
    app.mainloop()
