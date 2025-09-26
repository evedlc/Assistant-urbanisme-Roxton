import streamlit as st
import fitz  # PyMuPDF
import openai

# Interface utilisateur
st.set_page_config(page_title="Assistant d'urbanisme", layout="wide")
st.title("Assistant d'urbanisme – Vérification de conformité réglementaire")

# Saisie de la clé API
api_key = st.text_input("🔑 Entrez votre clé API OpenAI", type="password")

# Saisie de la description du projet
project_description = st.text_area("📝 Description du projet d’urbanisme", height=200)

# Téléversement des fichiers PDF
uploaded_files = st.file_uploader("📄 Téléversez les fichiers PDF des règlements municipaux", type=["pdf"], accept_multiple_files=True)

# Bouton d'analyse
if st.button("Analyser la conformité du projet") and api_key and project_description and uploaded_files:
    # Lecture du contenu des fichiers PDF
    full_context = ""
    for file in uploaded_files:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        full_context += f"\n\n--- Document : {file.name} ---\n{text}"

    # Construction du prompt
    prompt = f"""
Tu es un expert en urbanisme municipal au Québec. Voici un projet d’urbanisme à analyser :

=== Description du projet ===
{project_description}

=== Documents de référence ===
{full_context}

=== Question ===
Le projet est-il conforme à l’ensemble des règlements municipaux ci-dessus ? Si non, indique précisément les éléments non conformes, les articles concernés, et propose des pistes de régularisation (ex. : dérogation mineure, PPCMOI, modification du projet).
"""

    # Appel à l'API OpenAI
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant d’urbanisme qui analyse la conformité réglementaire."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        st.success("✅ Analyse terminée")
        st.markdown("### Résultat de l’analyse :")
        st.write(answer)
    except Exception as e:
        st.error(f"Erreur lors de l’appel à l’API : {e}")
else:
    st.info("Veuillez entrer votre clé API, une description de projet et téléverser au moins un fichier PDF.")
