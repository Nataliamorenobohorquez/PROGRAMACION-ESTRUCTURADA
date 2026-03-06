import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import base64
import io

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

# ─── Paleta de colores ────────────────────────────────────────────────────────
BG_DARK      = "#0F1923"
BG_PANEL     = "#162230"
BG_CARD      = "#1E2F3E"
ACCENT_BLUE  = "#2E86DE"
ACCENT_GREEN = "#1DD1A1"
ACCENT_RED   = "#FF6B6B"
ACCENT_GOLD  = "#FFC72C"
TEXT_WHITE   = "#EAF0FB"
TEXT_MUTED   = "#7F8C9A"
BORDER       = "#2A3D50"
ROW_ODD      = "#192736"
ROW_EVEN     = "#1E2F3E"
ROW_SEL      = "#2E4A62"

IMG_W, IMG_H = 220, 160


def _resize_pil(img, w, h):
    """Redimensiona la imagen manteniendo proporción y recortando al centro."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return img.crop((x, y, x + w, y + h))


class SistemaRentabilidad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Análisis de Rentabilidad")
        self.geometry("1280x760")
        self.minsize(1060, 640)
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        self.productos  = []    # lista de diccionarios con datos de cada producto
        self._foto_b64  = None  # imagen actual del formulario en Base64
        self._foto_tk   = None  # referencia PhotoImage (evita que el GC la elimine)
        self._sort_rev  = {}    # estado de ordenamiento por columna

        self._build_ui()
        self._center_window()

    # ─── Centrar ventana ──────────────────────────────────────────────────────
    def _center_window(self):
        self.update_idletasks()
        w, h   = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ─── Construcción de interfaz ─────────────────────────────────────────────
    def _build_ui(self):
        # Cabecera
        header = tk.Frame(self, bg=BG_PANEL, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="📊  Sistema de Análisis de Rentabilidad",
                 font=("Segoe UI", 16, "bold"), fg=TEXT_WHITE, bg=BG_PANEL
                 ).pack(side="left", padx=24, pady=14)
        tk.Label(header, text="Gestión inteligente de productos y proveedores",
                 font=("Segoe UI", 10), fg=TEXT_MUTED, bg=BG_PANEL
                 ).pack(side="left", pady=20)
        tk.Frame(self, bg=ACCENT_BLUE, height=2).pack(fill="x")

        # Área central
        center = tk.Frame(self, bg=BG_DARK)
        center.pack(fill="both", expand=True, padx=18, pady=(14, 0))
        self._build_form(center)
        self._build_table(center)

        self._build_action_bar()
        self._build_status_bar()

    # ─── Formulario (columna izquierda) ───────────────────────────────────────
    def _build_form(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL, width=340)
        frame.pack(side="left", fill="y", padx=(0, 14))
        frame.pack_propagate(False)

        tk.Label(frame, text="➕  Registrar Producto",
                 font=("Segoe UI", 12, "bold"),
                 fg=ACCENT_BLUE, bg=BG_PANEL).pack(anchor="w", padx=20, pady=(18, 4))
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 10))

        # ── Foto del producto ─────────────────────────────────────────────────
        foto_outer = tk.Frame(frame, bg=BG_PANEL)
        foto_outer.pack(fill="x", padx=20, pady=(0, 8))

        tk.Label(foto_outer, text="Foto del Producto",
                 font=("Segoe UI", 9, "bold"),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(0, 4))

        foto_borde = tk.Frame(foto_outer, bg=BORDER,
                              width=IMG_W + 4, height=IMG_H + 4)
        foto_borde.pack()
        foto_borde.pack_propagate(False)

        self.foto_canvas = tk.Canvas(foto_borde,
                                     width=IMG_W, height=IMG_H,
                                     bg=BG_CARD, highlightthickness=0,
                                     cursor="hand2")
        self.foto_canvas.place(x=2, y=2)
        self._draw_placeholder()
        self.foto_canvas.bind("<Button-1>", lambda _e: self._seleccionar_foto())

        btn_row = tk.Frame(foto_outer, bg=BG_PANEL)
        btn_row.pack(fill="x", pady=(6, 0))

        btn_sel = tk.Button(btn_row, text="📷 Seleccionar foto",
                            font=("Segoe UI", 9),
                            bg=ACCENT_BLUE, fg=TEXT_WHITE,
                            activebackground="#1a6bbf",
                            relief="flat", bd=0, cursor="hand2",
                            command=self._seleccionar_foto)
        btn_sel.pack(side="left", ipady=5, padx=(0, 6), fill="x", expand=True)
        self._hover(btn_sel, ACCENT_BLUE, "#1a6bbf")

        btn_del = tk.Button(btn_row, text="✖ Quitar",
                            font=("Segoe UI", 9),
                            bg=BG_CARD, fg=TEXT_MUTED,
                            activebackground=BORDER,
                            relief="flat", bd=0, cursor="hand2",
                            command=self._quitar_foto)
        btn_del.pack(side="left", ipady=5)
        self._hover(btn_del, BG_CARD, BORDER)

        # ── Campos de texto ───────────────────────────────────────────────────
        campos = [
            ("Nombre del Producto",   "nombre", "Ej: Auriculares Bluetooth"),
            ("Costo Proveedor 1 ($)", "costo1", "Ej: 150.00"),
            ("Costo Proveedor 2 ($)", "costo2", "Ej: 138.50"),
            ("Precio de Venta ($)",   "pventa", "Ej: 280.00"),
        ]
        self.entries = {}
        for etiqueta, clave, hint in campos:
            tk.Label(frame, text=etiqueta,
                     font=("Segoe UI", 9, "bold"),
                     fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", padx=20, pady=(6, 2))

            entrada = tk.Entry(frame,
                               font=("Segoe UI", 11),
                               bg=BG_CARD, fg=TEXT_MUTED,
                               insertbackground=TEXT_WHITE,
                               relief="flat", bd=0,
                               highlightthickness=1,
                               highlightbackground=BORDER,
                               highlightcolor=ACCENT_BLUE)
            entrada.insert(0, hint)
            entrada.pack(fill="x", padx=20, ipady=9)

            # Resaltar borde al enfocar
            entrada.bind("<FocusIn>",
                         lambda _e, en=entrada: en.config(highlightbackground=ACCENT_BLUE))
            entrada.bind("<FocusOut>",
                         lambda _e, en=entrada: en.config(highlightbackground=BORDER))

            # Comportamiento de placeholder
            entrada.bind("<FocusIn>",
                         lambda _e, en=entrada, ph=hint: self._limpiar_ph(en, ph),
                         add="+")
            entrada.bind("<FocusOut>",
                         lambda _e, en=entrada, ph=hint: self._restaurar_ph(en, ph),
                         add="+")

            self.entries[clave] = (entrada, hint)

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=20, pady=12)

        btn_reg = tk.Button(frame, text="✔  Registrar Producto",
                            font=("Segoe UI", 11, "bold"),
                            bg=ACCENT_BLUE, fg=TEXT_WHITE,
                            activebackground="#1a6bbf",
                            relief="flat", bd=0, cursor="hand2",
                            command=self._registrar)
        btn_reg.pack(fill="x", padx=20, ipady=12)
        self._hover(btn_reg, ACCENT_BLUE, "#1a6bbf")

        btn_clr = tk.Button(frame, text="↺  Limpiar Formulario",
                            font=("Segoe UI", 10),
                            bg=BG_CARD, fg=TEXT_MUTED,
                            activebackground=BORDER,
                            relief="flat", bd=0, cursor="hand2",
                            command=self._limpiar_form)
        btn_clr.pack(fill="x", padx=20, pady=(8, 0), ipady=9)

        # ── Tarjetas de resumen ───────────────────────────────────────────────
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=20, pady=14)
        tk.Label(frame, text="RESUMEN", font=("Segoe UI", 8, "bold"),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", padx=20)
        contenedor = tk.Frame(frame, bg=BG_PANEL)
        contenedor.pack(fill="x", padx=20, pady=(8, 0))
        self.lbl_total = self._tarjeta(contenedor, "Total productos",  "0",     TEXT_WHITE)
        self.lbl_avg   = self._tarjeta(contenedor, "Rentab. promedio", "0.00%", ACCENT_GREEN)
        self.lbl_best  = self._tarjeta(contenedor, "Mayor ganancia",   "$0.00", ACCENT_GOLD)

    def _tarjeta(self, parent, titulo, valor, color):
        """Crea una tarjeta de estadística y devuelve la etiqueta del valor."""
        card = tk.Frame(parent, bg=BG_CARD, pady=8)
        card.pack(fill="x", pady=3)
        tk.Label(card, text=titulo, font=("Segoe UI", 8),
                 fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", padx=10)
        lbl = tk.Label(card, text=valor, font=("Segoe UI", 13, "bold"),
                       fg=color, bg=BG_CARD)
        lbl.pack(anchor="w", padx=10)
        return lbl

    # ─── Placeholder helpers ──────────────────────────────────────────────────
    def _limpiar_ph(self, entrada, hint):
        if entrada.get() == hint:
            entrada.delete(0, "end")
            entrada.config(fg=TEXT_WHITE)

    def _restaurar_ph(self, entrada, hint):
        if not entrada.get():
            entrada.insert(0, hint)
            entrada.config(fg=TEXT_MUTED)

    def _obtener_valor(self, clave):
        entrada, hint = self.entries[clave]
        valor = entrada.get().strip()
        return "" if valor == hint else valor

    # ─── Foto ─────────────────────────────────────────────────────────────────
    def _draw_placeholder(self):
        self.foto_canvas.delete("all")
        self.foto_canvas.create_rectangle(
            8, 8, IMG_W - 8, IMG_H - 8,
            outline=BORDER, dash=(6, 4), width=1)
        self.foto_canvas.create_text(
            IMG_W // 2, IMG_H // 2 - 14,
            text="🖼", font=("Segoe UI", 28), fill=BORDER)
        self.foto_canvas.create_text(
            IMG_W // 2, IMG_H // 2 + 18,
            text="Clic para agregar foto",
            font=("Segoe UI", 9), fill=TEXT_MUTED)

    def _seleccionar_foto(self):
        tipos = [("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                 ("Todos",    "*.*")]
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto del producto", filetypes=tipos)
        if not ruta:
            return

        if PIL_DISPONIBLE:
            try:
                img       = Image.open(ruta).convert("RGB")
                img_small = _resize_pil(img, IMG_W, IMG_H)
                self._foto_tk = ImageTk.PhotoImage(img_small)
                self.foto_canvas.delete("all")
                self.foto_canvas.create_image(0, 0, anchor="nw", image=self._foto_tk)

                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=80)
                self._foto_b64 = base64.b64encode(buf.getvalue()).decode()
                self._set_status(f"🖼 Foto cargada: {os.path.basename(ruta)}")
            except Exception as ex:
                messagebox.showerror("Error de imagen",
                                     f"No se pudo cargar la imagen:\n{ex}")
        else:
            # Sin Pillow: se guarda la ruta y se muestra texto de confirmación
            self._foto_b64 = ruta
            self.foto_canvas.delete("all")
            self.foto_canvas.create_rectangle(
                4, 4, IMG_W - 4, IMG_H - 4, fill=BG_CARD, outline=ACCENT_BLUE)
            self.foto_canvas.create_text(
                IMG_W // 2, IMG_H // 2 - 10,
                text="✔ Foto registrada",
                font=("Segoe UI", 10, "bold"), fill=ACCENT_GREEN)
            self.foto_canvas.create_text(
                IMG_W // 2, IMG_H // 2 + 12,
                text="(instala Pillow para preview)",
                font=("Segoe UI", 8), fill=TEXT_MUTED)
            self._set_status(f"🖼 Foto vinculada: {os.path.basename(ruta)}")

    def _quitar_foto(self):
        self._foto_b64 = None
        self._foto_tk  = None
        self._draw_placeholder()

    # ─── Tabla (columna derecha) ───────────────────────────────────────────────
    def _build_table(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL)
        frame.pack(side="left", fill="both", expand=True)

        encabezado = tk.Frame(frame, bg=BG_PANEL)
        encabezado.pack(fill="x", pady=(10, 8), padx=14)
        tk.Label(encabezado, text="📋  Productos Registrados",
                 font=("Segoe UI", 12, "bold"),
                 fg=TEXT_WHITE, bg=BG_PANEL).pack(side="left")
        tk.Label(encabezado, text="(doble clic para ver foto)",
                 font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL).pack(side="right", padx=10)
        self.lbl_count = tk.Label(encabezado, text="0 registros",
                                  font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL)
        self.lbl_count.pack(side="right", padx=4)

        # Estilo del Treeview
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Custom.Treeview",
                         background=ROW_EVEN, foreground=TEXT_WHITE,
                         fieldbackground=ROW_EVEN, rowheight=38,
                         font=("Segoe UI", 10), borderwidth=0)
        estilo.configure("Custom.Treeview.Heading",
                         background=BG_CARD, foreground=TEXT_MUTED,
                         font=("Segoe UI", 9, "bold"),
                         relief="flat", borderwidth=0, padding=(8, 8))
        estilo.map("Custom.Treeview",
                   background=[("selected", ROW_SEL)],
                   foreground=[("selected", TEXT_WHITE)])
        estilo.map("Custom.Treeview.Heading",
                   background=[("active", BORDER)])
        estilo.configure("Vertical.TScrollbar",
                         background=BG_CARD, troughcolor=BG_PANEL,
                         arrowcolor=TEXT_MUTED, borderwidth=0)
        estilo.configure("Horizontal.TScrollbar",
                         background=BG_CARD, troughcolor=BG_PANEL,
                         arrowcolor=TEXT_MUTED, borderwidth=0)

        columnas = ("foto", "producto", "proveedor", "costo_mejor",
                    "precio_venta", "ganancia", "rentabilidad")
        self.tree = ttk.Treeview(frame, columns=columnas,
                                  show="headings",
                                  style="Custom.Treeview",
                                  selectmode="browse")

        definicion = {
            "foto":         ("📷",               46,  "center"),
            "producto":     ("Producto",         165, "w"),
            "proveedor":    ("Mejor Proveedor",  120, "center"),
            "costo_mejor":  ("Costo Mejor ($)",  110, "center"),
            "precio_venta": ("Precio Venta ($)", 110, "center"),
            "ganancia":     ("Ganancia ($)",      110, "center"),
            "rentabilidad": ("Rentabilidad (%)",  110, "center"),
        }
        for col, (titulo, ancho, ancla) in definicion.items():
            self.tree.heading(col, text=titulo,
                              command=lambda c=col: self._ordenar(c))
            self.tree.column(col, width=ancho, anchor=ancla, minwidth=40)

        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(14, 0), pady=(0, 2))
        vsb.pack(side="right",  fill="y",  pady=(0, 2))
        hsb.pack(side="bottom", fill="x",  padx=14)

        self.tree.tag_configure("odd",    background=ROW_ODD)
        self.tree.tag_configure("even",   background=ROW_EVEN)
        self.tree.tag_configure("high",   foreground=ACCENT_GREEN)
        self.tree.tag_configure("medium", foreground=ACCENT_GOLD)
        self.tree.tag_configure("low",    foreground=ACCENT_RED)

        self.tree.bind("<Double-1>", self._doble_clic)

    # ─── Barra de acciones ────────────────────────────────────────────────────
    def _build_action_bar(self):
        barra = tk.Frame(self, bg=BG_PANEL, height=62)
        barra.pack(fill="x", side="bottom", pady=(8, 0))
        barra.pack_propagate(False)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", side="bottom")

        botones = [
            ("🔍  Ver Productos",        self._ver_productos, ACCENT_BLUE, "#1a6bbf"),
            ("🗑  Eliminar Seleccionado", self._eliminar,      "#C0392B",   "#922b21"),
            ("💾  Guardar Datos",         self._guardar,       "#27AE60",   "#1e8449"),
            ("📂  Cargar Datos",          self._cargar,        ACCENT_GOLD, "#e6a800"),
            ("❌  Salir",                 self._salir,         "#4A4A4A",   "#333333"),
        ]
        for texto, cmd, bg, hbg in botones:
            btn = tk.Button(barra, text=texto,
                            font=("Segoe UI", 9, "bold"),
                            bg=bg, fg=TEXT_WHITE,
                            activebackground=hbg, activeforeground=TEXT_WHITE,
                            relief="flat", bd=0, cursor="hand2",
                            command=cmd, padx=18)
            btn.pack(side="left", padx=(14, 0), pady=12, ipady=6)
            self._hover(btn, bg, hbg)

    # ─── Barra de estado ──────────────────────────────────────────────────────
    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="✔ Sistema listo.")
        barra = tk.Frame(self, bg="#0A1520", height=24)
        barra.pack(fill="x", side="bottom")
        barra.pack_propagate(False)
        tk.Label(barra, textvariable=self.status_var,
                 font=("Segoe UI", 8), fg=TEXT_MUTED,
                 bg="#0A1520").pack(side="left", padx=14)
        if not PIL_DISPONIBLE:
            tk.Label(barra,
                     text="⚠ Para ver fotos instala:  pip install Pillow",
                     font=("Segoe UI", 8), fg=ACCENT_RED,
                     bg="#0A1520").pack(side="right", padx=14)

    # ─── Hover util ───────────────────────────────────────────────────────────
    def _hover(self, btn, color_normal, color_hover):
        btn.bind("<Enter>", lambda _e: btn.config(bg=color_hover))
        btn.bind("<Leave>", lambda _e: btn.config(bg=color_normal))

    # ─── Lógica de negocio ────────────────────────────────────────────────────
    def _registrar(self):
        nombre = self._obtener_valor("nombre")
        c1_str = self._obtener_valor("costo1")
        c2_str = self._obtener_valor("costo2")
        pv_str = self._obtener_valor("pventa")

        if not all([nombre, c1_str, c2_str, pv_str]):
            messagebox.showwarning("Campos incompletos",
                                   "Por favor completa todos los campos.")
            return
        try:
            c1 = float(c1_str)
            c2 = float(c2_str)
            pv = float(pv_str)
        except ValueError:
            messagebox.showerror("Error de formato",
                                 "Los costos y precio deben ser valores numéricos.")
            return
        if any(v <= 0 for v in (c1, c2, pv)):
            messagebox.showwarning("Valores inválidos",
                                   "Todos los valores deben ser mayores a 0.")
            return

        # Determinar proveedor más conveniente
        if c1 < c2:
            mejor_prov, mejor_costo = "Proveedor 1", c1
        elif c2 < c1:
            mejor_prov, mejor_costo = "Proveedor 2", c2
        else:
            mejor_prov, mejor_costo = "Empate", c1

        ganancia     = pv - mejor_costo
        rentabilidad = (ganancia / mejor_costo) * 100

        self.productos.append({
            "nombre":       nombre,
            "costo1":       c1,
            "costo2":       c2,
            "precio_venta": pv,
            "mejor_prov":   mejor_prov,
            "mejor_costo":  mejor_costo,
            "ganancia":     ganancia,
            "rentabilidad": rentabilidad,
            "foto_b64":     self._foto_b64,
        })
        self._actualizar_tabla()
        self._limpiar_form()
        self._set_status(f"✔ '{nombre}' registrado — Rentabilidad: {rentabilidad:.2f}%")

    def _actualizar_tabla(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        for i, p in enumerate(self.productos):
            tag_fila  = "odd" if i % 2 == 0 else "even"
            rent      = p["rentabilidad"]
            tag_color = "high" if rent >= 40 else ("medium" if rent >= 20 else "low")
            icono     = "📷" if p.get("foto_b64") else "  —"
            self.tree.insert("", "end",
                             values=(
                                 icono,
                                 p["nombre"],
                                 p["mejor_prov"],
                                 f"${p['mejor_costo']:.2f}",
                                 f"${p['precio_venta']:.2f}",
                                 f"${p['ganancia']:.2f}",
                                 f"{p['rentabilidad']:.2f}%",
                             ),
                             tags=(tag_fila, tag_color))

        self.lbl_count.config(text=f"{len(self.productos)} registro(s)")
        self._actualizar_resumen()

    def _actualizar_resumen(self):
        n = len(self.productos)
        self.lbl_total.config(text=str(n))
        if n:
            promedio = sum(p["rentabilidad"] for p in self.productos) / n
            mayor    = max(p["ganancia"]     for p in self.productos)
            self.lbl_avg.config( text=f"{promedio:.2f}%")
            self.lbl_best.config(text=f"${mayor:.2f}")
        else:
            self.lbl_avg.config( text="0.00%")
            self.lbl_best.config(text="$0.00")

    def _limpiar_form(self):
        for clave, (entrada, hint) in self.entries.items():
            entrada.delete(0, "end")
            entrada.insert(0, hint)
            entrada.config(fg=TEXT_MUTED)
        self._quitar_foto()

    # ─── Doble clic → ver foto ampliada ───────────────────────────────────────
    def _doble_clic(self, _event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        idx = self.tree.index(seleccion[0])
        p   = self.productos[idx]
        if not p.get("foto_b64"):
            messagebox.showinfo("Sin foto",
                                f"'{p['nombre']}' no tiene foto registrada.")
            return
        self._ver_foto(p)

    def _ver_foto(self, p):
        ventana = tk.Toplevel(self)
        ventana.title(f"📷  {p['nombre']}")
        ventana.configure(bg=BG_DARK)
        ventana.grab_set()
        ventana.resizable(False, False)

        if PIL_DISPONIBLE:
            b64 = p.get("foto_b64", "")
            if b64 and len(b64) > 260:
                try:
                    datos = base64.b64decode(b64)
                    img   = Image.open(io.BytesIO(datos)).convert("RGB")
                    img   = _resize_pil(img, 500, 360)
                    photo = ImageTk.PhotoImage(img)
                    lbl   = tk.Label(ventana, image=photo, bg=BG_DARK)
                    lbl.image = photo   # mantener referencia
                    lbl.pack(padx=24, pady=(24, 8))
                except Exception:
                    self._sin_preview(ventana)
            else:
                self._sin_preview(ventana)
        else:
            self._sin_preview(ventana)

        tk.Label(ventana, text=p["nombre"],
                 font=("Segoe UI", 14, "bold"), fg=TEXT_WHITE, bg=BG_DARK).pack()
        detalle = (f"Mejor proveedor: {p['mejor_prov']}   |   "
                   f"Ganancia: ${p['ganancia']:.2f}   |   "
                   f"Rentabilidad: {p['rentabilidad']:.2f}%")
        tk.Label(ventana, text=detalle,
                 font=("Segoe UI", 10), fg=ACCENT_GREEN, bg=BG_DARK
                 ).pack(pady=(6, 16))
        tk.Button(ventana, text="  Cerrar  ",
                  font=("Segoe UI", 10, "bold"),
                  bg=ACCENT_BLUE, fg=TEXT_WHITE,
                  relief="flat", cursor="hand2", padx=24, pady=6,
                  command=ventana.destroy).pack(pady=(0, 20))

    def _sin_preview(self, ventana):
        tk.Label(ventana,
                 text="🖼\n\nVista previa no disponible.\nInstala Pillow:  pip install Pillow",
                 fg=TEXT_MUTED, bg=BG_DARK,
                 font=("Segoe UI", 11), justify="center").pack(padx=80, pady=50)

    # ─── Botón: Ver productos (detalle completo) ───────────────────────────────
    def _ver_productos(self):
        if not self.productos:
            messagebox.showinfo("Sin productos", "No hay productos registrados.")
            return
        ventana = tk.Toplevel(self)
        ventana.title("Detalle de Productos")
        ventana.configure(bg=BG_DARK)
        ventana.geometry("720x500")
        ventana.grab_set()

        tk.Label(ventana, text="Detalle completo de productos",
                 font=("Segoe UI", 13, "bold"),
                 fg=TEXT_WHITE, bg=BG_DARK).pack(pady=(18, 4))
        tk.Frame(ventana, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 12))

        texto = tk.Text(ventana, bg=BG_CARD, fg=TEXT_WHITE,
                        font=("Consolas", 10), relief="flat",
                        bd=0, padx=16, pady=12, wrap="word")
        texto.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        for i, p in enumerate(self.productos, 1):
            tiene_foto = "✔ Sí" if p.get("foto_b64") else "✖ No"
            texto.insert("end", f"[{i}] {p['nombre']}\n", "titulo")
            texto.insert("end",
                f"  Foto:          {tiene_foto}\n"
                f"  Costo P1:      ${p['costo1']:.2f}\n"
                f"  Costo P2:      ${p['costo2']:.2f}\n"
                f"  Mejor Prov.:   {p['mejor_prov']} (${p['mejor_costo']:.2f})\n"
                f"  Precio Venta:  ${p['precio_venta']:.2f}\n"
                f"  Ganancia:      ${p['ganancia']:.2f}\n"
                f"  Rentabilidad:  {p['rentabilidad']:.2f}%\n\n")

        texto.tag_configure("titulo", foreground=ACCENT_BLUE,
                            font=("Consolas", 10, "bold"))
        texto.config(state="disabled")

        tk.Button(ventana, text="Cerrar", font=("Segoe UI", 10),
                  bg=ACCENT_BLUE, fg=TEXT_WHITE, relief="flat",
                  cursor="hand2", padx=24, pady=6,
                  command=ventana.destroy).pack(pady=(0, 14))

    # ─── Botón: Eliminar ───────────────────────────────────────────────────────
    def _eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección",
                                   "Selecciona un producto en la tabla.")
            return
        idx    = self.tree.index(seleccion[0])
        nombre = self.productos[idx]["nombre"]
        if messagebox.askyesno("Confirmar eliminación", f"¿Eliminar '{nombre}'?"):
            self.productos.pop(idx)
            self._actualizar_tabla()
            self._set_status(f"🗑 Producto '{nombre}' eliminado.")

    # ─── Botón: Guardar ────────────────────────────────────────────────────────
    def _guardar(self):
        if not self.productos:
            messagebox.showinfo("Sin datos", "No hay productos para guardar.")
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
            title="Guardar datos")
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(self.productos, archivo, ensure_ascii=False, indent=2)
            self._set_status(f"💾 Guardado en {os.path.basename(ruta)}")
            messagebox.showinfo("Guardado", f"Datos guardados en:\n{ruta}")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo guardar:\n{ex}")

    # ─── Botón: Cargar ─────────────────────────────────────────────────────────
    def _cargar(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
            title="Cargar datos")
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if not isinstance(datos, list):
                raise ValueError("El archivo no tiene el formato esperado.")
            self.productos = datos
            self._actualizar_tabla()
            self._set_status(
                f"📂 {len(datos)} producto(s) cargado(s) desde {os.path.basename(ruta)}")
        except Exception as ex:
            messagebox.showerror("Error al cargar", f"No se pudo cargar:\n{ex}")

    # ─── Botón: Salir ──────────────────────────────────────────────────────────
    def _salir(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar el sistema?"):
            self.destroy()

    # ─── Ordenar tabla ────────────────────────────────────────────────────────
    def _ordenar(self, columna):
        invertir = self._sort_rev.get(columna, False)
        mapa = {
            "producto":     "nombre",
            "proveedor":    "mejor_prov",
            "costo_mejor":  "mejor_costo",
            "precio_venta": "precio_venta",
            "ganancia":     "ganancia",
            "rentabilidad": "rentabilidad",
        }
        clave = mapa.get(columna)
        if clave:
            self.productos.sort(key=lambda p: p[clave], reverse=invertir)
            self._sort_rev[columna] = not invertir
            self._actualizar_tabla()

    # ─── Estado ───────────────────────────────────────────────────────────────
    def _set_status(self, mensaje):
        self.status_var.set(mensaje)


# ─── Punto de entrada ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SistemaRentabilidad()
    app.mainloop()
