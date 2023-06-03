import streamlit as st
import openai
import PyPDF2


# FUNÇÃO QUE LÊ O PDF
def ler_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# API CHAT GPT
openai.api_key = "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"


def obter_resposta(pergunta, contexto):
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pergunta + "\nContexto: " + contexto,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.4   #define a imaginação dele
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

    # Carrega o arquivo PDF
    uploaded_file = st.file_uploader("Carregue o seu PDF", type="pdf")

    if uploaded_file is not None:
        # Lê o PDF e obtém o texto
        texto_pdf = ler_pdf(uploaded_file)

        # Pergunta pro gpt
        pergunta = st.text_input("Faça uma pergunta sobre o PDF: ")

        if pergunta:
            # Tamanho da pergunta
            pergunta = pergunta[:50]

            # Inicializa o contexto com o texto do PDF
            contexto = texto_pdf

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