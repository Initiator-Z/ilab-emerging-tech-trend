import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from dateutil import parser

def bar_chart(data):
    agg_data = data.groupby('classification').size().reset_index(name='count')
    fig = px.bar(agg_data, x='classification', y='count', color='classification',
                 labels={'classification': 'Classification', 'count': 'Count of Publications'},
                 title='Count of Publication/Patent in Application Fields')
    return fig

def time_series(data):
    if not isinstance(data['publish_date'].iloc[0], pd.Timestamp):
        data['publish_date'] = data['publish_date'].apply(lambda x: parser.parse(x).strftime('%Y-%m-%d %H:%M:%S%z'))
        data['publish_date'] = pd.to_datetime(data['publish_date'], errors='coerce')

    start_date = data['publish_date'].min()
    end_date = data['publish_date'].max()
    interval_size = pd.DateOffset(months=1)
    intervals = pd.date_range(start=start_date, end=end_date, freq=interval_size)

    count_data = []
    classifications = data['classification'].unique()

    for classification in classifications:
        for interval_start, interval_end in zip(intervals, intervals[1:]):
            mask = (data['publish_date'] >= interval_start) & (data['publish_date'] < interval_end) & (data['classification'] == classification)
            count = data[mask]['classification'].count()
            count_data.append({'Interval Start': interval_start, 'Interval End': interval_end, 'Classification': classification, 'Count': count})

    count_df = pd.DataFrame(count_data)
    fig = px.line(count_df, x='Interval Start', y='Count', color='Classification',
                  labels={'Count': 'Count of Publications'},
                  title='Count of Application Fields Over Time')

    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), title_text='Publication Time'),
                      yaxis_title='Count of Publications')
    return fig

def pie_chart(data, selected_year):
    data['publish_date'] = pd.to_datetime(data['publish_date'])
    filtered_data = data[data['publish_date'].dt.year == selected_year]
    count_data = filtered_data['classification'].value_counts().reset_index()
    count_data.columns = ['Classification', 'Count']
    fig = px.pie(count_data, names='Classification', values='Count',
                 title=f'Proportion of Application Fields in {selected_year}',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    return fig
