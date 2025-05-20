import re
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale, PolynomialFeatures
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from functools import reduce
from sklearn.linear_model import LinearRegression
import json

def cluster_dbscan(data, distance = 0.5, min_samples = 5):
    dbscan = DBSCAN(eps=0.5, min_samples=5)

    for index in range(len(data.columns)):
        X = np.array(data.iloc[index]).reshape(-1, 1)
        kamal = dbscan.fit_predict(X)
        print('kamal', kamal)

    return

def get_data(excel_data_file_path):
    excel_data = pd.read_excel(excel_data_file_path)

    # Удаляем строки с NaN
    excel_data = excel_data.dropna()

    years = map(lambda column: re.search('^[0-9]{4}', str(column)), excel_data.columns)
    years = map(lambda match: match.group(0) if match != None else None, years)
    years = filter(lambda year: year != None, years)
    years = list(map(lambda year: int(year), years))

    regions = excel_data.loc[:, 'REGION'].values

    return excel_data, years, regions

def get_educated_dbscan(
    first_excel_data_file_path,
    second_excel_data_file_path,
    eps=100,
    min_samples=5,
    first_formatter=lambda v: v,
    second_formatter=lambda v: v,
):
    a_data, a_years, a_regions = get_data(first_excel_data_file_path)
    b_data, b_years, b_regions = get_data(second_excel_data_file_path) 

    same_years = list(set.intersection(set(a_years), set(b_years)))
    same_regions = list(set.intersection(set(a_regions), set(b_regions)))

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    data = {};

    # Обучение модели DBSCAN на данных всех лет
    for year in same_years:
        learning_a = [];
        learning_b = [];
        learning_data = {};

        for region in same_regions:
            A = a_data.loc[a_data['REGION'] == region, year].values[0]
            B = b_data.loc[b_data['REGION'] == region, year].values[0]
            
            A = first_formatter(A)
            B = second_formatter(B)

            learning_a.append(A)
            learning_b.append(B)
            learning_data[region] = [A, B]

        data[year] = learning_data
        dbscan.fit(list(learning_data.values()))

    return dbscan, data

def separate_data_by_clusters(data, clusters):
    result = {}
    
    for year in data.keys():
        regions_list = list(data[year].keys())

        for index in range(len(regions_list)):
            region = regions_list[index];
            cluster_id = clusters[index];
            values = data[year][region]

            if not result.get(cluster_id):
                result[cluster_id] = {}

            if not result[cluster_id].get(year):
                result[cluster_id][year] = {}

            result[cluster_id][year][region] = values

    return result

def get_educated_regression(data, degree=3, include_bias=True):
    poly_features = PolynomialFeatures(degree=degree, include_bias=include_bias)
 
    regions_data = map(lambda year_data: list(year_data.values()), data.values()) 
    solid_data = list(reduce(lambda a, b: a + b, regions_data))

    A = list(map(lambda v: [v[0]], solid_data));
    B = list(map(lambda v: [v[1]], solid_data)); 

    X = poly_features.fit_transform(A)
    y = B

    model = LinearRegression()
    model.fit(X, y)

    return model, poly_features

def get_result(
    clusters_data,
    some_range,
    degree=3
):
    result = [];
    X = list(map(lambda v: [v], list(some_range)));
    
    for cluster_id in sorted(clusters_data.keys()):
        current_cluster = clusters_data[cluster_id]
        years = sorted(current_cluster.keys())

        model, poly_features = get_educated_regression(current_cluster, degree=degree)
        X_poly = poly_features.fit_transform(X)
        y_pred = model.predict(X_poly)

        regression = list(map(lambda a, b: [int(a[0]), int(b[0])], X, y_pred));
        data = []

        for year in years:
            regions = {}

            for region_name in current_cluster[year].keys():
                regions[region_name] = list(map(int, current_cluster[year][region_name]))

            data.append({ "year": int(year), "regions": regions })

        

        result.append({
            "id": int(cluster_id),
            "data": data,
            "regression": regression
        })
    
    return result


def save_to_json(some_dict, file_path):
    # Сохраняем в файл
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(some_dict, f, ensure_ascii=False, indent=4)

#----------------------------------------------------------------------------------------------

dbscan, data = get_educated_dbscan(
    'data/bezrab.xlsx',
    'data/zp.xlsx',
    eps=5000,
    first_formatter=lambda v: v * 1000
)

newest_year = max(data.keys())
newest_data = list(data[newest_year].values())

clusters = dbscan.fit_predict(newest_data)
clusters_data = separate_data_by_clusters(data, clusters)

for cluster_id in clusters_data.keys():
    print('cluster_id', cluster_id)

selected_cluster = clusters_data[0]

model, poly_features = get_educated_regression(selected_cluster, degree=3)

result = get_result(clusters_data, range(0, 100000, 10000))
save_to_json(result, 'output/bezrab__zp.json')

# X = [[10000], [20000], [30000], [40000], [50000], [60000], [70000], [80000], [90000], [100000]]

# X_poly = poly_features.fit_transform(X)
# y_pred = model.predict(X_poly)

# # Вывод линии
# plt.scatter(X, y_pred)
# plt.plot(X, y_pred, color='darkorange', label='Polynomial Regression', marker='o')
# plt.xlabel('Количество безработных')
# plt.ylabel('Заработная плата')
# plt.legend()
# plt.show()

# # Вывод кластеров
# plt.scatter(
#     list(map(lambda v: v[0], newest_data)), # x 
#     list(map(lambda v: v[1], newest_data)), # y
#     c=clusters,
#     cmap='rainbow'
# )
# plt.title('Кластеры DBSCAN')
# plt.xlabel('Первая характеристика')
# plt.ylabel('Вторая характеристика')
# plt.show()

# Сохраняем результат в файл
# save_to_json(selected_cluster, 'output/bezrab__zp.json')