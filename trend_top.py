import json
import time
import asyncio
from fastapi import FastAPI, HTTPException
from pytrends.request import TrendReq
import plotly.graph_objs as go
from fastapi.responses import HTMLResponse

app = FastAPI()
pytrends = TrendReq(hl='BR', tz=120)

async def get_google_trends(keywords, timeframe='today 5-y', geo='BR'):
    while True:
        try:
            trends_data = {}
            for keyword in keywords[:5]:  # Limitando a 5 primeiras palavras-chave
                pytrends.build_payload(kw_list=[keyword], timeframe=timeframe, geo=geo)
                interest_over_time_df = pytrends.interest_over_time()
                trends_data.update(extract_trend_data(keyword, interest_over_time_df))
            return trends_data
        except Exception as e:
            print(f"Erro ao consultar Google Trends: {e}")
            await asyncio.sleep(10)  # Esperar 10 segundos antes de tentar novamente

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
    keywords = [i[0] for i in top_trends.values.tolist()]
    trend_data_json = await get_google_trends(keywords, geo=geo)
    
    keywords_html = """
    <style>
        .keyword-list {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        .keyword-list-item {
            margin-bottom: 8px;
            padding: 6px 10px;
            background-color: #f2f2f2;
            border-radius: 5px;
            display: inline-block;
            font-size: 14px;
            color: #333;
        }
    </style>
    <h2>Trending Topics:</h2>
    <ul class="keyword-list">
    """
    for keyword in keywords:
        keywords_html += f'<li class="keyword-list-item">{keyword}</li>'
    keywords_html += "</ul>"
    
    # Plotar o gráfico
    plot_html = plot_trend_data({keyword: trend_data_json[keyword] for keyword in keywords[:5]})
    
    # Combinar a lista de palavras-chave e o gráfico no HTML final
    final_html = f"{keywords_html}<br>{plot_html}"
    
    return final_html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)