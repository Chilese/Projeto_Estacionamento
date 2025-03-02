import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class PagamentoEncerramentoApp:
    def __init__(self, root, vaga):
        self.root = root
        self.vaga = vaga
        self.root.title("Pagamento e Encerramento")
        print(f"Inicializando PagamentoEncerramentoApp para a vaga {vaga}")

        # Frame principal
        self.frame_principal = ttk.Frame(root, padding=(10, 10))
        self.frame_principal.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Campos
        ttk.Label(self.frame_principal, text="Tipo de Pagamento:").grid(row=0, column=0, sticky="w", pady=(10, 0))
        self.combo_tipo_pagamento = ttk.Combobox(self.frame_principal, state="readonly", values=["Dinheiro", "Pix", "Crédito", "Débito"])
        self.combo_tipo_pagamento.grid(row=0, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Modalidade:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.combo_modalidade = ttk.Combobox(self.frame_principal, state="readonly", values=["Por Hora", "Diária", "Noturna", "Mensal"])
        self.combo_modalidade.grid(row=1, column=1, padx=10, pady=(10, 0))
        self.combo_modalidade.bind("<<ComboboxSelected>>", self.calcular_valor)

        ttk.Label(self.frame_principal, text="Valor a Pagar:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.entry_valor_pagar = ttk.Entry(self.frame_principal, state="readonly")
        self.entry_valor_pagar.grid(row=2, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Data e Hora de Entrada:").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.entry_data_hora_entrada = ttk.Entry(self.frame_principal)
        self.entry_data_hora_entrada.grid(row=3, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Data e Hora de Saída:").grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.entry_data_hora_saida = ttk.Entry(self.frame_principal)
        self.entry_data_hora_saida.grid(row=4, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Tempo de Permanência:").grid(row=5, column=0, sticky="w", pady=(10, 0))
        self.entry_tempo_permanencia = ttk.Entry(self.frame_principal)
        self.entry_tempo_permanencia.grid(row=5, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Número da Vaga:").grid(row=6, column=0, sticky="w", pady=(10, 0))
        self.entry_numero_vaga = ttk.Entry(self.frame_principal)
        self.entry_numero_vaga.grid(row=6, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Modelo do Veículo:").grid(row=7, column=0, sticky="w", pady=(10, 0))
        self.entry_modelo_veiculo = ttk.Entry(self.frame_principal)
        self.entry_modelo_veiculo.grid(row=7, column=1, padx=10, pady=(10, 0))

        ttk.Label(self.frame_principal, text="Placa do Veículo:").grid(row=8, column=0, sticky="w", pady=(10, 0))
        self.entry_placa_veiculo = ttk.Entry(self.frame_principal)
        self.entry_placa_veiculo.grid(row=8, column=1, padx=10, pady=(10, 0))

        # Botão Concluir
        self.btn_concluir = ttk.Button(self.frame_principal, text="Concluir", command=self.concluir_pagamento)
        self.btn_concluir.grid(row=9, column=0, columnspan=2, pady=10)

        # Carregar dados iniciais
        self.carregar_dados_iniciais()

    def carregar_dados_iniciais(self):
        try:
            print("Conectando ao banco de dados...")
            conn = sqlite3.connect('banco_dados.db')
            cursor = conn.cursor()
            print("Conexão estabelecida.")

            print("Executando consulta SQL...")
            cursor.execute(
                "SELECT r.Data_Hora_Entrada, v.Modelo_veiculo, v.Placa_veiculo "
                "FROM Registros_Uso_Vagas r "
                "JOIN Veiculos v ON r.ID_veiculo = v.ID_veiculo "
                "WHERE r.Numero_Vaga = ? "
                "ORDER BY r.Data_Hora_Entrada DESC "
                "LIMIT 1",
                (self.vaga,)
            )
            registro = cursor.fetchone()
            print(f"Resultado da consulta: {registro}")

            if registro:
                data_hora_entrada, modelo_veiculo, placa_veiculo = registro
                print(f"Inserindo valores nos campos: {data_hora_entrada}, {modelo_veiculo}, {placa_veiculo}, {self.vaga}")

                self.entry_data_hora_entrada.config(state="normal")
                self.entry_data_hora_entrada.insert(0, data_hora_entrada)
                self.entry_data_hora_entrada.config(state="readonly")

                self.entry_modelo_veiculo.config(state="normal")
                self.entry_modelo_veiculo.insert(0, modelo_veiculo)
                self.entry_modelo_veiculo.config(state="readonly")

                self.entry_placa_veiculo.config(state="normal")
                self.entry_placa_veiculo.insert(0, placa_veiculo)
                self.entry_placa_veiculo.config(state="readonly")

                self.entry_numero_vaga.config(state="normal")
                self.entry_numero_vaga.insert(0, self.vaga)
                self.entry_numero_vaga.config(state="readonly")

                data_hora_saida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.entry_data_hora_saida.config(state="normal")
                self.entry_data_hora_saida.insert(0, data_hora_saida)
                self.entry_data_hora_saida.config(state="readonly")

                hora_entrada = datetime.strptime(data_hora_entrada, "%Y-%m-%d %H:%M:%S")
                permanencia = datetime.now() - hora_entrada
                total_segundos = int(permanencia.total_seconds())
                dias, resto = divmod(total_segundos, 86400)
                horas, resto = divmod(resto, 3600)
                minutos, segundos = divmod(resto, 60)

                if dias > 0:
                    permanencia_str = f"{dias}d {horas:02}:{minutos:02}:{segundos:02}"
                else:
                    permanencia_str = f"{horas:02}:{minutos:02}:{segundos:02}"

                self.entry_tempo_permanencia.config(state="normal")
                self.entry_tempo_permanencia.insert(0, permanencia_str)
                self.entry_tempo_permanencia.config(state="readonly")
            else:
                messagebox.showerror("Erro", "Nenhum registro encontrado para a vaga especificada.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
        finally:
            conn.close()
            print("Conexão com o banco de dados fechada.")

    def calcular_valor(self, event):
        modalidade = self.combo_modalidade.get()
        data_hora_entrada = self.entry_data_hora_entrada.get()
        if not data_hora_entrada:
            messagebox.showerror("Erro", "Data e Hora de Entrada não pode estar vazio.")
            return

        conn = sqlite3.connect('banco_dados.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Tarifa_Por_Hora, Tarifa_Diaria, Tarifa_Noturna, Tarifa_Mensal FROM Configuracoes_Estabelecimento LIMIT 1")
        tarifas = cursor.fetchone()

        if tarifas:
            tarifa_por_hora, tarifa_diaria, tarifa_noturna, tarifa_mensal = tarifas
            hora_entrada = datetime.strptime(data_hora_entrada, "%Y-%m-%d %H:%M:%S")
            permanencia = datetime.now() - hora_entrada
            total_horas = permanencia.total_seconds() / 3600

            if modalidade == "Por Hora":
                valor = total_horas * tarifa_por_hora
            elif modalidade == "Diária":
                valor = tarifa_diaria
            elif modalidade == "Noturna":
                valor = tarifa_noturna
            elif modalidade == "Mensal":
                valor = tarifa_mensal

            self.entry_valor_pagar.config(state="normal")
            self.entry_valor_pagar.delete(0, tk.END)
            self.entry_valor_pagar.insert(0, f"{valor:.2f}")
            self.entry_valor_pagar.config(state="readonly")

        conn.close()

    def concluir_pagamento(self):
        tipo_pagamento = self.combo_tipo_pagamento.get()
        data_hora_saida = self.entry_data_hora_saida.get()
        valor_pagar = self.entry_valor_pagar.get()

        print(f"Concluindo pagamento para a vaga {self.vaga}")
        print(f"Tipo de pagamento: {tipo_pagamento}")
        print(f"Data e Hora de Saída: {data_hora_saida}")
        print(f"Valor a Pagar: {valor_pagar}")

        conn = sqlite3.connect('banco_dados.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE Registros_Uso_Vagas SET Data_Hora_Saida = ? WHERE Numero_Vaga = ? AND Data_Hora_Saida IS NULL",
                (data_hora_saida, self.vaga)
            )
            print("Atualização de Registros_Uso_Vagas concluída.")

            cursor.execute(
                "INSERT INTO Registros_Pagamentos (Data_Hora_Pagamento, Tipo_Pagamento, Valor_Pago) VALUES (?, ?, ?)",
                (data_hora_saida, tipo_pagamento, valor_pagar)
            )
            print("Inserção em Registros_Pagamentos concluída.")

            conn.commit()
            messagebox.showinfo("Sucesso", "Pagamento concluído com sucesso!")
            self.root.destroy()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Erro SQLite: {e}")
            messagebox.showerror("Erro", f"Erro SQLite: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
        finally:
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pagamento e Encerramento")
    app = PagamentoEncerramentoApp(root, 1)  # Exemplo de uso com a vaga 1
    root.mainloop()
