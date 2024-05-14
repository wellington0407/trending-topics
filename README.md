# Visualização de Tendências do Google com FastAPI e Plotly

Este projeto consiste em uma aplicação web que utiliza o FastAPI para criar uma API em Python que fornece visualizações interativas das tendências de pesquisa do Google. A biblioteca Plotly é usada para gerar os gráficos.

## Funcionalidades

- **Obtenção de Dados**: Conecta-se ao Google Trends para obter os dados de tendências de pesquisa.
- **Processamento de Dados**: Organiza os dados obtidos em um formato adequado para visualização.
- **Visualização de Dados**: Cria gráficos interativos das tendências de pesquisa usando o Plotly.
- **Apresentação na Web**: Disponibiliza a visualização das tendências de pesquisa através de uma API web.

Link de demostração: https://app-brjilebi.b4a.run/trending-topics/

## Como Executar

Para executar este projeto, siga as etapas abaixo:

1. **Instale o Docker**: Se você ainda não tiver o Docker instalado, siga as instruções de instalação para o seu sistema operacional no [site oficial do Docker](https://www.docker.com/get-started).

2. **Clone o Repositório**: Clone este repositório para o seu ambiente de desenvolvimento:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
Substitua seu-usuario pelo seu nome de usuário no GitHub e seu-repositorio pelo nome do seu repositório.

3.Navegue até o Diretório do Projeto: Use o terminal ou prompt de comando para navegar até o diretório do projeto:

```bash
cd seu-repositorio
```

Substitua seu-repositorio pelo nome do diretório onde você clonou o repositório.

4. **Construa a Imagem Docker**: Use o seguinte comando para construir a imagem Docker:

```bash
docker build -t nome_da_imagem .
```

Substitua nome_da_imagem pelo nome que você deseja dar à sua imagem Docker.

5. **CExecute o Contêiner Docker**:: Use o seguinte comando para executar o contêiner Docker:

```bash
docker run -p 8000:8000 nome_da_imagem
```
Isso iniciará sua aplicação dentro do contêiner e mapeará a porta 8000 do contêiner para a porta 8000 do seu sistema local.

6. **Acesse a API**: Após iniciar o contêiner, acesse a API em http://localhost:8000/trending-topics/ para visualizar as tendências de pesquisa.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para relatar problemas ou sugerir melhorias.

## Licença
Este projeto é licenciado sob a MIT License.