# Visualização de Tendências do Google com FastAPI e Plotly

Este projeto consiste em uma aplicação web que utiliza o FastAPI para criar uma API em Python que fornece visualizações interativas das tendências de pesquisa do Google. A biblioteca Plotly é usada para gerar os gráficos.

## Funcionalidades

- **Obtenção de Dados**: Conecta-se ao Google Trends para obter os dados de tendências de pesquisa.
- **Processamento de Dados**: Organiza os dados obtidos em um formato adequado para visualização.
- **Visualização de Dados**: Cria gráficos interativos das tendências de pesquisa usando o Plotly.
- **Apresentação na Web**: Disponibiliza a visualização das tendências de pesquisa através de uma API web.

## Como Executar

1. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```
2.Inicie o servidor FastAPI:

```bash
uvicorn main:app --reload
```

3.Acesse a API em http://localhost:8000/trending-topics/ para visualizar as tendências de pesquisa.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para relatar problemas ou sugerir melhorias.

## Licença
Este projeto é licenciado sob a MIT License.
