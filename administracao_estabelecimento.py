import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class ConfiguracoesEstabelecimentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurações")

        # Configurar o estilo
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12), padding=(5, 5), foreground='#1f497d')  # Cor: Azul Salesforce
        self.style.configure('TEntry', font=('Arial', 12), padding=(5, 5))
        self.style.configure('TButton', font=('Arial', 12, 'bold'), padding=(5, 5), foreground='#ffffff', background='#0070e0')  # Cor: Azul Salesforce

        # Frame principal
        self.frame_principal = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.frame_principal.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Dados de Empresa
        self.frame_empresa = ttk.LabelFrame(self.frame_principal, text="Dados", padding=(10, 10), labelanchor='n')
        self.frame_principal.add(self.frame_empresa)

        campos_empresa = [
            ("Nome:", "Nome_Estacionamento", ttk.Entry),
            ("CNPJ:", "CNPJ_Estacionamento", ttk.Entry),
            ("E-mail:", "Email_Estacionamento", ttk.Entry),
            ("Telefone:", "Telefone_Estacionamento", ttk.Entry),
            ("Endereço:", "Endereco_Estacionamento", ttk.Entry)
        ]

        for label, field, widget_type in campos_empresa:
            ttk.Label(self.frame_empresa, text=label, foreground='#000000').grid(row=len(self.frame_empresa.winfo_children()), column=0, sticky="w", pady=(10, 0))
            entry = widget_type(self.frame_empresa, style='TEntry')
            entry.grid(row=len(self.frame_empresa.winfo_children()) - 1, column=1, padx=10, pady=(10, 0))
            setattr(self, f"entry_{field}", entry)

        # Dados Financeiros
        self.frame_financeiro = ttk.LabelFrame(self.frame_principal, text="Financeiros", padding=(10, 10), labelanchor='n')
        self.frame_principal.add(self.frame_financeiro)

        campos_financeiros = [
            ("Tarifa Por Hora:", "Tarifa_Por_Hora", ttk.Entry),
            ("Tarifa Diária:", "Tarifa_Diaria", ttk.Entry),
            ("Tarifa Noturna:", "Tarifa_Noturna", ttk.Entry),
            ("Tarifa Mensal:", "Tarifa_Mensal", ttk.Entry)
        ]

        for label, field, widget_type in campos_financeiros:
            ttk.Label(self.frame_financeiro, text=label, foreground='#000000').grid(row=len(self.frame_financeiro.winfo_children()), column=0, sticky="w", pady=(10, 0))
            entry = widget_type(self.frame_financeiro, style='TEntry')
            entry.grid(row=len(self.frame_financeiro.winfo_children()) - 1, column=1, padx=10, pady=(10, 0))
            setattr(self, f"entry_{field}", entry)

        # Dados de Funcionamento
        self.frame_funcionamento = ttk.LabelFrame(self.frame_principal, text="Funcionamento", padding=(10, 10), labelanchor='n')
        self.frame_principal.add(self.frame_funcionamento)

        campos_funcionamento = [
            ("Número de Vagas:", "Numero_Vagas", ttk.Entry),
            ("Hora de Abertura:", "Horario_Abertura", ttk.Entry),
            ("Hora de Fechamento:", "Horario_Fechamento", ttk.Entry)
        ]

        for label, field, widget_type in campos_funcionamento:
            ttk.Label(self.frame_funcionamento, text=label, foreground='#000000').grid(row=len(self.frame_funcionamento.winfo_children()), column=0, sticky="w", pady=(10, 0))
            entry = widget_type(self.frame_funcionamento, style='TEntry')
            entry.grid(row=len(self.frame_funcionamento.winfo_children()) - 1, column=1, padx=10, pady=(10, 0))
            setattr(self, f"entry_{field}", entry)

        # Ajustar o peso para redimensionamento
        self.frame_principal.columnconfigure(0, weight=1)

        # Botões
        self.btn_salvar = ttk.Button(root, text="Salvar", style='TButton', command=self.salvar_configuracoes)
        self.btn_salvar.grid(row=1, column=0, pady=10)

        # Carregar dados do banco (se existirem)
        self.carregar_dados_do_banco()

    def carregar_dados_do_banco(self):
        conn = sqlite3.connect('banco_dados.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Configuracoes_Estabelecimento LIMIT 1")
        dados = cursor.fetchone()

        conn.close()

        if dados:
            # Atualizar os campos com os dados do banco
            campos = ["Nome_Estacionamento", "CNPJ_Estacionamento", "Email_Estacionamento", "Telefone_Estacionamento",
                      "Endereco_Estacionamento", "Numero_Vagas", "Horario_Abertura", "Horario_Fechamento",
                      "Tarifa_Por_Hora", "Tarifa_Diaria", "Tarifa_Noturna", "Tarifa_Mensal"]

            for field, value in zip(campos, dados):
                entry = getattr(self, f"entry_{field}", None)
                if entry:
                    entry.insert(0, value)
    
    def salvar_configuracoes(self):
        conn = sqlite3.connect('banco_dados.db')
        cursor = conn.cursor()

        # Verifica se já existem dados no banco
        cursor.execute("SELECT COUNT(*) FROM Configuracoes_Estabelecimento")
        dados_existem = cursor.fetchone()[0] > 0

        campos = ["Nome_Estacionamento", "CNPJ_Estacionamento", "Email_Estacionamento", "Telefone_Estacionamento",
                "Endereco_Estacionamento", "Numero_Vagas", "Horario_Abertura", "Horario_Fechamento",
                "Tarifa_Por_Hora", "Tarifa_Diaria", "Tarifa_Noturna", "Tarifa_Mensal"]

        valores = [getattr(self, f"entry_{field}").get() for field in campos]

        try:
            if dados_existem:
                # Se já existem dados, atualiza
                cursor.execute("UPDATE Configuracoes_Estabelecimento SET "
                            "Nome_Estacionamento=?, CNPJ_Estacionamento=?, Email_Estacionamento=?, "
                            "Telefone_Estacionamento=?, Endereco_Estacionamento=?, Numero_Vagas=?, "
                            "Horario_Abertura=?, Horario_Fechamento=?, Tarifa_Por_Hora=?, Tarifa_Diaria=?, "
                            "Tarifa_Noturna=?, Tarifa_Mensal=?",
                            tuple(valores))
            else:
                # Se não existem dados, insere
                cursor.execute("INSERT INTO Configuracoes_Estabelecimento VALUES "
                            "(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            tuple(valores))

            conn.commit()

            # Exibe a mensagem de sucesso
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")

        except sqlite3.Error as e:
            # Exibe a mensagem de erro
            messagebox.showerror("Erro", f"Erro SQLite: {e}")

        finally:
            conn.close()