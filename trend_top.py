import json
import time
import asyncio
from fastapi import FastAPI, HTTPException
from pytrends.request import TrendReq
import plotly.graph_objs as go
from fastapi.responses import HTMLResponse

app = FastAPI()
pytrends = TrendReq(hl='BR', tz=120)

async def get_google_trends(keyword, timeframe='today 5-y', geo='BR'):
    while True:
        try:
            pytrends.build_payload(kw_list=[keyword], timeframe=timeframe, geo=geo)
            interest_over_time_df = pytrends.interest_over_time()
            return interest_over_time_df
        except Exception as e:
            print(f"Erro ao consultar Google Trends para {keyword}: {e}")
            await asyncio.sleep(1)  # Esperar 3 segundos antes de tentar novamente

async def get_top_trending_topics(geo='BR'):
    trending_topics = pytrends.trending_searches(pn='brazil')
    return trending_topics

def extract_trend_data(keyword, trends_data):
    if trends_data is not None and not trends_data.empty:
        daily_counts = trends_data[keyword].resample('D').sum()
        dates = [str(date) for date in daily_counts.index]
        counts = daily_counts.values.tolist()
        return {keyword: {'dates': dates, 'counts': counts}}
    else:
        print(f"Nenhum dado de tendência disponível para a palavra-chave: {keyword}")
        return {}

def plot_trend_data(trend_data):
    plots_html = []
    for keyword, data_info in trend_data.items():
        dates = data_info['dates']
        counts = data_info['counts']
        data = [go.Scatter(x=dates, y=counts, mode='lines+markers', name=keyword, line=dict(width=2), marker=dict(size=8))]
        layout = go.Layout(title=f'Google Trends sobre: {keyword}', xaxis=dict(title='Data', tickfont=dict(size=14)), yaxis=dict(title='Contagem', tickfont=dict(size=14)), titlefont=dict(size=16))
        fig = go.Figure(data=data, layout=layout)
        plots_html.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    return ''.join(plots_html)

@app.get("/trending-topics/", response_class=HTMLResponse)
async def read_trending_topics():
    geo = 'BR'
    top_trends = await get_top_trending_topics()
    lista = top_trends.values.tolist()
    trend_data_json = {}
    tasks = [get_google_trends(i[0], geo=geo) for i in lista]
    trends_data = await asyncio.gather(*tasks)
    for i, keyword in enumerate([i[0] for i in lista]):
        trend_data_json.update(extract_trend_data(keyword, trends_data[i]))
    plot_html = plot_trend_data(trend_data_json)
    return plot_html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
