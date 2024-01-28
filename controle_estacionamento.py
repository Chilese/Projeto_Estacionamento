import tkinter as tk
from tkinter import ttk
import sqlite3
import os

class EstacionamentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estacionamento")

        # Conectar ao banco de dados
        self.conn = sqlite3.connect('banco_dados.db')
        self.cursor = self.conn.cursor()

        # Criar a tabela
        self.tabela = ttk.Treeview(root, columns=('Vagas', 'Placa', 'Modelo', 'Entrada', 'Permanência', 'Alerta'), show='headings')
        self.tabela.heading('Vagas', text='Vagas')
        self.tabela.heading('Placa', text='Placa')
        self.tabela.heading('Modelo', text='Modelo')
        self.tabela.heading('Entrada', text='Entrada')
        self.tabela.heading('Permanência', text='Permanência')
        self.tabela.heading('Alerta', text='Alerta')

        # Adicionar dados nas colunas "Vagas" e "Placa"
        self.carregar_dados()

        # Colocar a tabela na tela
        self.tabela.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Botão para abrir a janela de registro
        btn_abrir_registro = ttk.Button(root, text="Registrar Veículo", command=self.abrir_registro)
        btn_abrir_registro.grid(row=1, column=0, pady=10)

        # Ajustar o peso para redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def carregar_dados(self):
        # Obter o número de vagas do banco de dados
        self.cursor.execute("SELECT Numero_Vagas FROM Configuracoes_Estabelecimento LIMIT 1")
        resultado = self.cursor.fetchone()

        if resultado:
            numero_vagas = resultado[0]

            # Preencher a coluna "Vagas"
            for vaga in range(1, numero_vagas + 1):
                self.tabela.insert('', 'end', values=(vaga, '', '', '', '', ''))

    def abrir_registro(self):
        # Chamar o script de registro_de_veiculos.py
        os.system('python registro_de_veiculos.py')

    def atualizar_interface_veiculo(self, vaga, placa, modelo):
        # Atualizar a tabela com as informações do veículo registrado
        # Encontrar a linha correspondente à vaga e atualizar as colunas Placa e Modelo
        for item_id in self.tabela.get_children():
            if int(self.tabela.item(item_id, 'values')[0]) == vaga:
                self.tabela.item(item_id, values=(vaga, placa, modelo, '', '', ''))

if __name__ == "__main__":
    root = tk.Tk()
    app = EstacionamentoApp(root)
    root.mainloop()
