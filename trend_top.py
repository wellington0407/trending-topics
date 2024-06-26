import random
from fastapi import FastAPI, HTTPException
from pytrends.request import TrendReq
import plotly.graph_objs as go
from fastapi.responses import HTMLResponse

app = FastAPI()
pytrends = TrendReq(hl='BR', tz=120)

async def get_top_trending_topics(geo='BR'):
    trending_topics = pytrends.trending_searches(pn='brazil')
    return trending_topics

async def get_google_trends(keyword, timeframe='today 5-y', geo='BR', max_retries=3):
    for _ in range(max_retries):
        try:
            pytrends.build_payload(kw_list=[keyword], timeframe=timeframe, geo=geo)
            interest_over_time_df = pytrends.interest_over_time()
            trend_data = extract_trend_data(keyword, interest_over_time_df)
            if trend_data:
                return trend_data
        except Exception as e:
            print(f"Erro ao consultar Google Trends: {e}")
    return None

def extract_trend_data(keyword, trends_data):
    if trends_data is not None and not trends_data.empty:
        daily_counts = trends_data[keyword].resample('D').sum()
        dates = [str(date) for date in daily_counts.index]
        counts = daily_counts.values.tolist()
        return {'dates': dates, 'counts': counts}
    return {}

def plot_trend_data(trend_data):
    plots_html = []
    for keyword, data_info in trend_data.items():
        dates = data_info['dates']
        counts = data_info['counts']
        data = [go.Scatter(x=dates, y=counts, mode='lines+markers', name=keyword, line=dict(width=2), marker=dict(size=8))]
        layout = go.Layout(title=f'Google Trends: {keyword}', xaxis=dict(title='Data', tickfont=dict(size=14)), yaxis=dict(title='Quantidade', tickfont=dict(size=14)), titlefont=dict(size=16))
        fig = go.Figure(data=data, layout=layout)
        plots_html.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    return ''.join(plots_html)

@app.get("/trending-topics/", response_class=HTMLResponse)
async def read_trending_topics():
    geo = 'BR'
    top_trends = await get_top_trending_topics()
    keywords = [i[0] for i in top_trends.values.tolist()]
    random_keyword = random.choice(keywords)
    trend_data = await get_google_trends(random_keyword, geo=geo)

    with open("style/styles.css", "r") as css_file:
        css_content = css_file.read()

    keywords_html = f"""
    <head>
        <title>Trending Topics</title>
        <style>{css_content}</style>
    </head>
    <h2>Trending Topics:</h2>
    <ul class="keyword-list">
    """

    for keyword in keywords:
        keywords_html += f'<li class="keyword-list-item">{keyword}</li>'

    keywords_html += "</ul>"
    
    if trend_data:
        plot_html = plot_trend_data({random_keyword: trend_data})
        final_html = f"{keywords_html}<br>{plot_html}"
    else:
        final_html = keywords_html

    return final_html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
