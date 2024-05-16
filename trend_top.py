import random
from fastapi import FastAPI, HTTPException, Query
from pytrends.request import TrendReq
import plotly.graph_objs as go
from fastapi.responses import HTMLResponse
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = FastAPI()
pytrends = TrendReq(hl='BR', tz=120)

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')

sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('portuguese'))

async def get_top_trending_topics(geo='BR'):
    try:
        trending_topics = pytrends.trending_searches(pn='brazil')
        return trending_topics
    except Exception as e:
        print(f"Erro ao obter tópicos em alta: {e}")
        return None

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

def analyze_trend(keyword):
    try:
        news_articles = pytrends.related_queries(kw_list=[keyword])['top']
        analysis = ""
        for i in range(5):
            sentence = news_articles.iloc[i]['value']
            words = word_tokenize(sentence)
            filtered_words = [w for w in words if w not in stop_words]
            analysis += ' '.join(filtered_words)
            sentiment = sia.polarity_scores(sentence)
            analysis += f" - Sentiment: {sentiment['compound']}"
        return analysis
    except Exception as e:
        return f"Análise de tendência falhou: {e}"

@app.get("/trending-topics/", response_class=HTMLResponse)
async def read_trending_topics(keyword: str = Query(None)):
    geo = 'BR'
    top_trends = await get_top_trending_topics()
    
    with open("style/styles.css", "r") as css_file:
        css_content = css_file.read()

    keywords_html = f"""
    <head>
        <title>Trending Topics</title>
        <style>{css_content}</style>
    </head>
    """

    if not top_trends.empty:
        keywords = [i[0] for i in top_trends.values.tolist()]
        keywords_html += f"<h2>Trending Topics:</h2><ul class='keyword-list'>"
        for keyword in keywords:
            keywords_html += f'<li class="keyword-list-item">{keyword}</li>'
        keywords_html += "</ul>"
    else:
        keywords_html += "<h2>Trending Topics:</h2><p>Não foi possível obter tópicos em alta.</p>"

    if keyword is None:
        if not top_trends.empty:
            random_keyword = random.choice(keywords)
            trend_data = await get_google_trends(random_keyword, geo=geo)
        else:
            trend_data = None
    else:
        trend_data = await get_google_trends(keyword, geo=geo)

    if trend_data:
        plot_html = plot_trend_data({keyword: trend_data})
        analysis = analyze_trend(keyword)
        final_html = f"{keywords_html}<br>{plot_html}<br><br><b>Análise:</b><br>{analysis}"
    else:
        analysis = analyze_trend(keyword)
        final_html = f"{keywords_html}<br><br><b>Análise:</b><br>{analysis}"

    return final_html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)