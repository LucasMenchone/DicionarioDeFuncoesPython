import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class DicionarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dicionário App")

        # Componentes da interface
        self.label_chave = tk.Label(root, text="Nome Função/Atributo:", font=("Arial", 12))
        self.label_valor = tk.Label(root, text="Descrição:", font=("Arial", 12))
        self.entry_chave = tk.Entry(root, font=("Arial", 12))
        self.entry_valor = tk.Entry(root, font=("Arial", 12))
        self.button_adicionar = tk.Button(root, text="Adicionar", command=self.adicionar_palavra, font=("Arial", 12))

        self.label_busca = tk.Label(root, text="Buscar:", font=("Arial", 12))
        self.entry_busca = tk.Entry(root, font=("Arial", 12))
        self.button_buscar = tk.Button(root, text="Buscar", command=self.buscar_palavra, font=("Arial", 12))

        self.resultado_busca = tk.Label(root, text="Resultado:", font=("Arial", 12))
        self.lista_resultados = tk.Listbox(root, selectmode=tk.SINGLE, font=("Arial", 12))
        self.scrollbar_resultados_y = tk.Scrollbar(root, command=self.lista_resultados.yview)
        self.scrollbar_resultados_x = tk.Scrollbar(root, command=self.lista_resultados.xview, orient=tk.HORIZONTAL)
        self.lista_resultados.config(yscrollcommand=self.scrollbar_resultados_y.set, xscrollcommand=self.scrollbar_resultados_x.set)

        self.button_editar = tk.Button(root, text="Editar", command=self.editar_palavra, font=("Arial", 12))
        self.button_excluir = tk.Button(root, text="Excluir", command=self.excluir_palavra, font=("Arial", 12))
        self.button_limpar = tk.Button(root, text="Limpar", command=self.limpar_resultados, font=("Arial", 12))

        # Configuração do grid para tornar a interface responsiva
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(3, weight=1)
        root.grid_rowconfigure(4, weight=1)
        root.grid_rowconfigure(5, weight=1)
        root.grid_rowconfigure(6, weight=1)
        root.grid_rowconfigure(7, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Atributo dicionario
        self.dicionario = {}
        self.arquivo_dados = "dados_dicionario.json"
        self.carregar_dados()

        # Layout
        self.label_chave.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_chave.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        self.label_valor.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_valor.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
        self.button_adicionar.grid(row=2, column=0, columnspan=2, pady=10)

        self.label_busca.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_busca.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)
        self.button_buscar.grid(row=4, column=0, columnspan=2, pady=10)

        self.resultado_busca.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.lista_resultados.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)
        self.scrollbar_resultados_y.grid(row=6, column=2, sticky=tk.NS, pady=5)
        self.scrollbar_resultados_x.grid(row=7, column=0, columnspan=2, sticky=tk.EW, pady=5)

        self.button_editar.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.button_excluir.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        self.button_limpar.grid(row=8, column=2, padx=5, pady=5, sticky=tk.E)

        # Adiciona evento para redimensionar dinamicamente os elementos
        root.bind("<Configure>", self.redimensionar)

    def adicionar_palavra(self):
        chave = self.entry_chave.get()
        valor = self.entry_valor.get()

        if chave and valor:
            self.dicionario[chave] = valor
            messagebox.showinfo("Sucesso", "Palavra adicionada ao dicionário!")
            self.entry_chave.delete(0, tk.END)
            self.entry_valor.delete(0, tk.END)
            self.salvar_dados()
        else:
            messagebox.showerror("Erro", "Por favor, preencha tanto a chave quanto o valor.")

    def buscar_palavra(self):
        termo_busca = self.entry_busca.get().lower()

        self.lista_resultados.delete(0, tk.END)  # Limpa a lista de resultados

        resultados = [f"{chave}: {valor}" for chave, valor in self.dicionario.items() if termo_busca in chave.lower() or termo_busca in valor.lower()]

        for resultado in resultados:
            self.lista_resultados.insert(tk.END, resultado)

    def editar_palavra(self):
        selecionado = self.lista_resultados.curselection()

        if selecionado:
            selecionado = selecionado[0]
            chave_valor = self.lista_resultados.get(selecionado).split(':')
            chave = chave_valor[0].strip()
            valor = chave_valor[1].strip()

            novo_valor = simpledialog.askstring("Editar Valor", f"Editar valor para a chave '{chave}':", initialvalue=valor)

            if novo_valor:
                self.dicionario[chave] = novo_valor
                messagebox.showinfo("Sucesso", "Valor editado com sucesso!")
                self.buscar_palavra()  # Atualiza a lista de resultados após a edição
                self.salvar_dados()
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma entrada para editar.")

    def excluir_palavra(self):
        selecionado = self.lista_resultados.curselection()

        if selecionado:
            selecionado = selecionado[0]
            chave_valor = self.lista_resultados.get(selecionado).split(':')
            chave = chave_valor[0].strip()

            resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a chave '{chave}'?")

            if resposta:
                del self.dicionario[chave]
                messagebox.showinfo("Sucesso", "Palavra excluída com sucesso!")
                self.buscar_palavra()  # Atualiza a lista de resultados após a exclusão
                self.salvar_dados()
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma entrada para excluir.")

    def limpar_resultados(self):
        self.lista_resultados.delete(0, tk.END)  # Limpa a lista de resultados

    def salvar_dados(self):
        with open(self.arquivo_dados, 'w') as file:
            json.dump(self.dicionario, file)

    def carregar_dados(self):
        try:
            with open(self.arquivo_dados, 'r') as file:
                self.dicionario = json.load(file)
        except FileNotFoundError:
            self.dicionario = {}

    def redimensionar(self, event):
        # Atualiza o tamanho da caixa de texto de resultados conforme a janela é redimensionada
        self.lista_resultados.config(width=event.width // 12)

if __name__ == "__main__":
    root = tk.Tk()
    app = DicionarioApp(root)
    root.mainloop()
