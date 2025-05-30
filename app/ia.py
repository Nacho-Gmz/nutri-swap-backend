from sklearn.cluster import KMeans
import numpy as np

def obtener_sustitutos_kmeans(alimento_obj, lista_alimentos, n_clusters=5):
    # Extraer las características nutricionales
    datos_nutricionales = np.array([
        [a.energia, a.proteinas, a.lipidos, a.carbohidratos]
        for a in lista_alimentos
    ])

    # Aplicar K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(datos_nutricionales)
    labels = kmeans.labels_

    # Ubicar índice del alimento original
    alimento_index = lista_alimentos.index(alimento_obj)
    cluster_alimento = labels[alimento_index]

    # Filtrar alimentos del mismo clúster excepto el original
    sustitutos = [
        a for i, a in enumerate(lista_alimentos)
        if labels[i] == cluster_alimento and a != alimento_obj
    ]
    print("aqui¨*¨*********************************")
    for alimento in sustitutos:
        print (alimento.alimento)
    return sustitutos