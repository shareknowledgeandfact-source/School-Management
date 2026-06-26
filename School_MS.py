import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

# ── Data ─────────────────────────────────────────────────────────────────────
DATABASE = "school_database.json"
data = {"students": [], "teachers": []}

if Path(DATABASE).exists():
    content = Path(DATABASE).read_text()
    if content.strip():
        data = json.loads(content)


def save():
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


def validate_email(email):
    return "@" in email and "." in email


def initials(name):
    parts = name.strip().split()
    return "".join(p[0] for p in parts).upper()[:2] if parts else "?"


# ── Theme / Colors ────────────────────────────────────────────────────────────
BG       = "#F5F5F5"
WHITE    = "#FFFFFF"
SIDEBAR  = "#FFFFFF"
ACCENT   = "#4F46E5"
ACCENT_H = "#4338CA"
GREEN    = "#059669"
ORANGE   = "#D97706"
RED      = "#DC2626"
BORDER   = "#E5E5E5"
TEXT     = "#1A1A1A"
MUTED    = "#9CA3AF"
BADGE_B  = "#EDE9FE"
BADGE_G  = "#D1FAE5"
BADGE_O  = "#FEF3C7"
BADGE_R  = "#FEE2E2"

FONT       = ("Segoe UI", 11)
FONT_SM    = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 9, "bold")
FONT_H1    = ("Segoe UI", 14, "bold")
FONT_NAV   = ("Segoe UI", 11)
FONT_STAT  = ("Segoe UI", 26, "bold")


# ── Helpers ───────────────────────────────────────────────────────────────────
def make_entry(parent, width=28):
    e = tk.Entry(parent, font=FONT, bd=0, relief="flat",
                 bg=WHITE, fg=TEXT, insertbackground=TEXT,
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT, width=width)
    return e


def make_button(parent, text, command, bg=ACCENT, fg="white", width=18):
    btn = tk.Button(parent, text=text, command=command,
                    font=("Segoe UI", 11, "bold"),
                    bg=bg, fg=fg, activebackground=ACCENT_H,
                    activeforeground="white", bd=0, relief="flat",
                    cursor="hand2", padx=14, pady=8, width=width)
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_H))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def card_frame(parent, padx=20, pady=16):
    outer = tk.Frame(parent, bg=BORDER, bd=0)
    inner = tk.Frame(outer, bg=WHITE, bd=0)
    inner.pack(padx=1, pady=1, fill="both", expand=True)
    return outer, inner


def section_label(parent, text):
    tk.Label(parent, text=text, font=("Segoe UI", 10, "bold"),
             bg=parent["bg"], fg=MUTED).pack(anchor="w", pady=(0, 4))


def toast(root, msg, error=False):
    t = tk.Toplevel(root)
    t.overrideredirect(True)
    t.attributes("-topmost", True)
    color = RED if error else "#1A1A1A"
    frame = tk.Frame(t, bg=color, padx=16, pady=10)
    frame.pack()
    tk.Label(frame, text=("✕  " if error else "✓  ") + msg,
             font=FONT, bg=color, fg="white").pack()
    # Position bottom-right
    root.update_idletasks()
    w, h = 280, 44
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    t.geometry(f"{w}x{h}+{sw - w - 24}+{sh - h - 60}")
    root.after(2500, t.destroy)


# ── Treeview style ────────────────────────────────────────────────────────────
def style_tree(tree):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=WHITE, foreground=TEXT,
                    rowheight=36, fieldbackground=WHITE,
                    borderwidth=0, font=FONT_SM)
    style.configure("Custom.Treeview.Heading",
                    background="#F9FAFB", foreground=MUTED,
                    relief="flat", font=("Segoe UI", 9, "bold"),
                    padding=(8, 6))
    style.map("Custom.Treeview",
              background=[("selected", "#EDE9FE")],
              foreground=[("selected", ACCENT)])
    tree.configure(style="Custom.Treeview")


