import streamlit as st
import openai
import PyPDF2
import datetime
import os


# FUNÇÃO QUE LÊ O PDF
def ler_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# API CHAT GPT
openai.api_key = os.environ.get("OPENAI_API_KEY")


def obter_resposta(pergunta, contexto):
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pergunta + "\nContexto: " + contexto,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.4  # define a imaginação dele
    )
    resposta_texto = resposta.choices[0].text.strip()

    # Verifica se a resposta termina com um ponto final
    if resposta_texto.endswith("."):
        return resposta_texto
    else:
        # Procura pelo último ponto final na resposta
        ultimo_ponto = resposta_texto.rfind(".")
        if ultimo_ponto != -1:
            return resposta_texto[:ultimo_ponto + 1]  # Retorna a resposta até o último ponto final encontrado
        else:
            return resposta_texto  # Retorna a resposta original caso não encontre um ponto final


def main():
    st.title("Projeto AÍ/Bubble")
    st.sidebar.title("Projeto IA")
    st.sidebar.write("André Silva Peixoto")
    st.sidebar.write("Felipe Angeli Cardoso de Aguiar")

    # Carrega os arquivos PDF
    uploaded_files = st.file_uploader("Carregue os seus arquivos PDF", type="pdf", accept_multiple_files=True)

    if uploaded_files is not None:
        # Pergunta pro gpt
        pergunta = st.text_input("Faça uma pergunta sobre os PDFs: ")

        if pergunta:
            # Tamanho da pergunta
            pergunta = pergunta[:50]

            # Concatena o texto de todos os arquivos PDF
            texto_pdf = ""
            for uploaded_file in uploaded_files:
                texto_pdf += ler_pdf(uploaded_file) + "\n"

            # Inicializa o contexto com o texto dos PDFs e o ano atual
            contexto = texto_pdf + "Ano atual: " + str(datetime.datetime.now().year)

            # Diminui o tamanho do contexto para ser mais eficiente o uso de tokens
            max_tokens_contexto = 4096 - len(pergunta) - len("\nContexto: ")
            contexto = contexto[:max_tokens_contexto]

            # Obtém a resposta inicial com base no contexto otimizado
            resposta = obter_resposta(pergunta, contexto)

            # Exibe a resposta
            st.write("Resposta do Chatbot: ")
            st.write(resposta)


if __name__ == "__main__":
    main()
