import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score

excel_data = pd.read_excel('data/population.xlsx')

# Удаляем строки с NaN
excel_data = excel_data.dropna()

for column in excel_data.columns:
    if (not re.search('^[0-9]{4}', column)):
        del excel_data[column]

years = map(lambda column: re.search('^[0-9]{4}', column), excel_data.columns)
years = map(lambda match: match.group(0) if match != None else None, years)
years = filter(lambda year: year != None, years)
years = list(map(lambda year: int(year), years))

# Подготовка данных
X = np.array(years).reshape(-1, 1)  # Признак: года
y = np.array(excel_data.iloc[0]).reshape(-1, 1)  # Целевая переменная: значения первого года (2018)

poly_features = PolynomialFeatures(degree=3, include_bias=True)
X_poly = poly_features.fit_transform(X)
print(X, y)
y_train, y_test = train_test_split(y, random_state=0)
X_poly_train, X_poly_test = train_test_split(X_poly, random_state=0)

X_pred = np.array(years + [years[-1] + index for index in range(1, 5)]).reshape(-1, 1)
X_poly_pred = poly_features.fit_transform(X_pred)

# Обучение модели
model = LinearRegression()
model.fit(X_poly_train, y_train)

for index in range(1, excel_data.shape[0]):
    kamal = np.array(excel_data.iloc[index]).reshape(-1, 1)  # Целевая переменная: значения первого года (2018)
    kamal_train, kamal_test = train_test_split(y, random_state=0)
    model.fit(X_poly_train, kamal_train)

# Предсказание
y_pred = model.predict(X_poly_pred)
# y_pred = model.predict(X_poly)
print(y_pred)
plt.scatter(X, y)
plt.plot(X_pred, y_pred, color='darkorange', label='Polynomial Regression', marker='o')
plt.title('Polynomial regression')
plt.xlabel('Год')
plt.ylabel('Прирост')
plt.legend()
plt.show()

# for column in excel_data.columns:
#     if (not re.search('^[0-9]{4}', column)):
#         del excel_data[column]


# years = map(lambda column: re.search('^[0-9]{4}', column), excel_data.columns)
# years = map(lambda match: match.group(0) if match != None else None, years)
# years = filter(lambda year: year != None, years)
# years = list(map(lambda year: int(year), years))

# for index in range(len(excel_data.index)): 
#     plt.plot(years, excel_data.iloc[index], marker='o') 

# plt.title('Прирост населения в регионах РФ')
# plt.xlabel('Год')
# plt.ylabel('Прирост')
# plt.grid()
# plt.show()

# print(excel_data)