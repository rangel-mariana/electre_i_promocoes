# Aplicação do Método ELECTRE I na Seleção de Categorias para Promoções em Comerciais de Televisão no Setor Supermercadista

Repositório desenvolvido para o artigo científico submetido ao XXVIII ENMC – Encontro Nacional de Modelagem Computacional e XVI ECTM – Encontro de Ciência e Tecnologia de Materiais (2025).

Foram considerados cinco critérios de decisão:
- Nível de estoque  
- Sazonalidade  
- Competitividade  
- Preferência de compras  
- Desvio em relação à meta de margem  

Os experimentos foram realizados com **dados reais de uma unidade varejista**, avaliando diferentes cenários a partir da variação dos parâmetros de corte de concordância e discordância.

---

## 📂 Estrutura do Repositório
- **data/** → `BASE.xlsx` (arquivo com a base de dados)  
- **electre_i.py** → script principal para execução dos experimentos  
- **results/** → arquivos gerados:
  - `df_normalizado.xlsx`  
  - `Matriz_Concordancia.xlsx`  
  - `Matriz_Discordancia.xlsx`  
  - `resultado_kernels.xlsx`  

---

## ⚙️ Metodologia
1. **Pré-processamento dos dados**  
   - Renomear as colunas e criação de identificadores automáticos.
   - Normalização min–max (benefício)- Nível de estoque, Sazonalidade, Competitividade ePreferência de compras.
   - Tratamento especial para o desvio de margem, atribuindo pontuação apenas a valores positivos.  

2. **Aplicação do ELECTRE I**  
   - Cálculo das matrizes de concordância e discordância.  
   - Construção da relação de sobreclassificação.  
   - Remoção de ciclos 2-a-2 por desempate de concordância/discordância.  
   - Identificação do **kernel** e das alternativas dominadas.  

---

## ⚖️ Pesos dos Critérios
- Nível de estoque → **0.20**  
- Sazonalidade → **0.15**  
- Competitividade → **0.20**  
- Preferência de compras → **0.20**  
- Desvio em relação à meta de margem → **0.25**  

---

## 🧪 Experimentos
Foram realizados três experimentos com diferentes valores de corte (`c_hat` e `d_hat`):

- **Experimento 1:** `c_hat = 0.6`, `d_hat = 0.3`  
- **Experimento 2:** `c_hat = 0.7`, `d_hat = 0.3`  
- **Experimento 3:** `c_hat = 0.8`, `d_hat = 0.2`  

Cada execução gera o conjunto de categorias pertencentes ao **kernel**, bem como as matrizes de concordância e discordância utilizadas para a análise.

---
## 📚 Bibliotecas Utilizadas
- **os** → manipulação de caminhos de arquivos  
- **numpy** → operações numéricas e vetoriais  
- **pandas** → leitura, tratamento e exportação de dados  
- **pyDecision** → implementação do método ELECTRE I  

---
### 🔧 Instalação
```bash
pip install numpy pandas pyDecision# electrei-promocoes
