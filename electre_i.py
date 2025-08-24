import os
import numpy as np
import pandas as pd
from pyDecision.algorithm import electre_i

# ==============================
# Configurações de caminho
# ==============================
diretorio_arquivos = "/seu_diretorio/BASE"
nome_arquivo = "BASE.xlsx"
caminho_completo = os.path.join(diretorio_arquivos, nome_arquivo)

# ==============================
# Leitura e preparação dos dados
# ==============================
df = pd.read_excel(caminho_completo, engine='openpyxl')

df = df.rename(columns={
    "DDV": "k1_estoque",
    "SAZONALIDADE": "k2_sazonalidade",
    "CATEGORIA DE PRODUTOS": "Categoria",
    "COMPETITIVIDADE": "k3_competitividade",
    "CUPONS": "k4_preferencia",
    "DESVIO META": "k5_margem"
})

df['k1_estoque'] = df['k1_estoque'].astype(int)
df['k5_margem'] = df['k5_margem'].round(2)
df['Codigo'] = [f'a{i+1}' for i in range(len(df))]
df.set_index('Codigo', inplace=True)

# ==============================
# Normalização dos critérios
# ==============================
criteria_info = {
    "k1_estoque": "benefit",
    "k2_sazonalidade": "benefit",
    "k3_competitividade": "benefit",
    "k4_preferencia": "benefit",
    "k5_margem": "custom"
}

df_norm = df.copy()

for col, ctype in criteria_info.items():
    if ctype == "benefit":
        df_norm[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    elif ctype == "cost":
        df_norm[col + '_abs'] = df[col].abs()
        x_max = df_norm[col + '_abs'].max()
        x_min = df_norm[col + '_abs'].min()
        df_norm[col] = (x_max - df_norm[col + '_abs']) / (x_max - x_min)

    elif ctype == "custom":
        df_norm[col] = df[col].copy()
        df_norm.loc[df[col] < 0, col] = 0
        if df_norm[col].max() > 0:
            df_norm[col] = df_norm[col] / df_norm[col].max()

df_criterios = df_norm[list(criteria_info.keys())].to_numpy(dtype=float)

# ==============================
# Salvar dataframe normalizado
# ==============================
caminho_norm_excel = os.path.join(diretorio_arquivos, "df_normalizado.xlsx")
df_norm.reset_index().to_excel(caminho_norm_excel, index=False)
print(f"DataFrame normalizado salvo: {caminho_norm_excel}")

# ==============================
# Pesos
# ==============================
W = np.array([0.20, 0.15, 0.20, 0.20, 0.25])

# ==============================
# Experimentos
# ==============================
experimentos = [
    {"nome": "experimento_1", "c_hat": 0.6, "d_hat": 0.3},
    {"nome": "experimento_2", "c_hat": 0.7, "d_hat": 0.3},
    {"nome": "experimento_3", "c_hat": 0.8, "d_hat": 0.2},
]

# ==============================
# Resultado kernels (consolidado) + matrizes
# ==============================
df_resultados = pd.DataFrame({"Categoria": df["Categoria"].values})
concordance_matrix = None
discordance_matrix = None

for exp in experimentos:
    concordance, discordance, dominance, _, _ = electre_i(
        df_criterios,
        W=W,
        remove_cycles=False,
        c_hat=exp["c_hat"],
        d_hat=exp["d_hat"],
        graph=False
    )

    # Salva matrizes só do primeiro experimento (as matrizes base não dependem de c_hat/d_hat)
    if concordance_matrix is None:
        categorias_index = df['Categoria']
        concordance_matrix = pd.DataFrame(concordance, index=categorias_index, columns=categorias_index)
        discordance_matrix = pd.DataFrame(discordance, index=categorias_index, columns=categorias_index)

    # --- Limpeza de ciclos 2-a-2 ---
    dom = dominance.copy()
    n = dom.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if dom[i, j] == 1 and dom[j, i] == 1:
                cij, cji = concordance[i, j], concordance[j, i]
                dij, dji = discordance[i, j], discordance[j, i]
                if cij > cji:
                    dom[j, i] = 0
                elif cji > cij:
                    dom[i, j] = 0
                else:
                    if dij <= dji:
                        dom[j, i] = 0
                    else:
                        dom[i, j] = 0

    # --- Kernel (indegree zero) ---
    indeg = dom.sum(axis=0)
    kernel_idx = np.where(indeg == 0)[0]
    kernel_cats = df.iloc[kernel_idx]["Categoria"].tolist()

    # Marca 1/0 por experimento
    df_resultados[exp["nome"]] = df_resultados["Categoria"].isin(kernel_cats).astype(int)

# ==============================
# Salvar 4 arquivos separados
# ==============================
# 1) Kernels consolidados
caminho_kernels = os.path.join(diretorio_arquivos, "resultado_kernels.xlsx")
df_resultados.to_excel(caminho_kernels, index=False)

# 2) Matriz de Concordância
caminho_conc = os.path.join(diretorio_arquivos, "Matriz_Concordancia.xlsx")
concordance_matrix.to_excel(caminho_conc)

# 3) Matriz de Discordância
caminho_disc = os.path.join(diretorio_arquivos, "Matriz_Discordancia.xlsx")
discordance_matrix.to_excel(caminho_disc)

# 4) DataFrame normalizado (já existente na memória)
caminho_norm = os.path.join(diretorio_arquivos, "df_normalizado.xlsx")
df_norm.reset_index().to_excel(caminho_norm, index=False)

print("Arquivos gerados:")
print(caminho_kernels)
print(caminho_conc)
print(caminho_disc)
print(caminho_norm)

