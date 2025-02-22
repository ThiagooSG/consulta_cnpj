import requests
import pandas as pd
import time
import certifi
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def consulta_cnpj(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    response = requests.get(url, verify=False)  # Desativar verificação SSL

    if response.status_code == 200:
        data = response.json()
        situacao = data.get("situacao")
        simples = data.get("simples", {})
        simei = data.get("simei", {})
        email = data.get("email", "Não informado")

        simples_info = ""
        simei_info = ""

        if simples.get("optante"):
            ultima_atualizacao_simples = datetime.strptime(simples.get('ultima_atualizacao'), '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')
            simples_info = f"Simples: Optante\nDesde {simples.get('data_opcao')}\nÚltima Atualização: {ultima_atualizacao_simples}"
            simei_info = "MEI: Não se enquadra"
        elif simei.get("optante"):
            ultima_atualizacao_simei = datetime.strptime(simei.get('ultima_atualizacao'), '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')
            simei_info = f"Simei: Optante\nDesde {simei.get('data_opcao')}\nÚltima Atualização: {ultima_atualizacao_simei}"
            simples_info = "Simples: Não se enquadra"
        else:
            simples_info = "Simples: Não se enquadra"
            simei_info = "MEI: Não se enquadra"

        return {
            "situacao": situacao,
            "simples": simples_info,
            "simei": simei_info,
            "email": email
        }
    else:
        return None

def processar_cnpjs(cnpj_file, output_file):
    try:
        df = pd.read_excel(cnpj_file, engine='openpyxl', dtype={'CNPJ': str})
        print("Arquivo Excel lido com sucesso.")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {cnpj_file}")
        return
    except PermissionError:
        print(f"Permissão negada ao tentar acessar o arquivo: {cnpj_file}. Verifique se o arquivo está aberto em outro programa ou se você tem as permissões necessárias.")
        return
    except ValueError as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return

    if 'CNPJ' not in df.columns:
        print("Coluna 'CNPJ' não encontrada no arquivo.")
        return

    resultados = []
    total_cnpjs = len(df)
    contador = 0

    for i, row in df.iterrows():
        if i > 0 and i % 3 == 0:  # A cada 3 consultas, esperar 60 segundos
            for remaining in range(60, 0, -1):
                timer_label.config(text=f"Esperando {remaining} segundos para a próxima rodada de consultas...")
                root.update()
                time.sleep(1)

        cnpj = row['CNPJ'].replace('.', '').replace('/', '').replace('-', '').strip().zfill(14)  # Remover máscara, espaços e adicionar zeros à esquerda se necessário
        print(f"Consultando CNPJ: {cnpj}")
        resultado = consulta_cnpj(cnpj)
        if resultado:
            print(f"Resultado: {resultado}")
            resultados.append((cnpj, resultado['situacao'], resultado['simples'], resultado['simei'], resultado['email']))
        else:
            print(f"Erro na consulta ao CNPJ: {cnpj}")
            resultados.append((cnpj, "Erro na consulta", "Simples: Não se enquadra", "MEI: Não se enquadra", "Não informado"))

        contador += 1
        contador_label.config(text=f"CNPJs consultados: {contador}/{total_cnpjs}")
        root.update()

    # Criar DataFrame com os resultados
    resultados_df = pd.DataFrame(resultados, columns=['CNPJ', 'Situação', 'Simples', 'Simei', 'Email'])

    # Salvar resultados em um novo arquivo Excel
    try:
        resultados_df.to_excel(output_file, index=False)
        print(f"Resultados salvos em: {output_file}")
        messagebox.showinfo("Sucesso", f"Resultados salvos em: {output_file}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel: {e}")
        messagebox.showerror("Erro", f"Erro ao salvar o arquivo Excel: {e}")


def consultar_unico_cnpj():
    cnpj = cnpj_entry.get().replace('.', '').replace('/', '').replace('-', '').strip().zfill(14)
    resultado = consulta_cnpj(cnpj)
    if resultado:
        resultado_text = f"CNPJ: {cnpj}\nSituação: {resultado['situacao']}\n{resultado['simples']}\n{resultado['simei']}\nEmail: {resultado['email']}"
    else:
        resultado_text = "Erro na consulta ao CNPJ."
    resultado_label.config(text=resultado_text)

def selecionar_arquivo():
    cnpj_file = filedialog.askopenfilename(title="Selecione a planilha de CNPJs", filetypes=[("Arquivos Excel", "*.xlsx")])
    if cnpj_file:
        output_file = filedialog.asksaveasfilename(title="Salvar resultados como", defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
        if output_file:
            processar_cnpjs(cnpj_file, output_file)

# Configurar a interface gráfica
root = tk.Tk()
root.title("Consulta de CNPJs")
root.geometry("400x400")

label = tk.Label(root, text="Selecione a planilha de CNPJs e o local para salvar os resultados", wraplength=300)
label.pack(pady=10)

botao_selecionar = tk.Button(root, text="Selecionar Planilha", command=selecionar_arquivo)
botao_selecionar.pack(pady=10)

contador_label = tk.Label(root, text="CNPJs consultados: 0/0")
contador_label.pack(pady=10)

timer_label = tk.Label(root, text="")
timer_label.pack(pady=10)

# Campo para consultar um único CNPJ
cnpj_entry = tk.Entry(root)
cnpj_entry.pack(pady=10)

botao_consultar = tk.Button(root, text="Consultar CNPJ", command=consultar_unico_cnpj)
botao_consultar.pack(pady=10)

resultado_label = tk.Label(root, text="", wraplength=300)
resultado_label.pack(pady=10)

root.mainloop()