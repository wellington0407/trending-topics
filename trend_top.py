import json
import time
import asyncio
import random
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
            return extract_trend_data(keyword, interest_over_time_df)
        except Exception as e:
            print(f"Erro ao consultar Google Trends: {e}")
            await asyncio.sleep(10)  

async def get_top_trending_topic(geo='BR'):
    trending_topics = pytrends.trending_searches(pn='brazil')
    return random.choice(trending_topics[0])

def extract_trend_data(keyword, trends_data):
    if trends_data is not None and not trends_data.empty:
        daily_counts = trends_data[keyword].resample('D').sum()
        dates = [str(date) for date in daily_counts.index]
        counts = daily_counts.values.tolist()
        return {'dates': dates, 'counts': counts}
    else:
        print(f"Nenhum dado de tendência disponível para a palavra-chave: {keyword}")
        return {}

def plot_trend_data(trend_data):
    dates = trend_data['dates']
    counts = trend_data['counts']
    data = [go.Scatter(x=dates, y=counts, mode='lines+markers', name='Tendência', line=dict(width=2), marker=dict(size=8))]
    layout = go.Layout(title='Google Trends', xaxis=dict(title='Data', tickfont=dict(size=14)), yaxis=dict(title='Contagem', tickfont=dict(size=14)), titlefont=dict(size=16))
    fig = go.Figure(data=data, layout=layout)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

@app.get("/trending-topic/", response_class=HTMLResponse)
async def read_trending_topic():
    geo = 'BR'
    keyword = await get_top_trending_topic(geo=geo)
    trend_data_json = await get_google_trends(keyword, geo=geo)
    
    with open("style/styles.css", "r") as css_file:
        css_content = css_file.read()
    
    keyword_html = f"""
    <head>
        <title>Trending Topic</title>
        <style>{css_content}</style>
    </head>
    <h2>Trending Topic:</h2>
    <p class="keyword">{keyword}</p>
    """
    
    plot_html = plot_trend_data(trend_data_json)
    
    final_html = f"{keyword_html}<br>{plot_html}"
    
    return final_html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
