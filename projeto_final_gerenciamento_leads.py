# Sistema de Gerenciamento de Leads para uma Agência de Marketing Digital
# Desenvolvido com Tkinter (interface gráfica) e SQLite (banco de dados leve)

import tkinter as tk
from tkinter import messagebox
import sqlite3

# =========================== PARTE 1: BANCO DE DADOS ===========================

# Função que cria o banco de dados e a tabela caso ainda não existam
def create_db():
    conn = sqlite3.connect('leads.db')  # Cria ou conecta ao arquivo leads.db
    cursor = conn.cursor()
    # Criação da tabela com os campos necessários para lead
    cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefone TEXT NOT NULL,
                        interesse TEXT NOT NULL,
                        status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# =========================== PARTE 2: FUNÇÕES DE AÇÃO ===========================

# Função para validar se os campos foram preenchidos corretamente
def validar_campos():
    if not entry_nome.get() or not entry_email.get() or not entry_telefone.get() or not entry_interesse.get() or not entry_status.get():
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return False
    return True

# Função para adicionar um novo lead
def adicionar():
    if validar_campos():
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        interesse = entry_interesse.get()
        status = entry_status.get()

        conn = sqlite3.connect('leads.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leads (nome, email, telefone, interesse, status) VALUES (?, ?, ?, ?, ?)",
                       (nome, email, telefone, interesse, status))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Lead cadastrado com sucesso!")
        limpar_campos()
        listar()

# Função para listar todos os leads na listbox
def listar():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads")
    registros = cursor.fetchall()
    conn.close()

    listbox.delete(0, tk.END)  # Limpa a lista antes de listar novamente
    for registro in registros:
        listbox.insert(tk.END, f"ID: {registro[0]} | Nome: {registro[1]} | Status: {registro[5]}")

# Função para buscar um lead pelo ID e preencher os campos com seus dados
def buscar():
    id = entry_id.get()
    if id.isdigit():
        conn = sqlite3.connect('leads.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leads WHERE id = ?", (id,))
        lead = cursor.fetchone()
        conn.close()

        if lead:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(tk.END, lead[1])
            entry_email.delete(0, tk.END)
            entry_email.insert(tk.END, lead[2])
            entry_telefone.delete(0, tk.END)
            entry_telefone.insert(tk.END, lead[3])
            entry_interesse.delete(0, tk.END)
            entry_interesse.insert(tk.END, lead[4])
            entry_status.delete(0, tk.END)
            entry_status.insert(tk.END, lead[5])
        else:
            messagebox.showwarning("Atenção", "Lead não encontrado.")
    else:
        messagebox.showerror("Erro", "ID inválido.")

# Função para atualizar os dados de um lead existente
def atualizar():
    if entry_id.get().isdigit() and validar_campos():
        id = int(entry_id.get())
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        interesse = entry_interesse.get()
        status = entry_status.get()

        conn = sqlite3.connect('leads.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE leads SET nome = ?, email = ?, telefone = ?, interesse = ?, status = ? WHERE id = ?",
                       (nome, email, telefone, interesse, status, id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Lead atualizado com sucesso!")
        limpar_campos()
        listar()
    else:
        messagebox.showerror("Erro", "ID inválido ou campos incompletos.")

# Função para excluir um lead pelo ID
def excluir():
    id = entry_id.get()
    if id.isdigit():
        conn = sqlite3.connect('leads.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leads WHERE id = ?", (id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Lead excluído com sucesso!")
        limpar_campos()
        listar()
    else:
        messagebox.showerror("Erro", "ID inválido.")

# Função para limpar os campos de entrada
def limpar_campos():
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_interesse.delete(0, tk.END)
    entry_status.delete(0, tk.END)

# =========================== PARTE 3: INTERFACE GRÁFICA ===========================

# Criação da janela principal
root = tk.Tk()
root.title("Gerenciador de Leads - Agência Marketing Digital")

# Frame para organizar os widgets
frame = tk.Frame(root, padx=100, pady=50)
frame.pack()

# Campos do formulário (ID para busca, Nome, Email, Telefone, Interesse, Status)

tk.Label(frame, text="ID:").grid(row=0, column=0)
entry_id = tk.Entry(frame)
entry_id.grid(row=0, column=1)

tk.Label(frame, text="Nome:").grid(row=1, column=0)
entry_nome = tk.Entry(frame)
entry_nome.grid(row=1, column=1)

tk.Label(frame, text="Email:").grid(row=2, column=0)
entry_email = tk.Entry(frame)
entry_email.grid(row=2, column=1)

tk.Label(frame, text="Telefone:").grid(row=3, column=0)
entry_telefone = tk.Entry(frame)
entry_telefone.grid(row=3, column=1)

tk.Label(frame, text="Interesse:").grid(row=4, column=0)
entry_interesse = tk.Entry(frame)
entry_interesse.grid(row=4, column=1)

tk.Label(frame, text="Status:").grid(row=5, column=0)
entry_status = tk.Entry(frame)
entry_status.grid(row=5, column=1)

# Listbox para mostrar os leads cadastrados
listbox = tk.Listbox(frame, width=60, height=20)
listbox.grid(row=8, column=0, columnspan=2, pady=10)

# Botões de ação
btn_adicionar = tk.Button(frame, text="Adicionar", command=adicionar)
btn_adicionar.grid(row=6, column=0, pady=5)

btn_buscar = tk.Button(frame, text="Buscar", command=buscar)
btn_buscar.grid(row=6, column=1, pady=5)

btn_atualizar = tk.Button(frame, text="Atualizar", command=atualizar)
btn_atualizar.grid(row=7, column=0, pady=5)

btn_excluir = tk.Button(frame, text="Excluir", command=excluir)
btn_excluir.grid(row=7, column=1, pady=5)

# Inicialização do banco de dados e carregamento dos dados existentes
create_db()
listar()

# Loop principal da interface
root.mainloop()
