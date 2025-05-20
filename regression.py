from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import json

df = pd.read_excel('data/population.xlsx')

# Подготовим данные для модели
df_clean = df.dropna(subset=["2018 г.", "2019 г.", "2020 г.", "2021 г.", "2022 г.", "2023 г."])
years = np.array([2018, 2019, 2020, 2021, 2022, 2023])
future_years = np.array([2024, 2025, 2026])

result = []

for _, row in df_clean.iterrows():
    region_name = row["все население"]
    values = row[["2018 г.", "2019 г.", "2020 г.", "2021 г.", "2022 г.", "2023 г."]].values.astype(float)

    # Подготовка полиномиальных признаков степени 2
    poly = PolynomialFeatures(degree=2)
    X = poly.fit_transform(years.reshape(-1, 1))
    print(X, values)
    # Обучение модели
    model = LinearRegression()
    model.fit(X, values)

    # Прогноз на 2024-2026
    future_X = poly.transform(future_years.reshape(-1, 1))
    predicted_values = model.predict(future_X)

    # Формирование JSON-структуры
    region_entry = {
        "name": region_name,
        "values": {
            str(year): int(round(val)) for year, val in zip(years, values)
        }
    }
    for year, val in zip(future_years, predicted_values):
        region_entry["values"][str(year)] = int(round(val))

    result.append(region_entry)

# Сохраняем в файл
with open("population_forecast.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)