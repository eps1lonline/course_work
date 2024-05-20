import warnings
import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

data = sm.datasets.co2.load_pandas()
y = data.data

print("Данные:")
print(y)

# 'MS' группирует месячные данные
y = y['co2'].resample('MS').mean()

print("Данные:")
print(y)

# bfill значит, что нужно использовать значение до заполнения пропущенных значений
y = y.fillna(y.bfill())
print("Данные:")
print(y)

y.plot(figsize=(15, 6))
plt.show()

# Определяю p, d и q в диапазоне 0-2
p = d = q = range(0, 2)
print("\nЗначения p, d, q:\np: ", p, "\nd: ", d, "\nq: ", q)

# Генерируем различные комбинации p, q и q
pdq = list(itertools.product(p, d, q))
print("\nВсе возможные комбинации p, d, q:\n(p, d, q):", pdq, "\n")

# Сгенерируйте комбинации сезонных параметров p, q и q
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))] 

print("Примеры комбинаций параметров для сезонного ARIMA:\n",
        "SARIMAX: {} x {}".format(pdq[1], seasonal_pdq[1]), "\n",
        "SARIMAX: {} x {}".format(pdq[1], seasonal_pdq[2]), "\n",
        "SARIMAX: {} x {}".format(pdq[2], seasonal_pdq[3]), "\n",
        "SARIMAX: {} x {}".format(pdq[2], seasonal_pdq[4]), "\n")

print("Вычисление минимального (оптимального) AIC для ARIMA:")
warnings.filterwarnings("ignore")  # отключает предупреждения
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y, order=param, seasonal_order=param_seasonal, enforce_stationarity=False, enforce_invertibility=False)
            results = mod.fit(disp=False)

            # log_likelihood = results.llf
            # k = len(results.params)
            # print('k = ' , k)
            # print('aic = ', 2 * k - 2 * log_likelihood)

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))

        except:
            continue


# Определение модели временных рядов ARIMA
mod = sm.tsa.statespace.SARIMAX(y,
order=(1, 1, 1),
seasonal_order=(1, 1, 1, 12), enforce_stationarity=False, enforce_invertibility=False)
results = mod.fit(disp=False)

print(results.summary().tables[1])

print("ar.L1              Коэффицент авторегрессии (AR)\n",
        "ma.L1             Коэффицент скользящего среднего (MA)\n",
        "ar.S.L12          Коэффицент сезонной авторегрессии (SAR)\n",
        "ma.S.L12          Коэффицент сезонного скользящего среднего (SMA)\n",
        "sigma2            Оценка дисперсии ошибок модели\n\n",
        "coef              Важность каждого параметра и его влияние на временной ряд\n",
        "str err           Оценка стандартного отклонения коэффициента\n",
        "z                 Мера статистической значимости коэффициента модели\n",
        "P>|z|             Вероятность получения такого же или более экстремального значения коэффициента\n",
        "[0.025...0.975]   Промежуток доверительного интервала\n")

results.plot_diagnostics(figsize=(15, 12))
plt.show()

# Прогнозирование временных рядов
pred_dynamic = results.get_prediction(start=pd.to_datetime('1998-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()

ax = y['1990':].plot(label='Прогноз', figsize=(20, 15))
pred_dynamic.predicted_mean.plot(label='Динамический прогноз', ax=ax)
ax.fill_between(pred_dynamic_ci.index, pred_dynamic_ci.iloc[:, 0], pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)
ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('1998-01-01'), y.index[-1],
alpha=.1, zorder=-1)
ax.set_xlabel('Дата')
ax.set_ylabel('CO2 Уровень')
plt.legend()
plt.show()

# Извлечь прогнозируемые и истинные значения временного ряда
y_forecasted = pred_dynamic.predicted_mean
y_truth = y['1998-01-01':] # Вычислить среднеквадратичную ошибку
mse = ((y_forecasted - y_truth) ** 2).mean()
print()
print('Средняя квадратическая ошибка прогнозов равна: {}'.format(round(mse, 2)))

# Создание и визуализация прогноза
# Получить прогноз на 500 шагов вперёд
pred_uc = results.get_forecast(steps=500)

# Получить интервал прогноза
pred_ci = pred_uc.conf_int()

ax = y.plot(label='Известные значения', figsize=(20, 15))
pred_uc.predicted_mean.plot(ax=ax, label='Прогноз')
ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Дата')
ax.set_ylabel('CO2 Уровень')
plt.legend()
plt.show()
