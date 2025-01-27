# ANALISADOR DE IPS EM LOTE
### José Eduardo de Souza Pimentel

O programa emprega o poder do Python e das LLMs, mediadas pela biblioteca `litellm`, para analisar uma coleção de inquéritos policiais em formato PDF encontrados em determinada pasta (diretório).

## Estratégias
1. Usamos o `PyPDF` para extrair textos dos PDFs. Preservamos a numeração das páginas para referenciar as respostas.
2. O texto extraído compõe um extenso prompt, com as perguntas à LLM dirigidas à analise de cada caso.
3. Importante: **a biblioteca `litellm` facilitou o desenvolvimento e abstraiu toda a complexidade das chamadas a APIs. Com ela, é muito fácil substituir um provedor de LLM por outro.** 

## Intalações necessárias
- ```pip install PyPDF2 litellm python-dotenv```

- Configure um arquivo ```.env``` com os chaves (api keys) das suas LLMs.

## Privacidade
Provedores de LLMs, como a OpenAI, afirmam que não utilizam os dados de entrada e saída de suas APIs para treinamento. Também garantem que permanecem privados. 

Avalie sempre os riscos. 

Prefira testar a ferramenta com processos não gravados de sigilo ou que serão elegíveis aos bancos públicos de sentenças.

## Alucina?
LLMs ainda alucinam bastante. 

O emprego da ferramenta no campo profissional deve ser avaliado caso a caso.

## Restrições
Observe o número máximo de tokens dos modelos selecinados. 

Faça sempre uma avaliação de custo-benefício do modelo escolhido.

## Apresentação do relatório
O relatório é formatado em `markdown`, que se integra muito bem às LLMs.

Se você vai repassar o relatório, considere acrescentar as seguintes linhas ao código:
```bash
pip install pypandoc
```

```python
import pypandoc
pypandoc.convert_file('arquivo.md', 'pdf', outputfile='arquivo.pdf')
```
Você tem que ter o executável do `pandoc` no seu sistema (adicionado à variável `PATH` do sistema).

Outra opção é usar a extensão `Markdown PDF` do VS Code e fazer a exportação manual.

## Aprendendo?
Então, use o Google Colab e faça as alterações do código pelo navegador. 

Vou deixar no meu GitHub uma versão adaptada deste programa.