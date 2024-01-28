import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from controle_estacionamento import EstacionamentoApp

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
        # Obter o número de vagas do banco de dados
        conn = sqlite3.connect('banco_dados.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Numero_Vagas FROM Configuracoes_Estabelecimento LIMIT 1")
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            numero_vagas = resultado[0]
            opcoes_vaga = [str(vaga) for vaga in range(1, numero_vagas + 1)]

            # Configurar as opções do combobox
            self.combo_vaga["values"] = opcoes_vaga
            # Definir a primeira opção como selecionada por padrão
            self.combo_vaga.current(0)

            # Conectar a variável à combobox
            self.combo_vaga.bind("<<ComboboxSelected>>", self.atualizar_numero_vaga)

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
            self.estacionamento_app.atualizar_interface_veiculo(vaga, placa, modelo)

            messagebox.showinfo("Sucesso", "Veículo registrado com sucesso!")

            # Limpar os campos após o registro
            self.combo_vaga.set("")  # Limpar a seleção do combobox
            self.entry_placa.delete(0, tk.END)
            self.entry_modelo.delete(0, tk.END)

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

# Criar a janela principal
if __name__ == "__main__":
    root_registro = tk.Tk()
    estacionamento_app = EstacionamentoApp(tk.Tk())
    app_registro = RegistroVeiculoApp(root_registro, estacionamento_app)
    root_registro.mainloop()
