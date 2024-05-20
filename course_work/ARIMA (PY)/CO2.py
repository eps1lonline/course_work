import warnings
import itertools
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


# Данные CO2
data = sm.datasets.co2.load_pandas()
y = data.data
y = y['co2'].resample('MS').mean()  # 'MS' группирует месячные данные
y = y.fillna(y.bfill())             # bfill значит, что нужно использовать значение до заполнения пропущенных значений
print("\nДанные:\n", y, sep="")


# Задаю стиль графику и рисую его
# plt.style.use('fivethirtyeight')
y.plot(figsize=(15, 6))
plt.show()


# Определяю параметры p, d, q в диапазоне от [0,1]
p = d = q = range(0, 2)
print("\nЗначения (p, d, q):",
      "\np: ", p, 
      "\nd: ", d, 
      "\nq: ", q)


# Генерируем различные комбинации p, q и q
pdq = list(itertools.product(p, d, q))
print("\nВсе возможные комбинации (p, d, q):",
      "\n(p, d, q):", pdq, "\n")


# Сгенерируйте комбинации сезонных параметров p, q и q
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))] 
print("Примеры комбинаций параметров для сезонного ARIMA:\n",
      "SARIMAX: {} x {}".format(pdq[1], seasonal_pdq[1]), "\n",
      "SARIMAX: {} x {}".format(pdq[1], seasonal_pdq[2]), "\n",
      "SARIMAX: {} x {}".format(pdq[2], seasonal_pdq[3]), "\n",
      "SARIMAX: {} x {}".format(pdq[2], seasonal_pdq[4]), "\n", sep = "")


# Вычисление минимального (оптимального) AIC для ARIMA
print("Вычисление минимального (оптимального) AIC для ARIMA:")
warnings.filterwarnings("ignore")  # Отключает предупреждения
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


# Вывод таблицы и описание её значений
print("\n", results.summary().tables[1])
print("\nar.L1             Коэффицент авторегрессии (AR)\n",
      "ma.L1             Коэффицент скользящего среднего (MA)\n",
      "ar.S.L12          Коэффицент сезонной авторегрессии (SAR)\n",
      "ma.S.L12          Коэффицент сезонного скользящего среднего (SMA)\n",
      "sigma2            Оценка дисперсии ошибок модели\n\n",
      "coef              Важность каждого параметра и его влияние на временной ряд\n",
      "str err           Оценка стандартного отклонения коэффициента\n",
      "z                 Мера статистической значимости коэффициента модели\n",
      "P>|z|             Вероятность получения такого же или более экстремального значения коэффициента\n",
      "[0.025...0.975]   Промежуток доверительного интервала\n", sep="")


# Рисую 4 графика, которые показывают свойства временного ряда и его прогноза
results.plot_diagnostics(figsize=(15, 12))
plt.show()


# Прогнозирование временных рядов
pred_dynamic = results.get_prediction(start=pd.to_datetime('1998-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()


# Рисую график прогноза и действительного значения
ax = y['1990':].plot(label='Known values', figsize=(20, 15))
pred_dynamic.predicted_mean.plot(label='Forecast', ax=ax)
ax.fill_between(pred_dynamic_ci.index, pred_dynamic_ci.iloc[:, 0], pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)
ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('1998-01-01'), y.index[-1],
alpha=.1, zorder=-1)
ax.set_xlabel('Date')
ax.set_ylabel('CO2 rate') # BTC rate
plt.legend()
plt.show()


# Извлечь прогнозируемые и истинные значения временного ряда
y_forecasted = pred_dynamic.predicted_mean
y_truth = y['1998-01-01':]              # Вычислить среднеквадратичную ошибку
mse = ((y_forecasted - y_truth) ** 2).mean()
print('Среднеквадратическая ошибка прогнозов равна: {}'.format(round(mse, 2)))


# Создание и визуализация прогноза. Получить прогноз на 15 шагов вперёд
pred_uc = results.get_forecast(steps=15)


# Получить интервал прогноза
pred_ci = pred_uc.conf_int()


# Рисую график прогноза
ax = y.plot(label='Known values', figsize=(20, 15))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('CO2 rate') # BTC rate
plt.legend()
plt.show()
