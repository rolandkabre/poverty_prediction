import streamlit as st
import pandas as pd
import pickle

# Charger le modèle
with open('meilleur_modele.pkl', 'rb') as file:
    modele = pickle.load(file)

st.markdown('<h1 style="color: blue;">Application de Prévision de la Pauvreté</h1>', unsafe_allow_html=True)

st.write('''
Cette application prédit votre niveau de pauvreté selon les données de l'enquête sur les conditions de vie des ménages de 2021.
Veuillez renseigner les paramètres et appuyer sur le bouton "Prédire" en bas pour obtenir la prédiction.
''')

st.header("Les paramètres d'entrée")

tage = st.number_input("Age du chef de ménage :", min_value=16, max_value=114, step=1)
genre = st.radio("Sexe du chef de ménage :", ["Masculin", "Féminin"])
genre_enc = 1 if genre == "Féminin" else 0
taille = st.number_input("Taille du ménage :", min_value=1, max_value=43, value=5, step=1)

milieu = st.radio("Milieu de résidence :", ["Rural", "Urbain"])
milieu_enc = 0 if milieu == "Rural" else 1

education_levels = ["Aucun", "Primaire", "Postprimaire", "Secondaire", "Superieur"]
education_mapping = {level: idx for idx, level in enumerate(education_levels)}
selected_education = st.selectbox("Niveau d'éducation du chef de ménage:", education_levels)
education_enc = education_mapping[selected_education]

occupation = st.radio("Statut du chef de ménage :", ["Non-occupé", "Travailleur"])
occupation_enc = 0 if occupation == "Non-occupé" else 1

logement_options = ["logem_Proprietaire sans titre", "logem_Locataire", "logem_Autre"]
selected_logement = st.selectbox("Statut d'occupation du logement:", logement_options)

elec = st.radio("Avez-vous accès à l'électricité :", ["Non", "Oui"])
elec_enc = 0 if elec == "Non" else 1

elec_solaire = st.radio("Utilisez-vous l'énergie solaire :", ["Non", "Oui"])
solaire_enc = 0 if elec_solaire == "Non" else 1

mur = st.radio("Votre résidence est-elle clôturée? :", ["Non", "Oui"])
mur_enc = 0 if mur == "Non" else 1

toilette = st.radio("Avez-vous des toilettes :", ["Non", "Oui"])
toilet_enc = 0 if toilette == "Non" else 1

input_data = {
    "hactiv12m": occupation_enc,
    "hage": tage,
    "hgender": genre_enc,
    "hhsize": taille,
    "milieu": milieu_enc,
    "toilet": toilet_enc,
    "elec_ur": solaire_enc,
    "elec_ac": elec_enc,
    "mur": mur_enc,
    "educ_rec": education_enc,
    **{col: 1 if col == selected_logement else 0 for col in logement_options}
}

input_df = pd.DataFrame([input_data])

st.write("Données encodées pour la prédiction:", input_df)

def faire_prediction(input_df):
    prediction = modele.predict(input_df)
    return prediction

if st.button("Prédire"):
    prediction = faire_prediction(input_df)
    prediction_value = prediction[0]
    classe_predite = {1: "Pauvres", 0: "Non Pauvres"}
    st.write(f"#### Vous êtes classés dans la catégorie des : **{classe_predite[prediction_value]}**")

st.write("**Auteur: Kabre Roland, Ingénieur Statisticien Économiste**")


