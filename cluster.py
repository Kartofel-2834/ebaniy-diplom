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
import copy

def print_line_model_equatation(model):
    coefficients = list(map(str, filter(lambda v: v != 0, model.coef_[0])));
    coefficients = map(lambda v, i: f'({v} * x^{str(i)})', coefficients, range(1, len(coefficients) + 1))
    
    right_size = ' + '.join([str(model.intercept_[0])] + list(coefficients))

    print(f'y = {right_size}')

def print_forecast(result_data):
    years = set();
    rows_A = [];
    rows_B = [];

    for cluster in result_data:
        row_A = ['Выбросы' if cluster['id'] == -1 else f'Кластер {cluster['id'] + 1}'];
        row_B = ['Выбросы' if cluster['id'] == -1 else f'Кластер {cluster['id'] + 1}'];

        for point in cluster['forecast']['A']:
            years.add(str(point[0]))
            row_A.append(str(point[1]))

        for point in cluster['forecast']['B']:
            row_B.append(str(point[1]))

        rows_A.append(row_A)
        rows_B.append(row_B)
    
    print('\n\nПрогнозная таблица для характеристики А')
    print(';'.join(['Кластеры'] + sorted(years))) 
    print('\n'.join(map(lambda row: ';'.join(row), rows_A))) 

    print('\n\nПрогнозная таблица для характеристики B')
    print(';'.join(['Кластеры'] + sorted(years))) 
    print('\n'.join(map(lambda row: ';'.join(row), rows_B))) 

def print_regions(result_data):
    for cluster in result_data:
        cluster_name = 'Выбросы' if cluster['id'] == -1 else f'Кластер {cluster["id"] + 1}'
        print(f'\n\nРегионы - {cluster_name}')

        regions = cluster['data'][0]['regions'].keys();

        print(', '.join(sorted(regions)))


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
    learning_data = {};

    # Обучение модели DBSCAN на данных всех лет
    for year in same_years:
        learning_year_data = {};
        year_data = {};

        for region in same_regions:
            A_clean = a_data.loc[a_data['REGION'] == region, year].values[0]
            B_clean = b_data.loc[b_data['REGION'] == region, year].values[0]
            
            A = first_formatter(a_data.loc[a_data['REGION'] == region, year].values[0])
            B = second_formatter(b_data.loc[b_data['REGION'] == region, year].values[0])

            year_data[region] = [A_clean, B_clean]
            learning_year_data[region] = [A, B]

        data[year] = year_data
        learning_data[year] = learning_year_data
        dbscan.fit(list(learning_year_data.values()))

    return dbscan, data, learning_data    

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

def get_forecast(data, degree=3, include_bias=True):
    poly_features = PolynomialFeatures(degree=degree, include_bias=include_bias)
    result = {}

    years = sorted(list(data.keys()));
    regions = list(data[years[0]].keys());

    model_A = LinearRegression();
    model_B = LinearRegression();

    for region in regions:
        X = poly_features.fit_transform(list(map(lambda v: [v], years)));
        y_A = list(map(lambda v: data[v][region][0], years));
        y_B = list(map(lambda v: data[v][region][1], years));
    
        model_A.fit(X, y_A)
        model_B.fit(X, y_B)

    years_predict = years + list(range(years[-1] + 1, 2027)) 
    years_predict = list(map(lambda v: [v], years_predict))
   
    X_predict = poly_features.fit_transform(years_predict)
    y_A_predict = model_A.predict(X_predict)
    y_B_predict = model_B.predict(X_predict)

    result['A'] = list(map(lambda year, v: [int(year[0]), int(v)], years_predict, y_A_predict))
    result['B'] = list(map(lambda year, v: [int(year[0]), int(v)], years_predict, y_B_predict))

    return result

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

        forecast = get_forecast(current_cluster, degree=degree)

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

        print(f'\nУравнение регрессии A от Б для кластера {cluster_id}')
        print_line_model_equatation(model)

        result.append({
            "id": int(cluster_id),
            "data": data,
            "regression": regression,
            "forecast": forecast,
        })
    
    return result


def save_to_json(some_dict, file_path):
    # Сохраняем в файл
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(some_dict, f, ensure_ascii=False, indent=4)

#----------------------------------------------------------------------------------------------

## ВРП от Инвестиций
# regression_range = range(0, 100000, 10000)
# dbscan, data, learning_data = get_educated_dbscan(
#     'data/Инвестиции в основной капитал.xlsx',
#     'data/ВРП.xlsx',
#     eps=100000,
#     min_samples=5,
#     first_formatter=lambda v: v,
#     second_formatter=lambda v: v / 10
# )

# # ВРП от Среднегодовой численности занятых
# regression_range = range(0, 3000, 300)
# dbscan, data, learning_data = get_educated_dbscan(
#     'data/Среднегодовая численность занятых.xlsx',
#     'data/ВРП.xlsx',
#     eps=100000,
#     min_samples=5,
#     first_formatter=lambda v: v * 2000,
#     second_formatter=lambda v: v / 2.5
# )

# # ВРП от Стоимости основных фондов
regression_range = range(0, 1000000, 100000)
dbscan, data, learning_data = get_educated_dbscan(
    'data/Стоимость основных фондов.xlsx',
    'data/ВРП.xlsx',
    eps=360000,
    min_samples=4,
    first_formatter=lambda v: v / 1.7,
    second_formatter=lambda v: v / 1.75
)


newest_year = max(data.keys())
newest_data = list(data[newest_year].values())
newest_learning_data = list(learning_data[newest_year].values())

clusters = dbscan.fit_predict(newest_learning_data)
clusters_data = separate_data_by_clusters(data, clusters)

for cluster_id in clusters_data.keys():
    print('cluster_id', cluster_id)

result = get_result(clusters_data, regression_range)
save_to_json(result, 'output/invest__vrp.json')

print_forecast(result)
print_regions(result)
#----------------------------------------------------------------------------------------------

# selected_cluster = clusters_data[0]

# years = list(selected_cluster.keys());

# X = [[2020], [2021], [2022], [2023], [2024], [2025], [2026]]

# model, poly_features = get_educated_regression(selected_cluster, degree=3)

# X = list(map(lambda v: [v], range(0, 100000, 10000)))  

# X_poly = poly_features.fit_transform(X)
# y_pred = model.predict(X_poly)

# # Вывод линии
# plt.scatter(X, y_pred)
# plt.scatter(X[:3], y)
# plt.plot(X, y_pred, color='darkorange', label='Polynomial Regression', marker='o')
# plt.xlabel('Количество безработных')
# plt.ylabel('Заработная плата')
# plt.legend()
# plt.show()

# # Вывод кластеров
plt.scatter(
    list(map(lambda v: v[0], newest_learning_data)), # x 
    list(map(lambda v: v[1], newest_learning_data)), # y
    c=clusters,
    cmap='rainbow'
)
plt.title('Кластеры DBSCAN')
plt.xlabel('Первая характеристика')
plt.ylabel('Вторая характеристика')
plt.show()

# Сохраняем результат в файл
# save_to_json(selected_cluster, 'output/bezrab__zp.json')