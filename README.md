# ANALISADOR DE IPS EM LOTE
### José Eduardo de Souza Pimentel

O programa emprega o poder das LLMs, mediadas pelo `litellm`, para analisar uma coleção de inquéritos policiais em formato PDF.
## Estratégias
1. Usamos o `PyPDF` para extrair textos dos PDFs. Preservamos a numeração das páginas para garantir que as respostas serão referenciadas.
2. O texto extraído comporá um extenso prompt, com as perguntas à LLM que a fazem analisar cada caso.
3. A biblioteca `litellm` facilita o desenvolvimento e abstrai a complexidade das chamadas de APIs. Com ela, é fácil substituir um provedor de LLM por outro. 

## Intalações necessárias
```pip install PyPDF2 litellm python-dotenv```

Configure um arquivo ```.env``` com os chaves (api keys) das suas LLMs.

## Privacidade
Provedores de LLMs, como a OpenAI, afirmam que não utilizam os dados de entrada e saída das APIs para treinamento e que estes permanecem privados. Avalie os riscos. Prefira testar a ferramenta com processos não gravados de sigilo. Opte por usar naqueles casos que serão elegíveis aos bancos públicos de sentenças.

## Alucina?
LLMs sempre alucinam. O emprego da ferramenta no campo profissional deve ser avaliado caso a caso pelo usuário.

## Restrições
Observe o número máximo de tokens dos modelos selecinados. Faça sempre uma avaliação de custo-benefício.