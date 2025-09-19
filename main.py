import json
import time
import os
import matplotlib.pyplot as plt

# =============================
# Métodos de Ordenação
# =============================

def bubble_sort(arr):
    n = len(arr)
    while True:
        swapped = False
        for i in range(1, n):
            if arr[i - 1] > arr[i]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True
        n -= 1
        if not swapped:
            break

def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort(left)
        merge_sort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

def quick_sort(arr):
    def _quick_sort(lst, low, high):
        if low < high:
            pi = partition(lst, low, high)
            _quick_sort(lst, low, pi - 1)
            _quick_sort(lst, pi + 1, high)
    def partition(lst, low, high):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if lst[j] <= pivot:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        return i + 1
    _quick_sort(arr, 0, len(arr) - 1)

# =============================
# Funções Auxiliares
# =============================

def carregar_dados(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["dados"]

def medir_tempo(funcao, arr):
    copia = arr.copy()
    inicio = time.time()
    funcao(copia)
    fim = time.time()
    duracao = fim - inicio
    if duracao >= 1:
        return {"valor": duracao, "unidade": "s"}
    else:
        return {"valor": duracao * 1000, "unidade": "ms"}

# =============================
# Execução Principal + Relatório
# =============================

def main():
    
    # 10, 100, 1000, 5000, 10000, 50000, 100000
    arquivos = [f"jsons/entrada_{n}.json" for n in [10, 100, 1000, 5000, 10000, 50000, 100000]]
    algoritmos = [
        ("Bubble Sort", bubble_sort, {"melhor":"O(n)","medio":"O(n^2)","pior":"O(n^2)"}),
        ("Selection Sort", selection_sort, {"melhor":"O(n^2)","medio":"O(n^2)","pior":"O(n^2)"}),
        ("Insertion Sort", insertion_sort, {"melhor":"O(n)","medio":"O(n^2)","pior":"O(n^2)"}),
        ("Merge Sort", merge_sort, {"melhor":"O(n log n)","medio":"O(n log n)","pior":"O(n log n)"}),
        ("Quick Sort", quick_sort, {"melhor":"O(n log n)","medio":"O(n log n)","pior":"O(n^2)"}),
    ]

    resultados = {alg[0]: [] for alg in algoritmos}
    tamanhos = []

    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            print(f"⚠ Arquivo {arquivo} não encontrado!")
            continue

        dados = carregar_dados(arquivo)
        tamanhos.append(len(dados))
        for nome, funcao, _ in algoritmos:
            tempo_info = medir_tempo(funcao, dados)
            resultados[nome].append(tempo_info)

    if not os.path.exists("grafico_resultados"):
        os.makedirs("grafico_resultados")

    # Criar gráfico comparativo usando apenas valores numéricos em ms
    for nome, tempos_info in resultados.items():
        valores_ms = [t["valor"] * (1000 if t["unidade"] == "s" else 1) for t in tempos_info]
        plt.figure()
        plt.plot(tamanhos, valores_ms, marker='o')
        plt.xlabel("Tamanho da Entrada")
        plt.ylabel("Tempo (ms)")
        plt.title(f"{nome} - Tempo x Tamanho")
        plt.grid()
        plt.savefig(f"grafico_resultados/grafico_{nome.replace(' ', '_')}.png")
        plt.close()

    plt.figure()
    for nome, tempos_info in resultados.items():
        valores_ms = [t["valor"] * (1000 if t["unidade"] == "s" else 1) for t in tempos_info]
        plt.plot(tamanhos, valores_ms, marker='o', label=nome)
    plt.xlabel("Tamanho da Entrada")
    plt.ylabel("Tempo (ms)")
    plt.title("Comparativo de Algoritmos de Ordenação")
    plt.legend()
    plt.grid()
    plt.savefig("grafico_resultados/grafico_comparativo.png")
    plt.close()

    relatorio = {
        "maquina": {
            "processador": "AMD Ryzen™ 5 3500U",
            "memoria_gb": "12,0 GB",
            "sistema_operacional": "Ubuntu 24.04.3 LTS"
        },
        "resultados": resultados,
        "complexidades": {nome: comp for nome, _, comp in algoritmos},
        "graficos": {
            "individuais": [f"grafico_resultados/grafico_{nome.replace(' ', '_')}.png" for nome in resultados.keys()],
            "comparativo": "grafico_resultados/grafico_comparativo.png"
        },
        "referencias": ["Aula 06 - Algoritmos de Ordenação - Prof. André Chaves Lima"]
    }

    with open("relatorio_resultados.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print("Relatório gerado: relatorio_resultados.json")

if __name__ == "__main__":
    main()
