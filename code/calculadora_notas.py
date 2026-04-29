import tkinter as tk
from tkinter import messagebox

# ── Paleta ────────────────────────────────────────────
BG       = "#0f1923"
SURFACE  = "#1a2535"
SURFACE2 = "#243045"
BORDER   = "#2e3d55"
TEXT_PRI = "#e8edf3"
TEXT_SEC = "#7a8ea8"
ACCENT   = "#4a9eff"

COR_APROVADO    = "#34d47a"
COR_RECUPERACAO = "#f5c842"
COR_REPROVADO   = "#f05454"


# ── Lógica ────────────────────────────────────────────
def calcular():
    nome = entry_nome.get().strip()
    n1   = entry_n1.get().strip()
    n2   = entry_n2.get().strip()

    # validações
    if not nome:
        shake(entry_nome)
        messagebox.showwarning("Campo vazio", "Informe o nome do aluno.", parent=root)
        return

    try:
        nota1 = float(n1.replace(",", "."))
        nota2 = float(n2.replace(",", "."))
    except ValueError:
        messagebox.showwarning("Valor inválido",
            "As notas devem ser números (ex: 7 ou 7.5).", parent=root)
        return

    if not (-2 <= nota1 <= 10) or not (0 <= nota2 <= 10):
        messagebox.showwarning("Fora do intervalo",
            "As notas devem estar entre 0 e 10.", parent=root)
        return

    media = (nota1 + nota2) / 2

    if media > 6:
        situacao = "Aprovado"
        cor      = COR_APROVADO
        icone    = "✔"
    elif media >= 4:
        situacao = "Em Recuperação"
        cor      = COR_RECUPERACAO
        icone    = "⚠"
    else:
        situacao = "Reprovado"
        cor      = COR_REPROVADO
        icone    = "✖"

    # exibe resultado
    frame_resultado.pack(fill="x", padx=30, pady=(0, 28))

    lbl_nome_res.config(text=nome)
    lbl_media_val.config(text=f"{media:.1f}", fg=cor)
    lbl_n1_val.config(text=f"{nota1:.1f}")
    lbl_n2_val.config(text=f"{nota2:.1f}")

    # faixa colorida de situação — fundo sólido escuro por situação
    bg_sit = {
        COR_APROVADO:    "#0d2b1a",
        COR_RECUPERACAO: "#2b2510",
        COR_REPROVADO:   "#2b1010",
    }.get(cor, SURFACE2)
    frame_situacao.config(bg=bg_sit)
    sit_inner.config(bg=bg_sit)
    lbl_icone.config(bg=bg_sit, text=icone, fg=cor)
    lbl_situacao.config(bg=bg_sit, text=situacao, fg=cor)

    # animação simples: fade-in via resize
    frame_resultado.update_idletasks()
    pulse(lbl_situacao)


def limpar():
    entry_nome.delete(0, "end")
    entry_n1.delete(0, "end")
    entry_n2.delete(0, "end")
    frame_resultado.pack_forget()
    entry_nome.focus()


# ── Animações ─────────────────────────────────────────
def shake(widget):
    """Balança o widget horizontalmente para indicar erro."""
    x0 = widget.winfo_x()
    def step(i, delta):
        if i == 0:
            return
        widget.place_configure(x=widget.winfo_x() + delta)
        widget.after(30, step, i - 1, -delta)
    widget.after(0, step, 6, 8)


def pulse(widget, count=0):
    """Pisca o label de situação uma vez ao aparecer."""
    sizes = [22, 24, 22]
    if count < len(sizes):
        widget.config(font=("Segoe UI", sizes[count], "bold"))
        widget.after(80, pulse, widget, count + 1)


