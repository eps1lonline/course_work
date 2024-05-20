import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

sr=pd.Series(np.random.randn(1000))
print(sr)

data = pd.read_csv('C:/Users/danik/Desktop/course_work/Датасеты/BTC_Corrected_Month.txt', delimiter='\s+', header=None, names=['Date', 'Value'], converters={'Value': lambda x: float(x.replace(',', '.'))})
sr = pd.Series(data['Value'].values, index=pd.to_datetime(data['Date']))
print("\nДанные:\n", sr, sep="")

n=5
############################################
rolling_mean = sr.rolling(window=n).mean()  
plt.plot(sr[n:], label="Actual values",color='blue') 
plt.plot(rolling_mean, color="red", lw=3, label="Rolling mean trend")
plt.legend(loc="upper left") 
plt.show() 