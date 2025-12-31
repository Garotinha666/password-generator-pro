import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import json
import os
from datetime import datetime
import hashlib
from cryptography.fernet import Fernet
import pyperclip

class PasswordGeneratorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Generator Pro")
        self.root.geometry("800x700")
        self.root.configure(bg="#0f0f1e")
        self.root.resizable(False, False)
        
        # Configurações
        self.config_file = "passwords.enc"
        self.key_file = ".key"
        self.cipher = self.load_or_create_key()
        
        # Variáveis
        self.length_var = tk.IntVar(value=16)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=True)
        
        self.setup_styles()
        self.create_ui()
        self.load_passwords()
        
    def load_or_create_key(self):
        """Carrega ou cria chave de criptografia"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        return Fernet(key)
    
    def setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores
        bg_dark = "#0f0f1e"
        bg_medium = "#1a1a2e"
        bg_light = "#16213e"
        accent = "#0f4c75"
        accent_bright = "#3282b8"
        text_color = "#ffffff"
        
        style.configure("TFrame", background=bg_dark)
        style.configure("TLabel", background=bg_dark, foreground=text_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground=accent_bright)
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=accent_bright)
        
        style.configure("TButton", 
                       font=("Segoe UI", 10, "bold"),
                       background=accent,
                       foreground=text_color,
                       borderwidth=0,
                       focuscolor='none',
                       padding=10)
        style.map("TButton",
                 background=[('active', accent_bright), ('pressed', accent)])
        
        style.configure("Accent.TButton",
                       background=accent_bright,
                       foreground=text_color)
        
        style.configure("TCheckbutton",
                       background=bg_dark,
                       foreground=text_color,
                       font=("Segoe UI", 10))
        
    def create_ui(self):
        """Cria interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="🔐 Password Generator Pro", style="Title.TLabel")
        title.pack(pady=(0, 20))
        
        # Notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba Gerador
        self.create_generator_tab(notebook)
        
        # Aba Histórico
        self.create_history_tab(notebook)
        
        # Aba Força da Senha
        self.create_strength_tab(notebook)
        
    def create_generator_tab(self, notebook):
        """Cria aba de geração de senhas"""
        gen_frame = ttk.Frame(notebook, padding="15")
        notebook.add(gen_frame, text="⚡ Gerar Senha")
        
        # Configurações
        config_frame = ttk.LabelFrame(gen_frame, text="Configurações", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Comprimento
        length_frame = ttk.Frame(config_frame)
        length_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(length_frame, text=f"Comprimento:").pack(side=tk.LEFT)
        
        length_scale = tk.Scale(length_frame, 
                               from_=8, to=64,
                               orient=tk.HORIZONTAL,
                               variable=self.length_var,
                               bg="#1a1a2e", fg="#ffffff",
                               highlightthickness=0,
                               length=200,
                               command=self.update_length_label)
        length_scale.pack(side=tk.LEFT, padx=10)
        
        self.length_label = ttk.Label(length_frame, text="16 caracteres")
        self.length_label.pack(side=tk.LEFT)
        
        # Opções
        options_frame = ttk.Frame(config_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(options_frame, text="Maiúsculas (A-Z)", 
                       variable=self.use_uppercase).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="Minúsculas (a-z)", 
                       variable=self.use_lowercase).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="Números (0-9)", 
                       variable=self.use_digits).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="Símbolos (!@#$%)", 
                       variable=self.use_symbols).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="Excluir caracteres ambíguos (0, O, l, 1)", 
                       variable=self.exclude_ambiguous).pack(anchor=tk.W, pady=3)
        
        # Resultado
        result_frame = ttk.LabelFrame(gen_frame, text="Senha Gerada", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.password_display = tk.Text(result_frame,
                                       height=3,
                                       font=("Consolas", 14, "bold"),
                                       bg="#1a1a2e",
                                       fg="#3282b8",
                                       wrap=tk.WORD,
                                       relief=tk.FLAT,
                                       padx=10,
                                       pady=10)
        self.password_display.pack(fill=tk.BOTH, expand=True)
        
        # Info de força
        self.strength_info = ttk.Label(result_frame, text="", font=("Segoe UI", 10))
        self.strength_info.pack(pady=(10, 0))
        
        # Botões
        button_frame = ttk.Frame(gen_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="🎲 Gerar Senha", 
                  command=self.generate_password,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📋 Copiar", 
                  command=self.copy_password).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="💾 Salvar", 
                  command=self.save_password_dialog).pack(side=tk.LEFT, padx=5)
        
    def create_history_tab(self, notebook):
        """Cria aba de histórico"""
        hist_frame = ttk.Frame(notebook, padding="15")
        notebook.add(hist_frame, text="📜 Histórico")
        
        # Lista de senhas
        list_frame = ttk.LabelFrame(hist_frame, text="Senhas Salvas", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.password_listbox = tk.Listbox(list_frame,
                                           font=("Consolas", 10),
                                           bg="#1a1a2e",
                                           fg="#ffffff",
                                           selectmode=tk.SINGLE,
                                           yscrollcommand=scrollbar.set,
                                           relief=tk.FLAT,
                                           highlightthickness=0)
        self.password_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.password_listbox.yview)
        
        # Detalhes
        detail_frame = ttk.LabelFrame(hist_frame, text="Detalhes", padding="10")
        detail_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.detail_text = scrolledtext.ScrolledText(detail_frame,
                                                     height=6,
                                                     font=("Consolas", 9),
                                                     bg="#1a1a2e",
                                                     fg="#ffffff",
                                                     wrap=tk.WORD,
                                                     relief=tk.FLAT)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # Botões
        button_frame = ttk.Frame(hist_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="👁️ Ver Senha", 
                  command=self.view_password).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📋 Copiar Senha", 
                  command=self.copy_saved_password).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🗑️ Deletar", 
                  command=self.delete_password).pack(side=tk.LEFT, padx=5)
        
        # Bind selection
        self.password_listbox.bind('<<ListboxSelect>>', self.on_password_select)
        
    def create_strength_tab(self, notebook):
        """Cria aba de análise de força"""
        strength_frame = ttk.Frame(notebook, padding="15")
        notebook.add(strength_frame, text="💪 Analisar Força")
        
        # Input
        input_frame = ttk.LabelFrame(strength_frame, text="Digite uma senha para analisar", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.test_password_entry = tk.Entry(input_frame,
                                            font=("Consolas", 12),
                                            bg="#1a1a2e",
                                            fg="#ffffff",
                                            insertbackground="#ffffff",
                                            relief=tk.FLAT,
                                            show="*")
        self.test_password_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(input_frame, text="🔍 Analisar", 
                  command=self.analyze_strength).pack()
        
        # Resultado
        result_frame = ttk.LabelFrame(strength_frame, text="Análise", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.analysis_text = scrolledtext.ScrolledText(result_frame,
                                                       font=("Consolas", 10),
                                                       bg="#1a1a2e",
                                                       fg="#ffffff",
                                                       wrap=tk.WORD,
                                                       relief=tk.FLAT)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
        
    def update_length_label(self, value):
        """Atualiza label de comprimento"""
        self.length_label.config(text=f"{int(float(value))} caracteres")
        
    def generate_password(self):
        """Gera senha com base nas configurações"""
        length = self.length_var.get()
        
        # Monta conjunto de caracteres
        chars = ""
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        if self.exclude_ambiguous.get():
            ambiguous = "0Ol1"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        if not chars:
            messagebox.showerror("Erro", "Selecione ao menos uma opção de caracteres!")
            return
            
        # Gera senha
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Exibe
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(1.0, password)
        
        # Calcula força
        strength, color = self.calculate_strength(password)
        self.strength_info.config(text=f"Força: {strength}", foreground=color)
        
    def calculate_strength(self, password):
        """Calcula força da senha"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
            
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 2
            
        if score <= 3:
            return "Fraca 😟", "#ff4444"
        elif score <= 5:
            return "Média 😐", "#ffaa00"
        elif score <= 7:
            return "Forte 😊", "#88cc00"
        else:
            return "Muito Forte 🔥", "#00ff00"
            
    def copy_password(self):
        """Copia senha para clipboard"""
        password = self.password_display.get(1.0, tk.END).strip()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Sucesso", "Senha copiada para área de transferência!")
        else:
            messagebox.showwarning("Aviso", "Nenhuma senha para copiar!")
            
    def save_password_dialog(self):
        """Dialog para salvar senha"""
        password = self.password_display.get(1.0, tk.END).strip()
        if not password:
            messagebox.showwarning("Aviso", "Gere uma senha primeiro!")
            return
            
        # Dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Salvar Senha")
        dialog.geometry("400x200")
        dialog.configure(bg="#0f0f1e")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nome/Descrição:").pack(pady=(20, 5))
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        ttk.Label(dialog, text="Categoria (opcional):").pack(pady=(10, 5))
        category_entry = ttk.Entry(dialog, width=40)
        category_entry.pack(pady=5)
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Aviso", "Digite um nome!")
                return
            self.save_password(password, name, category_entry.get().strip())
            dialog.destroy()
            
        ttk.Button(dialog, text="💾 Salvar", command=save).pack(pady=20)
        
    def save_password(self, password, name, category=""):
        """Salva senha criptografada"""
        passwords = self.load_passwords_data()
        
        entry = {
            "name": name,
            "password": password,
            "category": category,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "strength": self.calculate_strength(password)[0]
        }
        
        passwords.append(entry)
        
        # Criptografa e salva
        encrypted = self.cipher.encrypt(json.dumps(passwords).encode())
        with open(self.config_file, 'wb') as f:
            f.write(encrypted)
            
        self.load_passwords()
        messagebox.showinfo("Sucesso", f"Senha '{name}' salva com sucesso!")
        
    def load_passwords_data(self):
        """Carrega senhas do arquivo"""
        if not os.path.exists(self.config_file):
            return []
            
        try:
            with open(self.config_file, 'rb') as f:
                encrypted = f.read()
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except:
            return []
            
    def load_passwords(self):
        """Carrega senhas na listbox"""
        self.password_listbox.delete(0, tk.END)
        passwords = self.load_passwords_data()
        
        for pwd in passwords:
            display = f"🔑 {pwd['name']}"
            if pwd.get('category'):
                display += f" [{pwd['category']}]"
            self.password_listbox.insert(tk.END, display)
            
    def on_password_select(self, event):
        """Quando seleciona uma senha"""
        selection = self.password_listbox.curselection()
        if not selection:
            return
            
        idx = selection[0]
        passwords = self.load_passwords_data()
        pwd = passwords[idx]
        
        self.detail_text.delete(1.0, tk.END)
        details = f"""Nome: {pwd['name']}
Categoria: {pwd.get('category', 'N/A')}
Criada em: {pwd['created']}
Força: {pwd['strength']}
Comprimento: {len(pwd['password'])} caracteres"""
        
        self.detail_text.insert(1.0, details)
        
    def view_password(self):
        """Mostra senha selecionada"""
        selection = self.password_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma senha!")
            return
            
        idx = selection[0]
        passwords = self.load_passwords_data()
        pwd = passwords[idx]
        
        messagebox.showinfo("Senha", f"Senha de '{pwd['name']}':\n\n{pwd['password']}")
        
    def copy_saved_password(self):
        """Copia senha salva"""
        selection = self.password_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma senha!")
            return
            
        idx = selection[0]
        passwords = self.load_passwords_data()
        pwd = passwords[idx]
        
        pyperclip.copy(pwd['password'])
        messagebox.showinfo("Sucesso", f"Senha de '{pwd['name']}' copiada!")
        
    def delete_password(self):
        """Deleta senha"""
        selection = self.password_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma senha!")
            return
            
        idx = selection[0]
        passwords = self.load_passwords_data()
        pwd = passwords[idx]
        
        if messagebox.askyesno("Confirmar", f"Deletar senha '{pwd['name']}'?"):
            passwords.pop(idx)
            
            encrypted = self.cipher.encrypt(json.dumps(passwords).encode())
            with open(self.config_file, 'wb') as f:
                f.write(encrypted)
                
            self.load_passwords()
            self.detail_text.delete(1.0, tk.END)
            messagebox.showinfo("Sucesso", "Senha deletada!")
            
    def analyze_strength(self):
        """Analisa força de senha"""
        password = self.test_password_entry.get()
        
        if not password:
            messagebox.showwarning("Aviso", "Digite uma senha!")
            return
            
        self.analysis_text.delete(1.0, tk.END)
        
        # Análise
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        strength, _ = self.calculate_strength(password)
        
        # Tempo estimado para quebrar (simplificado)
        charset_size = 0
        if has_lower: charset_size += 26
        if has_upper: charset_size += 26
        if has_digit: charset_size += 10
        if has_symbol: charset_size += 20
        
        combinations = charset_size ** length
        
        analysis = f"""╔══════════════════════════════════════════╗
║         ANÁLISE DE FORÇA DA SENHA        ║
╚══════════════════════════════════════════╝

📏 Comprimento: {length} caracteres
   {'✅ Bom' if length >= 12 else '⚠️ Recomendado: 12+'}

🔤 Composição:
   Maiúsculas (A-Z): {'✅ Sim' if has_upper else '❌ Não'}
   Minúsculas (a-z): {'✅ Sim' if has_lower else '❌ Não'}
   Números (0-9):    {'✅ Sim' if has_digit else '❌ Não'}
   Símbolos (!@#$):  {'✅ Sim' if has_symbol else '❌ Não'}

💪 Força: {strength}

🔢 Combinações possíveis: {combinations:,.0f}

⏱️ Tempo estimado para quebrar:
   (força bruta, 1 bilhão de tentativas/seg)
   {self.estimate_crack_time(combinations)}

💡 Recomendações:
"""
        
        recommendations = []
        if length < 12:
            recommendations.append("   • Use pelo menos 12 caracteres")
        if not has_upper:
            recommendations.append("   • Adicione letras maiúsculas")
        if not has_lower:
            recommendations.append("   • Adicione letras minúsculas")
        if not has_digit:
            recommendations.append("   • Adicione números")
        if not has_symbol:
            recommendations.append("   • Adicione símbolos especiais")
            
        if recommendations:
            analysis += "\n".join(recommendations)
        else:
            analysis += "   ✅ Senha excelente!"
            
        self.analysis_text.insert(1.0, analysis)
        
    def estimate_crack_time(self, combinations):
        """Estima tempo para quebrar senha"""
        attempts_per_sec = 1_000_000_000
        seconds = combinations / attempts_per_sec
        
        if seconds < 1:
            return "< 1 segundo"
        elif seconds < 60:
            return f"{seconds:.0f} segundos"
        elif seconds < 3600:
            return f"{seconds/60:.0f} minutos"
        elif seconds < 86400:
            return f"{seconds/3600:.0f} horas"
        elif seconds < 31536000:
            return f"{seconds/86400:.0f} dias"
        else:
            years = seconds / 31536000
            if years < 1000:
                return f"{years:.0f} anos"
            elif years < 1000000:
                return f"{years/1000:.0f} mil anos"
            elif years < 1000000000:
                return f"{years/1000000:.0f} milhões de anos"
            else:
                return "Trilhões de anos"

def main():
    root = tk.Tk()
    app = PasswordGeneratorPro(root)
    root.mainloop()

if __name__ == "__main__":
    main()
