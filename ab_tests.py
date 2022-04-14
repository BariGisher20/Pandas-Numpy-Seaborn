import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)


historical_data = pd.read_csv('historical_data.csv',
                              parse_dates=[1, 2],
                              index_col=0)

perc_85 = round(np.percentile(historical_data['time_to_order'], 85),  1)  # на уровне значимости 85% проверяем возможное окно конверсии при потере 15% достоверности

plt.figure(figsize=(16, 9))
sns.displot(historical_data['time_to_order'])
plt.vlines(perc_85, ymin=0, ymax=0.7,
           linestyles='dashed',
           label=f'85-ый перцентиль - {perc_85} дней')

plt.title('Распределение времени между первым заходом на сайт и покупкой')
plt.xlabel('Кол-во дней')
plt.ylabel('Кол-во пользователей')
plt.legend()
# plt.show()

data = pd.read_csv('ab_data.csv', index_col=0)
metrics = data.groupby('test_group', as_index=False).agg({
    'user_id': 'count',
    'created_order_in_3_days': 'sum'
})
metrics['conversion'] = round(metrics['created_order_in_3_days']/metrics['user_id']*100, 2)


def plot_segment_distribution(df, segment_columns, test_factor):
    for segment in segment_columns:
        aggregated_data = df.groupby(by=[test_factor, segment]).user_id.count().reset_index()
        sns.catplot(x=segment, y='user_id', hue=test_factor, data=aggregated_data, kind='bar', height=4, aspect=1.5)


plot_segment_distribution(data, ['geo_group', 'marketing_group'], 'test_group')
metrics = data.groupby('marketing_group', as_index=False).agg({
    'user_id': 'count',
    'created_order_in_3_days': 'sum'
})
metrics['conversion'] = round(metrics['created_order_in_3_days']/metrics['user_id']*100, 2)
print(metrics)
plt.show()


