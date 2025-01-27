import os
import re
import PyPDF2
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def listar_pdfs(diretorio):
    pdfs = []
    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(".pdf"):
            pdfs.append(os.path.join(diretorio, arquivo))
    return pdfs

def ler_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ''
        for pagina_num, pagina in enumerate(leitor.pages, start=1):
            texto += f"--- Página {pagina_num} ---\n"
            texto += pagina.extract_text() + "\n\n"
    return texto

def limpar_texto(texto):
  # Remover a assinatura
  padrao_assinatura = r"Este documento .*?fls\. \d+"
  texto = re.sub(padrao_assinatura, "", texto, flags=re.DOTALL)
  # Remover sequências de números e barras
  padrao_sequencias = r"\/[j\d]+ (?:\/[j\d]+)+"
  texto_limpo = re.sub(padrao_sequencias, "", texto)
  return texto_limpo

def analisar_conteudo (texto, prompt, modelo, api_key):
  try:
    resultado = completion(
    model=modelo,
    messages=[{"role": "system", "content": "Você é um promotor de justiça especializado em analisar inquéritos policiais."},
                {"role": "system", "content": "Trabalhe somente com texto fornecido com o prompt. Não alucine."},
                {"role": "user", "content": f"**Texto do PDF:**\n\n{texto}"},
                {"role": "user", "content": f"**Instruções:**\n {prompt}"}],
                api_key=api_key
    )
    return resultado.get('choices', [{}])[0].get('message', {}).get('content', 'Sem resposta.')
  except Exception as e:
    print(f"Erro: {e}")
    return None

def gerar_markdown(texto, nome_arquivo="analises.md"):
  modo = 'a' if os.path.exists(nome_arquivo) else 'w'
  try:
    with open(nome_arquivo, modo, encoding='utf-8') as arquivo:
      if modo == 'w':
        arquivo.write("# PROMOTORIA DE JUSTIÇA DE PIRACICABA\n")
        arquivo.write("**Análise automatizada de inquéritos policiais**\n\n")
      arquivo.write(texto)
  except Exception as e:
    print(f"Erro ao salvar o arquivo: {e}")

prompt = f"""
    Extraia as seguintes informações do texto fornecido. Inclua os números de páginas de onde foram extraídas. Despreze as páginas sem informação compreensível.

    **Informações gerais:**
    * Número do procedimento no padrão CNJ
    * Data, hora e local da ocorrência
    * Crime que está sendo apurado e dispositivo legal correspondente
    * Indiciado(s) e sua(s) conduta(s)
    * Vítima(s) e testemunha(s) com seus respectivos relatos

    **Laudo:**
    * Resumo dos dados relevantes do laudo
    * Tipos e quantidades de drogas apreendidas (se aplicável)

    **Avaliação da prova:**
    * Classifique a prova como "boa" ou "fraca"
    * Justifique essa classificação

    **Dúvidas e verificação:**
    * Liste as dúvidas que você teve ao gerar o resumo
    * Verifique se todos os dados fornecidos estão no PDF e evite alucinações

    **Resumo do caso**
    * Forneça um resumo, em 2 ou 3 parágrafos. Indique data, hora, local, indiciado, conduta e toda informação juridicamente relevante.
    """

if __name__ == "__main__":
    diretorio_pdfs = "pdfs"
    
    modelo = "gpt-4o-mini"
    api_key = os.getenv('API_OPENAI')
    
    #modelo = 'deepseek/deepseek-chat'
    #api_key = os.getenv('API_DEEPSEEK')

    pdfs = listar_pdfs(diretorio_pdfs)
    conteudo = ""
    for pdf in pdfs:
        texto = ler_pdf(pdf)
        texto_limpo = limpar_texto(texto)
        resultado = analisar_conteudo(texto_limpo, prompt, modelo, api_key)
        if resultado:
            conteudo += f"\n**Arquivo:** {pdf}\n\n"
            conteudo += resultado.get('choices', [{}])[0].get('message', {}).get('content', 'Sem resposta.')
            conteudo += "\n___________________________________\n" 
            print(conteudo)
            gerar_markdown(conteudo)
        else:
            print(f"Não foi possível obter o resultado do {pdf}.")