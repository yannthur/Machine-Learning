import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Token d'accès Dropbox 
load_dotenv()
ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")  # Inserer le token dans la variable d'environnement
if not ACCESS_TOKEN:
    st.error("Le token d'accès Dropbox n'est pas défini dans les variables d'environnement (DROPBOX_ACCESS_TOKEN).")

# Chemin Dropbox correspondant à l'URL publique partagée
FILE_PATH = "/data.xlsx"  # Assurez-vous que ce chemin est correct côté Dropbox
FILE_PATH_2 = "/data2.xlsx"

# Fonction pour télécharger le fichier Dropbox
def download_file_from_dropbox(path):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Dropbox-API-Arg": f'{{"path": "{path}"}}'
    }
    url = "https://content.dropboxapi.com/2/files/download"
    response = requests.post(url, headers=headers, stream=True)
    
    if response.status_code == 200:
        with open("data/"+path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return "data/"+path
    else:
        st.error(f"Erreur de téléchargement Dropbox : {response.status_code}")
        return None
        
liste_vaccin = ['YELLOW FEVER', 'Penta', 'VPO', 'VPI', 'nOPV2', 'TD','Mosquirix', 'PCV13', 'MEASLES', 'BCG', 'Janssen', 'Rota', 'MENINGO', 'HPV', 'Mencevax', 'Hepatite B']

data_ = None

# Initialization
if 'data' not in st.session_state:
    st.session_state['data'] = None

if 'data_file' not in st.session_state:
    st.session_state['data_file'] = None

if 'data_file_2' not in st.session_state:
    st.session_state['data_file_2'] = None

if 'auto_clean_state' not in st.session_state:
    st.session_state['auto_clean_state'] = None

if 'dataframe_mappi_region' not in st.session_state:
    st.session_state['dataframe_mappi_region'] = None

# chargement des donnees
@st.cache_data
def load_data(data_file):
    data = pd.read_excel(data_file)
    return data

# fontion de retraits des colonnes vide
def empty_columns_cleaner(data):
    temp = dict(data.isna().sum())
    _ = []
    for i in list(data.columns):
        if temp[f"{i}"] == data.shape[0] :
            _.append(i)
            data.drop(columns=f"{i}", inplace=True)
    return _

# fonction de retrait des colonnes avec une valeur unique
def remove_one_columns_values(data):
    _ = []
    for i in list(data.columns):
        if len(list(data[f"{i}"].unique())) == 1:
            data.drop(columns=f"{i}", inplace=True)
            _.append(i)
    return _


## gestion de l'importation et de la manipulation des donnees

# importation et previsualisation des donnees
if st.session_state['data_file'] is None:
    if os.path.exists("data/"+FILE_PATH):
        data_file = "data/"+FILE_PATH
    else:
        data_file = download_file_from_dropbox(path=FILE_PATH)
    st.session_state['data_file'] = data_file
else:
    data_file = st.session_state['data_file']

if st.session_state['data_file_2'] is None:
    if os.path.exists("data/"+FILE_PATH_2):
        data_file_2 = "data/"+FILE_PATH_2
    else:
        data_file_2 = download_file_from_dropbox(path=FILE_PATH_2)
    st.session_state['data_file_2'] = data_file_2
else:
    data_file_2 = st.session_state['data_file_2']

if data_file :
    data = load_data(data_file)
    # remplacement 
    st.session_state["data"] = data

     # afficher le jeu de donnees initiale
    st.header("Previsualisation des donnees pre-nettoyage")
    # creation des filtres et des fonctions d'explorations
    form_1 = st.form("filtre")
    with form_1:
        list_colonne = st.multiselect("Choisir les colonnes a appliquer", options=list(data.columns), )
        list_ligne = st.select_slider("Choisir les lignes a afficher", options=[i for i in range(0,data.shape[0])], value=(0,int(data.shape[0]-1)))
        col3, col4 = st.columns([4,1])
        with col3:
            btn_3 = st.form_submit_button("Appliquer", use_container_width=True)
        if btn_3:
            if list_colonne :
                data_ = data.loc[:,list(list_colonne)]
                if list_ligne:
                    data_ = data_.iloc[[i for i in range(list_ligne[0], list_ligne[1]+1)]]
            else:
                if list_ligne:
                    data_ = data
                    data_ = data_.iloc[[i for i in range(list_ligne[0], list_ligne[1]+1)]]
        with col4:
            btn_4 = st.form_submit_button("Reinitialiser",use_container_width=True)
            if btn_4:
                list_colonne.clear()
                list_ligne = ()
    
    # choix des colonnees a afficher

    expander_1 = st.expander("Previsualisation des donnees pre-nettoyage", expanded=True)
    with expander_1:
        if data_ is None:
            st.dataframe(data)
        else:
            st.dataframe(data_)
    st.write("___")

    if st.session_state['auto_clean_state'] == None :
        form_2 = st.form(key="form_1")
        with form_2:
            form_2.subheader("Souhaiter vous nettoyer automatiquement les donnees ?")
            col1,col2 = st.columns([1,1])
            with col1:
                btn_1 = st.form_submit_button("Accepter", use_container_width=True)
                if btn_1:
                    st.session_state['auto_clean_state'] = True
                    st.rerun()
            with col2:
                btn_2 = st.form_submit_button("Refuser", use_container_width=True)
                if btn_2:
                    st.session_state['auto_clean_state'] = False
                    st.rerun()
        st.write("___")

    if st.session_state['auto_clean_state'] == True :
        # netoyage des donnees
        st.header("Nettoyage des donnees")
        expander_2 = st.expander("Liste des operations")
        with expander_2:
            st.subheader("Retrait des colonnes vides")
            st.write("Liste des colonnes vides supprimer")
            _ = empty_columns_cleaner(data)
            st.write(_)
            st.subheader("Retrait des colonnes mono-value")
            st.write("Liste des colonnes mono-value")
            _ = remove_one_columns_values(data)
            st.write(_)
            st.session_state["data"] = data
        st.write("___")
        # afficher le je de donnees nettoyer

else : 
    st.warning("Veuillez selectionner le fichier a traiter")