# ── Helpers de widget ─────────────────────────────────
def mk_entry(parent, ph=""):
    f = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    e = tk.Entry(f,
        bg=SURFACE2, fg=TEXT_PRI,
        insertbackground=TEXT_PRI,
        font=("Segoe UI", 13),
        relief="flat", bd=8,
        highlightthickness=0)
    e.pack(fill="x")
    # placeholder
    if ph:
        e.insert(0, ph)
        e.config(fg=TEXT_SEC)
        def on_focus_in(event, entry=e, placeholder=ph):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=TEXT_PRI)
        def on_focus_out(event, entry=e, placeholder=ph):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=TEXT_SEC)
        e.bind("<FocusIn>",  on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
    return f, e


def mk_label_pair(parent, label_text, value_text, val_color=TEXT_PRI):
    row = tk.Frame(parent, bg=parent["bg"])
    row.pack(fill="x", pady=2)
    tk.Label(row, text=label_text,
        bg=parent["bg"], fg=TEXT_SEC,
        font=("Segoe UI", 10)).pack(side="left")
    lbl = tk.Label(row, text=value_text,
        bg=parent["bg"], fg=val_color,
        font=("Segoe UI", 10, "bold"))
    lbl.pack(side="right")
    return lbl


# ── Janela principal ───────────────────────────────────
root = tk.Tk()
root.title("Calculadora de Notas")
root.configure(bg=BG)
root.resizable(False, False)

# centraliza
W, H = 420, 580
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

# ── Cabeçalho ─────────────────────────────────────────
header = tk.Frame(root, bg=SURFACE)
header.pack(fill="x")
tk.Frame(header, bg=ACCENT, height=4).pack(fill="x")
tk.Label(header,
    text="  ◈  Calculadora de Notas",
    bg=SURFACE, fg=ACCENT,
    font=("Segoe UI", 15, "bold"),
    anchor="w", pady=14
).pack(fill="x", padx=18)
tk.Label(header,
    text="  Informe os dados do aluno para calcular a média",
    bg=SURFACE, fg=TEXT_SEC,
    font=("Segoe UI", 10),
    anchor="w", pady=0
).pack(fill="x", padx=18)
tk.Frame(header, bg=BORDER, height=1).pack(fill="x", pady=(10, 0))

# ── Formulário ────────────────────────────────────────
form = tk.Frame(root, bg=BG)
form.pack(fill="x", padx=30, pady=24)

# Nome
tk.Label(form, text="Nome do Aluno", bg=BG, fg=TEXT_SEC,
    font=("Segoe UI", 10, "bold"), anchor="w"
).pack(fill="x", pady=(0, 4))
frame_nome, entry_nome = mk_entry(form, "Digite o nome completo")
frame_nome.pack(fill="x", pady=(0, 16))

# Notas lado a lado
notas_row = tk.Frame(form, bg=BG)
notas_row.pack(fill="x")

# Nota 1
col1 = tk.Frame(notas_row, bg=BG)
col1.pack(side="left", fill="x", expand=True, padx=(0, 8))
tk.Label(col1, text="Nota 1", bg=BG, fg=TEXT_SEC,
    font=("Segoe UI", 10, "bold"), anchor="w"
).pack(fill="x", pady=(0, 4))
frame_n1, entry_n1 = mk_entry(col1, "0 – 10")
frame_n1.pack(fill="x")

# Nota 2
col2 = tk.Frame(notas_row, bg=BG)
col2.pack(side="left", fill="x", expand=True)
tk.Label(col2, text="Nota 2", bg=BG, fg=TEXT_SEC,
    font=("Segoe UI", 10, "bold"), anchor="w"
).pack(fill="x", pady=(0, 4))
frame_n2, entry_n2 = mk_entry(col2, "0 – 10")
frame_n2.pack(fill="x")

# ── Botões ────────────────────────────────────────────
btn_row = tk.Frame(root, bg=BG)
btn_row.pack(fill="x", padx=30, pady=(4, 0))

def btn_hover(btn, color_on, color_off):
    btn.bind("<Enter>", lambda e: btn.config(bg=color_on))
    btn.bind("<Leave>", lambda e: btn.config(bg=color_off))

btn_calc = tk.Button(btn_row,
    text="  ▶  Calcular",
    command=calcular,
    bg=ACCENT, fg=BG,
    font=("Segoe UI", 11, "bold"),
    relief="flat", cursor="hand2",
    padx=18, pady=10, bd=0)
btn_calc.pack(side="left", fill="x", expand=True, padx=(0, 8))
btn_hover(btn_calc, "#74b8ff", ACCENT)

btn_limpar = tk.Button(btn_row,
    text="  ↺  Limpar",
    command=limpar,
    bg=SURFACE2, fg=TEXT_SEC,
    font=("Segoe UI", 11),
    relief="flat", cursor="hand2",
    padx=18, pady=10, bd=0)
btn_limpar.pack(side="left", fill="x", expand=True)
btn_hover(btn_limpar, BORDER, SURFACE2)

# ── Separador ─────────────────────────────────────────
tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=20)

# ── Painel de resultado (oculto até calcular) ─────────
frame_resultado = tk.Frame(root, bg=SURFACE, bd=0)

# mini grid de notas / média
info_grid = tk.Frame(frame_resultado, bg=SURFACE)
info_grid.pack(fill="x", padx=20, pady=(16, 10))

lbl_nome_res = tk.Label(info_grid,
    text="", bg=SURFACE, fg=TEXT_PRI,
    font=("Segoe UI", 12, "bold"), anchor="w")
lbl_nome_res.pack(fill="x", pady=(0, 8))

tk.Frame(info_grid, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

# linha com N1 / N2 / Média
cols_info = tk.Frame(info_grid, bg=SURFACE)
cols_info.pack(fill="x")

def info_card(parent, label_text, default_text, is_big=False):
    c = tk.Frame(parent, bg=SURFACE2, padx=12, pady=8)
    c.pack(side="left", fill="x", expand=True, padx=4)
    tk.Label(c, text=label_text, bg=SURFACE2, fg=TEXT_SEC,
        font=("Segoe UI", 9)).pack()
    lbl = tk.Label(c, text=default_text, bg=SURFACE2,
        fg=TEXT_PRI,
        font=("Segoe UI", 18 if is_big else 14, "bold"))
    lbl.pack()
    return lbl

lbl_n1_val    = info_card(cols_info, "Nota 1", "—")
lbl_n2_val    = info_card(cols_info, "Nota 2", "—")
lbl_media_val = info_card(cols_info, "Média",  "—", is_big=True)

# faixa de situação
frame_situacao = tk.Frame(frame_resultado, bg=SURFACE2)
frame_situacao.pack(fill="x", padx=20, pady=(6, 16))

sit_inner = tk.Frame(frame_situacao, bg=frame_situacao["bg"])
sit_inner.pack(pady=14)

lbl_icone = tk.Label(sit_inner, text="", bg=frame_situacao["bg"],
    font=("Segoe UI", 22))
lbl_icone.pack(side="left", padx=(0, 10))

lbl_situacao = tk.Label(sit_inner, text="", bg=frame_situacao["bg"],
    font=("Segoe UI", 22, "bold"))
lbl_situacao.pack(side="left")

# bind Enter nos campos para acionar calcular
root.bind("<Return>", lambda e: calcular())

root.mainloop()