# ── App ───────────────────────────────────────────────────────────────────────
class SchoolApp:
    def __init__(self, root):
        self.root = root
        root.title("School Management System")
        root.geometry("920x620")
        root.configure(bg=BG)
        root.resizable(True, True)

        self._build_layout()
        self._show_panel("dashboard")

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=200, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Right border on sidebar
        tk.Frame(self.root, bg=BORDER, width=1).pack(side="left", fill="y")

        # Main
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self._build_sidebar()

        # Topbar
        self.topbar = tk.Frame(self.main, bg=WHITE, height=56)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        tk.Frame(self.main, bg=BORDER, height=1).pack(fill="x")

        self.page_title = tk.Label(self.topbar, text="Dashboard",
                                   font=FONT_H1, bg=WHITE, fg=TEXT)
        self.page_title.pack(side="left", padx=20, pady=0)

        # Content area
        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=20, pady=16)

        # Panels
        self.panels = {}
        self.panels["dashboard"] = self._panel_dashboard()
        self.panels["students"]  = self._panel_students()
        self.panels["teachers"]  = self._panel_teachers()
        self.panels["grades"]    = self._panel_grades()

    def _build_sidebar(self):
        # Logo
        logo = tk.Frame(self.sidebar, bg=SIDEBAR)
        logo.pack(fill="x", padx=16, pady=(20, 12))
        tk.Label(logo, text="🏫  School MS", font=("Segoe UI", 13, "bold"),
                 bg=SIDEBAR, fg=TEXT).pack(anchor="w")
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=12)

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "⊞  Dashboard"),
            ("students",  "👥  Students"),
            ("teachers",  "🖥  Teachers"),
            ("grades",    "🏅  Grades"),
        ]
        for key, label in nav_items:
            btn = tk.Label(self.sidebar, text=label, font=FONT_NAV,
                           bg=SIDEBAR, fg=TEXT, cursor="hand2",
                           anchor="w", padx=16, pady=10)
            btn.pack(fill="x", padx=8, pady=2)
            btn.bind("<Button-1>", lambda e, k=key: self._show_panel(k))
            btn.bind("<Enter>", lambda e, b=btn, k=key: self._nav_hover(b, k, True))
            btn.bind("<Leave>", lambda e, b=btn, k=key: self._nav_hover(b, k, False))
            self.nav_buttons[key] = btn

    def _nav_hover(self, btn, key, entering):
        if key == self.current_panel:
            return
        btn.config(bg="#F3F4F6" if entering else SIDEBAR)

    def _show_panel(self, key):
        self.current_panel = key
        titles = {"dashboard": "Dashboard", "students": "Students",
                  "teachers": "Teachers", "grades": "Grades"}
        self.page_title.config(text=titles[key])

        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.config(bg=BADGE_B, fg=ACCENT, font=("Segoe UI", 11, "bold"))
            else:
                btn.config(bg=SIDEBAR, fg=TEXT, font=FONT_NAV)

        for k, panel in self.panels.items():
            panel.pack_forget()
        self.panels[key].pack(fill="both", expand=True)

        refresh = {
            "dashboard": self._refresh_dashboard,
            "students":  self._refresh_students,
            "teachers":  self._refresh_teachers,
            "grades":    self._refresh_grades,
        }
        refresh[key]()

    # ── Dashboard panel ───────────────────────────────────────────────────────
    def _panel_dashboard(self):
        frame = tk.Frame(self.content, bg=BG)

        # Stat cards
        stats_row = tk.Frame(frame, bg=BG)
        stats_row.pack(fill="x", pady=(0, 16))

        self.stat_students = self._stat_card(stats_row, "Students", "0", ACCENT)
        self.stat_teachers = self._stat_card(stats_row, "Teachers", "0", GREEN)
        self.stat_grades   = self._stat_card(stats_row, "Grades recorded", "0", ORANGE)

        # Recent students table
        tk.Label(frame, text="Recent students", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 6))

        outer, inner = card_frame(frame)
        outer.pack(fill="x")

        cols = ("Name", "Roll no", "Subject", "Email")
        self.dash_tree = ttk.Treeview(inner, columns=cols, show="headings",
                                       height=6, selectmode="browse")
        style_tree(self.dash_tree)
        for col in cols:
            self.dash_tree.heading(col, text=col)
        self.dash_tree.column("Name", width=200)
        self.dash_tree.column("Roll no", width=80, anchor="center")
        self.dash_tree.column("Subject", width=140)
        self.dash_tree.column("Email", width=200)
        self.dash_tree.pack(fill="both", padx=1, pady=1)

        return frame

    def _stat_card(self, parent, label, value, color):
        outer, inner = card_frame(parent)
        outer.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(inner, text=label, font=("Segoe UI", 9, "bold"),
                 bg=WHITE, fg=MUTED).pack(anchor="w", padx=16, pady=(14, 2))
        val_lbl = tk.Label(inner, text=value, font=FONT_STAT,
                           bg=WHITE, fg=color)
        val_lbl.pack(anchor="w", padx=16, pady=(0, 14))
        return val_lbl

    def _refresh_dashboard(self):
        total_grades = sum(len(s["grades"]) for s in data["students"])
        self.stat_students.config(text=str(len(data["students"])))
        self.stat_teachers.config(text=str(len(data["teachers"])))
        self.stat_grades.config(text=str(total_grades))

        for row in self.dash_tree.get_children():
            self.dash_tree.delete(row)
        for s in reversed(data["students"][-5:]):
            self.dash_tree.insert("", "end", values=(
                s["name"], f"#{s['roll_no']}", s["subject"], s["email"]))

    # ── Students panel ────────────────────────────────────────────────────────
    def _panel_students(self):
        frame = tk.Frame(self.content, bg=BG)

        # Form card
        tk.Label(frame, text="Register student", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 6))
        outer, inner = card_frame(frame)
        outer.pack(fill="x")

        grid = tk.Frame(inner, bg=WHITE)
        grid.pack(padx=16, pady=14, fill="x")

        self.s_name    = self._form_field(grid, "Name", 0, 0)
        self.s_age     = self._form_field(grid, "Age", 0, 1)
        self.s_roll    = self._form_field(grid, "Roll no", 1, 0)
        self.s_subject = self._form_field(grid, "Subject", 1, 1)
        self.s_email   = self._form_field(grid, "Email", 2, 0, span=2)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        btn_row = tk.Frame(inner, bg=WHITE)
        btn_row.pack(padx=16, pady=(0, 14), anchor="w")
        make_button(btn_row, "Register student", self._register_student).pack()

        # Table
        tk.Label(frame, text="All students", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(14, 6))
        outer2, inner2 = card_frame(frame)
        outer2.pack(fill="both", expand=True)

        cols = ("Name", "Roll no", "Age", "Subject", "Email")
        self.student_tree = ttk.Treeview(inner2, columns=cols, show="headings",
                                          height=8, selectmode="browse")
        style_tree(self.student_tree)
        for col in cols:
            self.student_tree.heading(col, text=col)
        self.student_tree.column("Name", width=180)
        self.student_tree.column("Roll no", width=80, anchor="center")
        self.student_tree.column("Age", width=60, anchor="center")
        self.student_tree.column("Subject", width=140)
        self.student_tree.column("Email", width=200)

        sb = ttk.Scrollbar(inner2, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=sb.set)
        self.student_tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)
        sb.pack(side="right", fill="y")

        return frame

    def _register_student(self):
        name    = self.s_name.get().strip()
        subject = self.s_subject.get().strip()
        email   = self.s_email.get().strip()
        try:
            age  = int(self.s_age.get())
            roll = int(self.s_roll.get())
        except ValueError:
            return toast(self.root, "Age and roll no must be numbers", True)
        if not name:
            return toast(self.root, "Name is required", True)
        if not validate_email(email):
            return toast(self.root, "Invalid email address", True)
        if any(s["roll_no"] == roll for s in data["students"]):
            return toast(self.root, "Roll number already exists", True)

        data["students"].append({"name": name, "age": age, "roll_no": roll,
                                  "subject": subject, "email": email, "grades": {}})
        save()
        for e in (self.s_name, self.s_age, self.s_roll, self.s_subject, self.s_email):
            e.delete(0, "end")
        self._refresh_students()
        self._refresh_dashboard()
        toast(self.root, "Student registered")

    def _refresh_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for s in data["students"]:
            self.student_tree.insert("", "end", values=(
                s["name"], f"#{s['roll_no']}", s["age"], s["subject"], s["email"]))

    # ── Teachers panel ────────────────────────────────────────────────────────
    def _panel_teachers(self):
        frame = tk.Frame(self.content, bg=BG)

        tk.Label(frame, text="Register teacher", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 6))
        outer, inner = card_frame(frame)
        outer.pack(fill="x")

        grid = tk.Frame(inner, bg=WHITE)
        grid.pack(padx=16, pady=14, fill="x")

        self.t_name    = self._form_field(grid, "Name", 0, 0)
        self.t_age     = self._form_field(grid, "Age", 0, 1)
        self.t_id      = self._form_field(grid, "Teacher ID", 1, 0)
        self.t_subject = self._form_field(grid, "Subject", 1, 1)
        self.t_email   = self._form_field(grid, "Email", 2, 0, span=2)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        btn_row = tk.Frame(inner, bg=WHITE)
        btn_row.pack(padx=16, pady=(0, 14), anchor="w")
        make_button(btn_row, "Register teacher", self._register_teacher,
                    bg=GREEN).pack()

        tk.Label(frame, text="All teachers", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(14, 6))
        outer2, inner2 = card_frame(frame)
        outer2.pack(fill="both", expand=True)

        cols = ("Name", "ID", "Age", "Subject", "Email")
        self.teacher_tree = ttk.Treeview(inner2, columns=cols, show="headings",
                                          height=8, selectmode="browse")
        style_tree(self.teacher_tree)
        for col in cols:
            self.teacher_tree.heading(col, text=col)
        self.teacher_tree.column("Name", width=180)
        self.teacher_tree.column("ID", width=80, anchor="center")
        self.teacher_tree.column("Age", width=60, anchor="center")
        self.teacher_tree.column("Subject", width=140)
        self.teacher_tree.column("Email", width=200)

        sb = ttk.Scrollbar(inner2, orient="vertical", command=self.teacher_tree.yview)
        self.teacher_tree.configure(yscrollcommand=sb.set)
        self.teacher_tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)
        sb.pack(side="right", fill="y")

        return frame

    def _register_teacher(self):
        name    = self.t_name.get().strip()
        subject = self.t_subject.get().strip()
        email   = self.t_email.get().strip()
        try:
            age  = int(self.t_age.get())
            roll = int(self.t_id.get())
        except ValueError:
            return toast(self.root, "Age and ID must be numbers", True)
        if not name:
            return toast(self.root, "Name is required", True)
        if not validate_email(email):
            return toast(self.root, "Invalid email address", True)
        if any(t["roll_no"] == roll for t in data["teachers"]):
            return toast(self.root, "Teacher ID already exists", True)

        data["teachers"].append({"name": name, "age": age, "roll_no": roll,
                                  "subject": subject, "email": email})
        save()
        for e in (self.t_name, self.t_age, self.t_id, self.t_subject, self.t_email):
            e.delete(0, "end")
        self._refresh_teachers()
        toast(self.root, "Teacher registered")

    def _refresh_teachers(self):
        for row in self.teacher_tree.get_children():
            self.teacher_tree.delete(row)
        for t in data["teachers"]:
            self.teacher_tree.insert("", "end", values=(
                t["name"], f"#{t['roll_no']}", t["age"], t["subject"], t["email"]))

    # ── Grades panel ──────────────────────────────────────────────────────────
    def _panel_grades(self):
        frame = tk.Frame(self.content, bg=BG)

        tk.Label(frame, text="Add grade", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 6))
        outer, inner = card_frame(frame)
        outer.pack(fill="x")

        grid = tk.Frame(inner, bg=WHITE)
        grid.pack(padx=16, pady=14, fill="x")

        self.g_roll    = self._form_field(grid, "Roll no", 0, 0)
        self.g_subject = self._form_field(grid, "Subject", 0, 1)
        self.g_marks   = self._form_field(grid, "Marks", 1, 0)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        btn_row = tk.Frame(inner, bg=WHITE)
        btn_row.pack(padx=16, pady=(0, 14), anchor="w")
        make_button(btn_row, "Save grade", self._add_grade, bg=ORANGE).pack()

        tk.Label(frame, text="Student grades", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(14, 6))
        outer2, inner2 = card_frame(frame)
        outer2.pack(fill="both", expand=True)

        cols = ("Name", "Roll no", "Subject", "Marks", "Grade")
        self.grade_tree = ttk.Treeview(inner2, columns=cols, show="headings",
                                        height=10, selectmode="browse")
        style_tree(self.grade_tree)
        for col in cols:
            self.grade_tree.heading(col, text=col)
        self.grade_tree.column("Name", width=180)
        self.grade_tree.column("Roll no", width=80, anchor="center")
        self.grade_tree.column("Subject", width=150)
        self.grade_tree.column("Marks", width=80, anchor="center")
        self.grade_tree.column("Grade", width=80, anchor="center")

        sb = ttk.Scrollbar(inner2, orient="vertical", command=self.grade_tree.yview)
        self.grade_tree.configure(yscrollcommand=sb.set)
        self.grade_tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)
        sb.pack(side="right", fill="y")

        return frame

    def _add_grade(self):
        subject = self.g_subject.get().strip()
        try:
            roll  = int(self.g_roll.get())
            marks = float(self.g_marks.get())
        except ValueError:
            return toast(self.root, "Roll no and marks must be numbers", True)
        if not subject:
            return toast(self.root, "Subject is required", True)

        student = next((s for s in data["students"] if s["roll_no"] == roll), None)
        if not student:
            return toast(self.root, "Student not found", True)

        student["grades"][subject] = marks
        save()
        for e in (self.g_roll, self.g_subject, self.g_marks):
            e.delete(0, "end")
        self._refresh_grades()
        self._refresh_dashboard()
        toast(self.root, "Grade saved")

    def _grade_letter(self, m):
        if m >= 90: return "A+"
        if m >= 80: return "A"
        if m >= 70: return "B"
        if m >= 60: return "C"
        if m >= 50: return "D"
        return "F"

    def _refresh_grades(self):
        for row in self.grade_tree.get_children():
            self.grade_tree.delete(row)
        for s in data["students"]:
            for subject, marks in s["grades"].items():
                self.grade_tree.insert("", "end", values=(
                    s["name"], f"#{s['roll_no']}", subject,
                    marks, self._grade_letter(marks)))

    # ── Form field helper ─────────────────────────────────────────────────────
    def _form_field(self, parent, label, row, col, span=1):
        wrap = tk.Frame(parent, bg=WHITE)
        wrap.grid(row=row, column=col, columnspan=span,
                  padx=(0, 12 if col == 0 else 0), pady=6, sticky="ew")
        tk.Label(wrap, text=label, font=FONT_LABEL,
                 bg=WHITE, fg=MUTED).pack(anchor="w")
        entry = make_entry(wrap, width=24)
        entry.pack(fill="x", ipady=5, pady=(3, 0))
        return entry


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolApp(root)
    root.mainloop()