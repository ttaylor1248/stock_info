import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

ticker = yf.Ticker("RGTI")
hist = ticker.history("1mo")
columns = ['Open', 'High', 'Low', 'Close', 'Volume']
df = hist[columns]
df = df.loc['2023-11-01':]
# print(df.head())


df = df.reset_index("Date")

df["Date2"] = df['Date'].dt.date
df['DayofWeek'] = df["Date"].dt.dayofweek
df['Week'] = df['Date'].dt.isocalendar().week.astype(int)
# df['Week'] = df['Week'].str[-2:]
df['Year'] = df['Date'].dt.isocalendar().year
# df['Yr_Wk'] = (df['Year'] + df['Week'])

df_grouped = df.groupby(['DayofWeek']).aggregate({'High': 'max', 'Low': 'max'})
print(df_grouped)

max_high = df.groupby('Week').agg({'High':'mean'})
min_low = df.groupby('Week').agg({'Low': 'mean'})
df_min_max = pd.concat([min_low, max_high], ignore_index=False, sort=False,
                       axis=1)
df_min_max['Diff'] = df_min_max['High'] - df_min_max['Low']
df_min_max['Perc_change'] = df_min_max['Diff'] / df_min_max['Low']

# print(df_min_max)
columns2 = ['Date2', 'Open', 'High', 'Low', 'Close', 'Volume', 'DayofWeek',
            'Week']
col3 = ['Date', 'Date2', 'High', 'Low', 'Close', 'Week']
df2 = df[columns2]
# df2_filtered = df2.loc(df2['Date'].dt.year == 2024)
# print(df2_filtered.head())

highs = df[['Week','High']]
lows = df2[['Week','Low']]
close = df2[['Week','Close']]
lm = df2[['Week', 'High', 'Low']]


x = df['Date2']
y1 = df['Low']
y2 = df['High']
yc = df['Close']

fig = plt.figure()
ax1 = sns.boxplot(data=highs, x='Week', y='High')
ax2 = sns.boxplot(data=lows, x='Week', y='Low')
ax3 = sns.regplot(data=lm, x='Week', y='Low', color='orange')
ax4 = sns.regplot(data=lm, x='Week', y='High', color='blue')
ax1.set(title='RGTI High - Low Stock Prices')
ax1.set(ylabel='Stock Price')
ax1.set(xlabel='Year-Week')
plt.xticks(rotation=45)
plt.grid(linestyle='--')
plt.show()


fig2, ax = plt.subplots()
ax.fill_between(x, y1, y2, alpha=.5, linewidth=0)
ax.plot(x, yc, linewidth=2, color='red')
ax.tick_params(labelrotation=45)
plt.grid(linestyle='--')

plt.show()








