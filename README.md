# Newsletter

Este repositório contém um script para coletar diariamente notícias do setor de Alimentos e Bebidas utilizando o [NewsAPI](https://newsapi.org/).

## Uso
1. Crie uma conta no NewsAPI e obtenha uma chave de API.
2. Defina a variável de ambiente `NEWS_API_KEY` com a chave obtida.
3. Execute o script manualmente:
   ```bash
   python3 daily_news.py
   ```
4. Para executar diariamente de forma automática, agende o script com o `cron` do sistema. Exemplo de entrada no crontab para executar às 8h:
   ```
   0 8 * * * /usr/bin/python3 /caminho/para/daily_news.py >> /caminho/para/news.log 2>&1
   ```

Os artigos coletados são salvos em arquivos JSON nomeados com a data da coleta.
