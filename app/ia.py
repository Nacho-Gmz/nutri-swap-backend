from sklearn.cluster import KMeans
import numpy as np


def obtener_sustitutos_ordenados(alimento_obj, lista_alimentos, n_clusters=5):
    # Paso 1: Crear matriz nutricional
    datos_nutricionales = np.array(
        [[a.energia, a.proteinas, a.lipidos, a.carbohidratos] for a in lista_alimentos]
    )

    # Paso 2: Aplicar K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(datos_nutricionales)
    labels = kmeans.labels_

    # Paso 3: Identificar índice y clúster del alimento original
    alimento_index = lista_alimentos.index(alimento_obj)
    cluster_objetivo = labels[alimento_index]
    vector_objetivo = datos_nutricionales[alimento_index]

    # Paso 4: Obtener candidatos del mismo clúster (excepto el original)
    candidatos = []
    for i, alimento in enumerate(lista_alimentos):
        if labels[i] == cluster_objetivo and i != alimento_index:
            distancia = np.linalg.norm(vector_objetivo - datos_nutricionales[i])
            candidatos.append((alimento, distancia))

    # Paso 5: Ordenar por distancia (menor = más parecido)
    candidatos_ordenados = sorted(candidatos, key=lambda x: x[1])

    # Paso 6: Retornar solo la lista de objetos Alimento ordenados
    return [alimento for alimento, _ in candidatos_ordenados]
