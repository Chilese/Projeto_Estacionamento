import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import pagamento_encerramento  # Importar o novo módulo

class RegistroVeiculoApp:
    def __init__(self, root, estacionamento_app):
        self.root = root
        self.estacionamento_app = estacionamento_app
        self.root.title("Registro de Veículo")

        # Variável para armazenar o número da vaga selecionada
        self.numero_vaga_var = tk.StringVar()

        # Frame principal
        self.frame_principal = ttk.Frame(root, padding=(10, 10))
        self.frame_principal.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Campos
        ttk.Label(self.frame_principal, text="Vaga:").grid(row=0, column=0, sticky="w", pady=(10, 0))
        self.combo_vaga = ttk.Combobox(self.frame_principal, state="readonly", textvariable=self.numero_vaga_var)
        self.combo_vaga.grid(row=0, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Placa:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.entry_placa = ttk.Entry(self.frame_principal)
        self.entry_placa.grid(row=1, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Modelo:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.entry_modelo = ttk.Entry(self.frame_principal)
        self.entry_modelo.grid(row=2, column=1, padx=10, pady=(10, 0))

        # Botão Registrar
        self.btn_registrar = ttk.Button(self.frame_principal, text="Registrar", command=self.registrar_veiculo)
        self.btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)

        # Carregar as opções do campo "Vaga"
        self.carregar_opcoes_vaga()

    def carregar_opcoes_vaga(self):
        try:
            # Obter o número de vagas do banco de dados
            with sqlite3.connect('banco_dados.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Numero_Vagas FROM Configuracoes_Estabelecimento LIMIT 1")
                resultado = cursor.fetchone()

            if resultado:
                numero_vagas = resultado[0]
                opcoes_vaga = [str(vaga) for vaga in range(1, numero_vagas + 1)]

                # Configurar as opções do combobox
                self.combo_vaga["values"] = opcoes_vaga
                # Definir a primeira opção como selecionada por padrão
                self.combo_vaga.current(0)

                # Conectar a variável à combobox
                self.combo_vaga.bind("<<ComboboxSelected>>", self.atualizar_numero_vaga)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar opções de vagas: {e}")

    def atualizar_numero_vaga(self, event):
        # Atualizar a variável com o número da vaga selecionada
        self.numero_vaga_var.set(self.combo_vaga.get())

    def registrar_veiculo(self):
        # Obter dados dos campos
        vaga = self.combo_vaga.get()
        placa = self.entry_placa.get().strip().upper()
        modelo = self.entry_modelo.get().strip()

        conn = sqlite3.connect('banco_dados.db')
        cursor = conn.cursor()

        try:
            # Verificar se a placa já existe no banco
            id_veiculo = self.obter_id_veiculo(placa)

            if id_veiculo:
                # Veículo já existe, obter o ID_veiculo
                print(f"Veículo já registrado. ID_veiculo: {id_veiculo}")
            else:
                # Veículo não existe, inserir na tabela Veiculos
                id_veiculo = self.inserir_veiculo(cursor, placa, modelo)

                print(f"Veículo registrado na tabela Veiculos com ID_veiculo: {id_veiculo}")

            # Atualizar a tabela Registros_Uso_Vagas com o ID_veiculo e o número da vaga
            self.atualizar_registros_uso_vagas(cursor, id_veiculo, vaga)

            conn.commit()

            # Atualizar a interface principal
            self.estacionamento_app.atualizar_interface_veiculo(vaga)

            messagebox.showinfo("Sucesso", "Veículo registrado com sucesso!")

            # Fechar a janela de registro após o registro
            self.root.destroy()

        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro SQLite: {e}")

        finally:
            conn.close()

    def obter_id_veiculo(self, placa):
        # Obter o ID_veiculo se a placa já existe no banco
        conn = sqlite3.connect('banco_dados.db')
        cursor = conn.cursor()

        cursor.execute("SELECT ID_veiculo FROM Veiculos WHERE Placa_veiculo = ?", (placa,))
        resultado = cursor.fetchone()

        conn.close()

        return resultado[0] if resultado else None

    def inserir_veiculo(self, cursor, placa, modelo):
        # Obter o próximo ID disponível para Veiculos
        cursor.execute("SELECT MAX(ID_veiculo) FROM Veiculos")
        proximo_id_veiculo = cursor.fetchone()[0]
        if proximo_id_veiculo is None:
            proximo_id_veiculo = 1
        else:
            proximo_id_veiculo += 1

        # Inserir o novo veículo na tabela Veiculos
        cursor.execute("INSERT INTO Veiculos (ID_veiculo, Placa_veiculo, Modelo_veiculo) VALUES (?, ?, ?)",
                       (proximo_id_veiculo, placa, modelo))

        return proximo_id_veiculo

    def atualizar_registros_uso_vagas(self, cursor, id_veiculo, numero_vaga):
        # Adicionar o registro de uso de vaga na tabela Registros_Uso_Vagas
        data_hora_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Não fornecemos um valor para ID_registro, pois é autoincrementável
        cursor.execute(
            "INSERT INTO Registros_Uso_Vagas (ID_veiculo, Numero_Vaga, Data_Hora_Entrada) VALUES (?, ?, ?)",
            (id_veiculo, numero_vaga, data_hora_entrada)
        )

        print(f"Registro de uso de vaga adicionado na tabela Registros_Uso_Vagas")

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

        # Certifique-se de que a coluna "Permanência" está corretamente configurada na tabela
        self.tabela.heading("#5", text="Permanência")
        self.tabela.column("#5", width=100)

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

        self.atualizar_permanencia()

        self.tabela.bind("<Double-1>", self.abrir_pagamento_encerramento)  # Adicionar evento de clique duplo

    def carregar_dados(self):
        try:
            print("Carregando dados do banco de dados...")
            # Obter o número de vagas do banco de dados
            self.cursor.execute("SELECT Numero_Vagas FROM Configuracoes_Estabelecimento LIMIT 1")
            resultado = self.cursor.fetchone()
            print(f"Resultado da consulta de número de vagas: {resultado}")

            if resultado:
                numero_vagas = resultado[0]

                for vaga in range(1, numero_vagas + 1):
                    # Verificar se há registros de uso de vaga para a vaga atual
                    self.cursor.execute(
                        "SELECT r.ID_veiculo, v.Placa_veiculo, v.Modelo_veiculo, r.Data_Hora_Entrada "
                        "FROM Registros_Uso_Vagas r "
                        "JOIN Veiculos v ON r.ID_veiculo = v.ID_veiculo "
                        "WHERE r.Numero_Vaga = ? "
                        "ORDER BY r.Data_Hora_Entrada DESC "
                        "LIMIT 1",
                        (vaga,)
                    )
                    registro = self.cursor.fetchone()
                    print(f"Resultado da consulta para vaga {vaga}: {registro}")

                    if registro:
                        # Se houver registro, preencher as colunas Placa, Modelo e Entrada
                        self.tabela.insert('', 'end', values=(vaga, registro[1], registro[2], registro[3], '', ''))
                    else:
                        # Se não houver registro, preencher apenas a coluna Vagas
                        self.tabela.insert('', 'end', values=(vaga, '', '', '', '', ''))
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")

    def abrir_registro(self):
        # Chamar o script de registro_de_veiculos.py
        app_registro = RegistroVeiculoApp(tk.Toplevel(self.root), self)
        app_registro.root.mainloop()

    def atualizar_interface_veiculo(self, vaga):
        try:
            print(f"Atualizando interface para a vaga {vaga}...")
            # Atualizar a tabela com as informações do veículo registrado
            for item_id in self.tabela.get_children():
                if int(self.tabela.item(item_id, 'values')[0]) == int(vaga):
                    # Obter a hora atual para a coluna "Entrada"
                    hora_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Obter as informações do veículo registrado
                    self.cursor.execute(
                        "SELECT v.Placa_veiculo, v.Modelo_veiculo "
                        "FROM Registros_Uso_Vagas r "
                        "JOIN Veiculos v ON r.ID_veiculo = v.ID_veiculo "
                        "WHERE r.Numero_Vaga = ? "
                        "ORDER BY r.Data_Hora_Entrada DESC "
                        "LIMIT 1",
                        (vaga,)
                    )
                    registro = self.cursor.fetchone()
                    print(f"Resultado da consulta para atualização de interface: {registro}")

                    if registro:
                        placa, modelo = registro
                        # Atualizar as colunas Placa, Modelo e Entrada
                        self.tabela.item(item_id, values=(vaga, placa, modelo, hora_entrada, "0:00:00", ''))
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar interface: {e}")

    def atualizar_permanencia(self):
        for item_id in self.tabela.get_children():
            entrada_str = self.tabela.item(item_id, 'values')[3]
            if entrada_str:  # Verificar se entrada_str não está vazio
                try:
                    hora_entrada = datetime.strptime(entrada_str, "%Y-%m-%d %H:%M:%S")
                    permanencia = datetime.now() - hora_entrada
                    total_segundos = int(permanencia.total_seconds())
                    dias, resto = divmod(total_segundos, 86400)
                    horas, resto = divmod(resto, 3600)
                    minutos, segundos = divmod(resto, 60)
                    
                    if dias > 0:
                        permanencia_str = f"{dias}d {horas:02}:{minutos:02}:{segundos:02}"
                    else:
                        permanencia_str = f"{horas:02}:{minutos:02}:{segundos:02}"
                    
                    self.tabela.set(item_id, column="Permanência", value=permanencia_str)
                except Exception as e:
                    print(f"Erro ao atualizar permanência para item_id {item_id}: {e}")

        # Chamar este método novamente após 1 segundo (1000 milissegundos)
        self.root.after(1000, self.atualizar_permanencia)

    def abrir_pagamento_encerramento(self, event):
        item_id = self.tabela.identify_row(event.y)  # Identificar a linha clicada
        if item_id:
            vaga = self.tabela.item(item_id, 'values')[0]
            if self.tabela.item(item_id, 'values')[1]:  # Verificar se a vaga está ocupada
                nova_janela = tk.Toplevel(self.root)
                pagamento_encerramento.PagamentoEncerramentoApp(nova_janela, vaga)
            else:
                messagebox.showinfo("Informação", "Esta vaga está vazia.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EstacionamentoApp(root)
    root.mainloop()
