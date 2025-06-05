import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import random
from streamlit_echarts import st_pyecharts
from streamlit_echarts import st_echarts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts import options as opts
import requests
import os
from dotenv import load_dotenv

# Token d'accès Dropbox 
load_dotenv()
ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN") # Inserer le token dans la variable d'environnement
if not ACCESS_TOKEN:
    st.error("Le token d'accès Dropbox n'est pas défini dans les variables d'environnement (DROPBOX_ACCESS_TOKEN).")
FILE_PATH = "/data2.xlsx"  # Chemin du fichier dans Dropbox

# Fonction pour télécharger le fichier Dropbox
def download_file_from_dropbox():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Dropbox-API-Arg": f'{{"path": "{FILE_PATH}"}}'
    }
    url = "https://content.dropboxapi.com/2/files/download"
    response = requests.post(url, headers=headers, stream=True)
    
    if response.status_code == 200:
        with open("data/data2.xlsx", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return "data/data2.xlsx"
    else:
        st.error(f"Erreur de téléchargement Dropbox : {response.status_code}")
        return None



region_district = {
                "ADAMAOUA" : ["Bankim","Banyo","Belel","Dang","Djohong","Meiganga","Ngaoundal","Ngaoundere Rural","Ngaoundere Urbain","Tibati","Tignere"],
                "CENTRE" : ["Akonolinga","Awae","Ayos","Bafia","Biyem Assi","Cite Verte","Djoungolo","Ebebda","Efoulan","Elig Mfomo","Eseka","Esse","Evodoula","Mbalmayo","Mbandjock","Mbankomo","Mfou","Monatele","Mvog-Ada","Nanga Eboko","Ndikinimeki","Ngog Mapubi","Ngoumou","Nkolbisson","Nkolndongo","Ntui","Obala","Odza","Okola","Sa'a","Soa","Yoko"],
                "EST": ["Abong Mbang","Batouri","Belabo","Bertoua","Betare Oya","Doume","Garoua Boulai","Kette","Lomie","Mbang","Messamena","Moloundou","Ndelele","Nguelemendouka","Yokadouma"],
                "EXTREME NORD" : ["Bogo","Bourha","Fotokol","Gazawa","Goulfey","Guere","Guidiguis","Hina","Kaele","Kar Hay","Kolofata","Kousseri","Koza","Mada","Maga","Makary","Maroua 1","Maroua 2","Maroua 3","Meri","Mindif","Mogode","Mokolo","Mora","Moulvoudaye","Moutourwa","Mozogo","Pette","Roua","Tokombere","Vele","Waza","Yagoua"],
                "LITTORAL": ["Abo","Bangue","Boko","Bonassama","Cite Des Palmiers","Deido","Dibombari","Edea","Japoma","Logbaba","Loum","Manjo","Manoka","Mbanga","Melong","Ndom","New Bell","Ngambe","Njombe Penja","Nkondjock","Nkongsamba","Nylon","Pouma","Yabassi"],
                "NORD" : ["Bibemi","Figuil","Garoua I","Garoua II","Gaschiga","Golombe","Guider","Lagdo","Mayo Oulo","Ngong","Pitoa","Poli","Rey Bouba","Tchollire","Touboro"],
                "NORD OUEST" : ["Ako","Bafut","Bali","Bamenda","Bamenda 3","Batibo","Benakuma","Fundong","Kumbo East","Kumbo West","Mbengwi","Misaje","Ndop","Ndu","Njikwa","Nkambe","Nwa","Oku","Santa","Tubah","Wum"],
                "OUEST" : ["Bafang","Baham","Bamendjou","Bandja","Bandjoun","Bangangte","Bangourain","Batcham","Dschang","Foumban","Foumbot","Galim","Kekem","Kouoptamo","Malantouen","Massangam","Mbouda","Mifi","Penka Michel","Santchou"],
                "SUD" : ["Ambam","Djoum","Ebolowa","Kribi","Kye ossi","Lolodorf","Meyomessala","Mintom","Mvangan","Niete","Olamze","Sangmelima","Zoetele"],
                "SUD OUEST": ["Akwaya","Bakassi","Bamusso","Bangem","Buea","Ekondo Titi","Eyumodjock","Fontem","Konye","Kumba North","Kumba South","Limbe","Mamfe","Mbonge","Mundemba","Muyuka","Nguti","Tiko","Toko","Tombel","Wabane"]
}
liste_vaccin = ['YELLOW FEVER', 'Penta', 'VPO', 'VPI', 'nOPV2', 'TD','Mosquirix', 'PCV13', 'MEASLES', 'BCG', 'Janssen', 'Rota', 'MENINGO', 'HPV', 'Mencevax', 'Hepatite B']
liste_signe_symptome = {

    "code" : [    10022044,10001497,10002198,10002034,10002424,10061093,10002847,10002855,10003553,10049535,10069633,10060800,10006482,10005169,10005177,10019211,10002199,10011042,10010741,
                  10012373,10039906,10039083,10011703,10047555,10012174,10040844,10038687,10012735,10033371,10022086,10008479,10000081,10003239,10028411,10000084,10013968,10014625,10000087,
                  10015150,10041232,10042772,10028372,10016256,10037660,10033775,10008531,10025197,10018762,10019465,10018910,10039424,10020642,10020772,10071552,10021097,10023126,10022075,
                  10061218,10022437,10024264,10020937,10068319,10021089,10028813,10029864,10030095,10070774,10052139,10016029,10030302,10076569,10016062,10033799,10034037,10061428,10024855,
                  10017577,10061461,10005191,10042128,10011469,10037087,10052140,10052904,10037844,10020751,10058605,10080283,10030071,10039101,10022061,10030041,10055798,10040047,10015727,
                  10041349,10042241,10011878,10043071,10043089,10069381,10011224,10027327,10053425,10046735,10069555,10047340,10047513,100475132,10047700],

    "symptome" : ["Abcès au point d'injection", "Agitation", "Anaphylaxie", "Anémie", "Angioedème (généralisé ou localisé)", "Anomalies des nerfs crâniens", "Anurie",
                  "Anxiété", "Asthme", "Autres", "Baisse ou absence du contact visuel", "Bouffées de chaleur", "Bronchospame", "Cécité", "Cécité corticale",
                  "Céphalées", "Choc anaphylactique", "Clignement", "Conjonctivite", "Conscience altérée", "Convulsions", "Coryza", "Cyanose", "Déficit du champ visuel",
                  "Déshydratation", "Desquamation", "Détresse respiratoire", "Diarrhée", "Douleur", "Douleur au point d'injection", "Douleur thoracique", "Douleurs abdominales",
                  "Douleurs articulaires", "Douleurs musculaires", "Douleurs pelviennes", "Dyspnée", "Encéphalopathie", "Epigastralgie", "Erythème","Eternuement","Evanouissement/Syncope",
                  "Faiblesse motrice", "Fatigue / Prostration", "Fièvre", "Fourmillements", "Frissons", "Ganglion", "Geignement", "Hémiparésie", "Hémolyse", "Hypersalivation / hypersialorrhée",
                  "Hypersudation / Hyperhidrose", "Hypertension", "Hyporéactivité", "Hypotension", "Ictère", "Induration au point d'injection", "Inflammation", "Insomnie",
                  "Léthargie", "Lourdeur des membres", "Maux de gorge", "Modification des réflexes tendineux (hypo / hyper asymetrie)", "Nausée", "Nystagmus cérébelleux",
                  "Œdème", "Œdème des voies respiratoires hautes (lèvres, gorge, palais ou larynx)", "Œdème des yeux", "Œdème facial", "Oligurie", "Ophtalmoparésie", "Paralysie faciale",
                  "Paralysie flasque aiguë", "Parotidite", "Perte d'appétit (anorexie)", "Perte de connaissance", "Perte de l'équilibre", "Perturbations de la fonction érectile",
                  "Phlyctènes", "Plaies buccales", "Pleurs persistentes (> 3 heures)", "Prurit", "Prurit occulaire", "Raideur nucale", "Rash", "Réaction allergique", "Réflexe de moue succion",
                  "Refus de téter","Révulsion oculaire","Rhume", "Rougeur au point d'injection", "Rougeur des yeux", "Saignement (hémorrhagie)", "Sepsis", "Signes de Babinski", "Somnolence", "Stridor", "Surdité",
                  "Tachycardie, palpitations", "Tachypnée", "Temps de remplissage capillaire > 3s", "Toux", "Troubles du cycle menstruel", "Tuméfaction au point d'injection",
                  "Urticaire", "Utilisation excessive des muscles respiratoires accessoires", "Vertige", "Vision floue", "Voix rauque", "Vomissements"]
}

# Initialization
if 'data' not in st.session_state:
    st.session_state['data'] = None

if 'data_file_2' not in st.session_state:
    st.session_state['data_file_2'] = None

if 'data_2' not in st.session_state:
    st.session_state['data_2'] = None

if 'dataframe_mappi_region' not in st.session_state:
    st.session_state['dataframe_mappi_region'] = None

if st.session_state['data'] is None:
    st.warning("Veuillez entrer les données")
else :
    data = st.session_state['data']
    nav_bar1 = option_menu(None,
                       ["District silencieux", "Repartition des MAPPI"],
                        icons=['file-earmark-bar-graph-fill'],
                        menu_icon="cast",
                        default_index=0,
                        orientation="horizontal")


    ## gestion des districts silencieux
    if nav_bar1 == "District silencieux":
        region = []
        district = []
        col1, col2, col3 = st.columns([2,5,1])
        # creation du csv des district silencieux
        with col1 :
            for i in list(region_district.keys()):
                for k in region_district[f"{i}"] :
                    if data[data["admininfo/district"] == f"{k}".upper()].shape[0] == 0 :
                        region.append(i)
                        district.append(k)
            district_silencieux = {
                "Region" : region,
                "District": district
            }
            district_silencieux = pd.DataFrame(district_silencieux)
            st.write(district_silencieux)
            st.write("Nombre de district silencieux : ", district_silencieux.shape[0])
            st.write("Nombre de district present : ", len(list(data["admininfo/district"].unique())))

        # graphe de visualisation des district silencieux
        with col2:
            region_counts = district_silencieux.Region.value_counts().to_dict()
            regions = list(region_counts.keys())
            counts = list(region_counts.values())
            # Création du graphique
            # bar chart
            district_silencieux_bar = (
                Bar()
                .add_xaxis(regions)
                .add_yaxis("Nombre d'apparitions", counts)
                .set_global_opts(title_opts=opts.TitleOpts(title="Distribution des Régions"))
            )
            # Affichage avec Streamlit
            st_pyecharts(district_silencieux_bar, height="470px")

        with col3:
            # liste des district par region
            seleteur_1 = st.selectbox("Liste des district silencieux par region", options = list(district_silencieux["Region"].unique()))
            _ = []
            for i in list(district_silencieux.District[district_silencieux.Region == f"{seleteur_1}"]):
                _.append(i)
            st.write(_)

        st.write("___")

        col1, col2 = st.columns([1,4])
        with col2:
            # Création du pie chart complet (sans donut)
            district_silencieux_pie = (
                Pie()
                .add("", [list(z) for z in zip(regions, counts)])
                .set_global_opts(title_opts=opts.TitleOpts(title=""))
                .set_series_opts(
                    label_opts=opts.LabelOpts(formatter = "{b}: ({d}%)",
                                            position = "inside",  # Met le texte à l'intérieur du camembert
                                            font_size = 12,
                                            rotate = "radial")  # Affichage des pourcentages
                )
            )
            st_pyecharts(district_silencieux_pie, height="590px")
        with col1:
            # Taux de district silencieux par region
            st.subheader("Taux d'abstention par region")
            _ = []
            for i in list(region_district.keys()): # liste des regions
                # nombre de district de la region
                nbr_region_district = len(region_district[f"{i}"])
                # nombre de district silencieux de la region
                nbr_silenc_region_district = (district_silencieux[district_silencieux.Region == f"{i}"].shape[0])
                _.append((nbr_silenc_region_district/nbr_region_district)*100)

            taux_de_district_silencieux = {
                "region" : list(region_district.keys()),
                "taux de district silencieux" : [f"{round(k,2)}%" for k in _]
            }
            taux_de_district_silencieux = pd.DataFrame(taux_de_district_silencieux)
            st.dataframe(taux_de_district_silencieux, use_container_width = False)
        expander_2 = st.expander("District silentieux ", expanded=True)
        with expander_2:
            if st.session_state['data_file_2'] is None:
                data_file_2 = download_file_from_dropbox()
                st.session_state['data_file_2'] = data_file_2
            else:
                data_file_2 = st.session_state['data_file_2']

            if data_file_2:
                data_2 = pd.read_excel(data_file_2, engine="openpyxl")
                data_2['q6_district'] = data_2['q6_district'].str.replace('_', ' ')
                data_2['q6_district'] = data_2['q6_district'].str.replace('-', ' ')
                # determiner les district silencieux
                region_2 = []
                district_2 = []
                col1, col2, col3 = st.columns([2,5,1])
                # creation du csv des district silencieux
                with col1 :
                    for i in list(region_district.keys()):
                        for k in region_district[f"{i}"] :
                            if data_2[data_2["q6_district"] == f"{k}"].shape[0] == 0 :
                                region_2.append(i)
                                district_2.append(k)
                    district_silencieux_2 = {
                        "Region" : region_2,
                        "District": district_2
                    }
                col1, col2 = st.columns([5,9])
                with col1:
                    district_silencieux_2 = pd.DataFrame(district_silencieux_2)
                    st.write(district_silencieux_2)
                    st.write("Nombre de district silencieux : ", district_silencieux_2.shape[0])
                    st.write()
                with col2:
                    region_2_counts = district_silencieux_2.Region.value_counts().to_dict()
                    regions_2 = list(region_2_counts.keys())
                    counts_2 = list(region_2_counts.values())
                    district_silencieux_2_bar = (
                        Bar()
                        .add_xaxis(regions_2)
                        .add_yaxis("Nombre d'apparitions", counts_2)
                    )
                    # Affichage avec Streamlit
                    st_pyecharts(district_silencieux_2_bar, height="370px")
        
        st.write("___")
        if data_file_2:      
            expander_3 = st.expander("District silencieux absolue",expanded=True)
            with expander_3:
                st.header("Synthese")
                col1, col2 = st.columns([5,9])
                with col1:
                    df_common = district_silencieux.merge(district_silencieux_2, how='inner')
                    st.write(df_common)
                    st.write("Nombre de district silencieux : ", df_common.shape[0])
                    st.write()
                with col2:
                    region_2_counts = df_common .Region.value_counts().to_dict()
                    regions_2 = list(region_2_counts.keys())
                    counts_2 = list(region_2_counts.values())
                    district_silencieux_2_bar = (
                        Bar()
                        .add_xaxis(regions_2)
                        .add_yaxis("Nombre d'apparitions", counts_2)
                    )
                    # Affichage avec Streamlit
                    st_pyecharts(district_silencieux_2_bar, height="370px")


    if nav_bar1 == "Repartition des MAPPI":
        nav_bar2 = option_menu(None,
                            ["Carte" ,"Par region", "Par semaine épidémiologique", "Par vaccin"],
                                icons=['file-earmark-bar-graph-fill','file-earmark-bar-graph-fill', 'file-earmark-bar-graph-fill', 'file-earmark-bar-graph-fill'],
                                menu_icon="cast",
                                default_index=1,
                                orientation="horizontal")

        if nav_bar2 == "Par region" :
            expander_1 = st.expander("database Mappi par region", expanded=False)
            with expander_1:

                nbr_mappi_region = []

                for i in list(region_district.keys()):
                    x = data[data["admininfo/states"] == f"{i}"]
                    filtered_df = x[x['type_Vaccin'].isin(liste_vaccin)]
                    nbr_mappi_region.append(filtered_df.shape[0])

                # filtrage MAPPI grave
                filtered_df = data[data['type_Vaccin'].isin(liste_vaccin)] # filtrage du jeu de donnees
                # compter le nombre de mappi grave par region
                mappi_grave = []
                for i in list(region_district.keys()):
                    temp = filtered_df[filtered_df["admininfo/states"] == f"{i}"]
                    mappi_grave.append(temp[temp["seriousness/serious"] == 1.0].shape[0])
                # deduire le nombre de MAPPI non grave
                mappi_non_grave = []
                for i in range(0,10):
                    mappi_non_grave.append(nbr_mappi_region[i] - mappi_grave[i])

                # nombre de deces
                nbr_deces = []
                for i in list(region_district.keys()):
                    temp = filtered_df[filtered_df["admininfo/states"] == f"{i}"]
                    nbr_deces.append(temp[temp["seriousness/seriousnessdeath"] == 1.0].shape[0])

                dataframe_mappi_region = {
                        "region": list(region_district.keys()),
                        "Nombre de MAPPI" : nbr_mappi_region,
                        "Nombre de MAPPI non grave": mappi_non_grave,
                        "Nombre de MAPPI grave": mappi_grave,
                        "Nombre de deces" : nbr_deces
                    }
                dataframe_mappi_region = pd.DataFrame(dataframe_mappi_region)
                st.session_state['dataframe_mappi_region'] = dataframe_mappi_region

                st.dataframe(dataframe_mappi_region, use_container_width = True)
                col = st.columns(4)
                with col[0]:
                    st.write("Nombre totale de MAPPI : ", sum(nbr_mappi_region))
                with col[1]:
                    st.write("Nombre totale de MAPPI grave: ", sum(mappi_grave))
                with col[2]:
                    st.write("Nombre totale de MAPPI non grave: ", sum(mappi_non_grave))
                with col[3]:
                    st.write("Nombre de deces", sum(nbr_deces))
            st.write("___")

            col1, col2 = st.columns([4,1])
            with col2:
                # filtre
                form_1 = st.form("Filtre")
                with form_1:
                    seleteur_2 = st.multiselect("choisisez la/les regions", options=list(region_district.keys()))
                    btn_1 = st.form_submit_button("Appliquer", use_container_width=True)
                    btn_2 = st.form_submit_button("Reinitialiser", use_container_width=True)

            if btn_2:
                btn_1 = False

            with col1:
                if btn_1 and len(seleteur_2) > 0:
                    _1_ = []
                    _2_ = []
                    _3_ = []

                    for i in seleteur_2:
                        _1_.append(mappi_non_grave[list(region_district.keys()).index(i)])
                        _2_.append(mappi_grave[list(region_district.keys()).index(i)])
                        _3_.append(nbr_deces[list(region_district.keys()).index(i)])

                    district_silencieux_bar = (
                            Bar()
                            .add_xaxis(seleteur_2)
                            .add_yaxis("MAPPI NON GRAVE", _1_, itemstyle_opts=opts.ItemStyleOpts(color="#0F52BA"))
                            .add_yaxis("MAPPI GRAVE", _2_, itemstyle_opts=opts.ItemStyleOpts(color="#FF4B4B"))
                            .add_yaxis("Deces", _3_, itemstyle_opts=opts.ItemStyleOpts(color="#FFA62B"))
                            .set_global_opts(title_opts=opts.TitleOpts(title="Distribution des Régions"))
                        )
                        # Affichage avec Streamlit
                    st_pyecharts(district_silencieux_bar, height="470px")

                else:
                    district_silencieux_bar = (
                            Bar()
                            .add_xaxis(list(region_district.keys()))
                            .add_yaxis("MAPPI NON GRAVE", mappi_non_grave, itemstyle_opts=opts.ItemStyleOpts(color="#0F52BA"))
                            .add_yaxis("MAPPI GRAVE", mappi_grave, itemstyle_opts=opts.ItemStyleOpts(color="#FF4B4B"))
                            .add_yaxis("Deces", nbr_deces, itemstyle_opts=opts.ItemStyleOpts(color="#FFA62B"))
                            .set_global_opts(title_opts=opts.TitleOpts(title="Distribution des Régions"))
                        )
                        # Affichage avec Streamlit
                    st_pyecharts(district_silencieux_bar, height="470px")

        elif nav_bar2 == "Par semaine épidémiologique" :

            # filtrage MAPPI grave
            filtered_df = data[data['type_Vaccin'].isin(liste_vaccin)] # filtrage du jeu de donnees
            # liste des semaines vaccinales
            semaine_epidemiologique = list(filtered_df["Semaine_Epid"].unique())
            semaine_epidemiologique.sort()

            selecteur_3 = st.selectbox("Choisissez le type de vacin", options = liste_vaccin)
            # repartition des MAAPI par semaines vaccinal
            _ = []
            for i in semaine_epidemiologique:
                temp = filtered_df[(filtered_df["Semaine_Epid"] == f"{i}") & (filtered_df["type_Vaccin"] == selecteur_3)]
                _.append(temp.shape[0])
            # evolution des mappi par semaine vaccinal
            MAPPI_semaine_vaccinal_bar = (
                    Bar()
                    .add_xaxis(semaine_epidemiologique)
                    .add_yaxis("Nombre d'apparitions", _)
                    .set_global_opts(title_opts=opts.TitleOpts(title="Nombre de MAPPI par semaines épidémiologique"))
            )
            st_pyecharts(MAPPI_semaine_vaccinal_bar, width="100%", height="600px")

        elif nav_bar2 == "Par vaccin":
            selecteur_5 = st.selectbox("Choisir le Vaccin", options=liste_vaccin, index=0)
            col = st.columns(2)
            with col[0]:
                # filtre par sex:
                filtre_sex = st.toggle("Sexe")
            with col[1]:
                # filtre par tranche d'age
                list_tranche_dage = list(dict(data.Tranche_Age.value_counts()).keys())
                filtre_tranche_age = st.toggle("Tranche d'Age")


            # filtre des donnees selon les vaccin
            filtered_df = data[data['type_Vaccin'].isin(liste_vaccin)]
            # filtre selon le vaccin choisis
            filtered_df_2 = filtered_df[filtered_df["type_Vaccin"] == selecteur_5]
            # compte du nombre de MAPPI
            nbr_mappi = filtered_df_2.shape[0]
            # determination du nombre de mappi grave
            nbr_mappi_grave = filtered_df_2[filtered_df_2["seriousness/serious"] == 1.0].shape[0]
            # determination du nombre de mappi non grave
            nbr_mappi_non_grave = nbr_mappi - nbr_mappi_grave
            col = st.columns(3)
            with col[0]:
                st.write(f"Nombre de MAPPI : {nbr_mappi}")
            with col[1]:
                st.write(f"Nombre de mappi grave : {nbr_mappi_grave}")
            with col[2]:
                st.write(f"Nombre de mappi non grave : {nbr_mappi_non_grave}")
            st.write("___")

            if filtre_sex == True and filtre_tranche_age == False:
                ## filtre du nombre de mappi grave par sexe
                filtered_df_3 = filtered_df_2[filtered_df_2["seriousness/serious"] == 1.0]
                mappi_grave_homme = filtered_df_3[filtered_df_3["Sexe"] == "Masculin"].shape[0]
                mappi_grave_femme = filtered_df_3[filtered_df_3["Sexe"] != "Masculin"].shape[0]
                ## filtre mappi non grave par sexe
                filtered_df_3 = filtered_df_2[filtered_df_2["seriousness/serious"] == 2.0]
                mappi_non_grave_homme = filtered_df_3[filtered_df_3["Sexe"] == "Masculin"].shape[0]
                mappi_non_grave_femme = filtered_df_3[filtered_df_3["Sexe"] != "Masculin"].shape[0]
                col = st.columns(2)
                with col[0]:
                    st.subheader("HOMME")
                    ## graphe
                    Nbr_mappi_type_vaccin_homme = (
                        Bar()
                        .add_xaxis([selecteur_5])  # X-axis avec le vaccin sélectionné
                        .add_yaxis("Nombre de MAPPI non grave (HOMME)", [mappi_non_grave_homme])
                        .add_yaxis("Nombre de MAPPI grave (HOMME)", [mappi_grave_homme], itemstyle_opts=opts.ItemStyleOpts(color="#FF4B4B"))
                    )

                    # Affichage avec Streamlit
                    st_pyecharts(Nbr_mappi_type_vaccin_homme, height="470px")

                with col[1]:
                    st.subheader("FEMME")
                    Nbr_mappi_type_vaccin_femme = (
                        Bar()
                        .add_xaxis([selecteur_5])  # X-axis avec le vaccin sélectionné
                        .add_yaxis("Nombre de MAPPI non grave (FEMME)", [mappi_non_grave_femme])
                        .add_yaxis("Nombre de MAPPI grave (FEMME)", [mappi_grave_femme], itemstyle_opts=opts.ItemStyleOpts(color="#FF4B4B"))
                    )

                    # Affichage avec Streamlit
                    st_pyecharts(Nbr_mappi_type_vaccin_femme, height="470px")

            elif filtre_sex == False and filtre_tranche_age == True:
                _0_1_grave = []
                _1_5_grave = []
                _5_15_grave = []
                _15_18_grave = []
                _18_25_grave = []
                _25_35_grave = []
                _35_45_grave = []
                _45_55_grave = []
                _55_65_grave = []
                _65etPlus_grave = []

                _0_1_non_grave = []
                _1_5_non_grave = []
                _5_15_non_grave = []
                _15_18_non_grave = []
                _18_25_non_grave = []
                _25_35_non_grave = []
                _35_45_non_grave = []
                _45_55_non_grave = []
                _55_65_non_grave = []
                _65etPlus_non_grave = []

                filtered_df_3 = filtered_df_2[filtered_df_2["seriousness/serious"] == 1.0]
                filtered_df_4 = filtered_df_2[filtered_df_2["seriousness/serious"] == 2.0]
                for i in list_tranche_dage:
                    _ = filtered_df_3[filtered_df_3.Tranche_Age == f"{i}"].shape[0]

                    if i == '[0-1[':
                        _0_1_grave.append(_)
                    elif i == '[01-05[':
                        _1_5_grave.append(_)
                    elif i == '[05-15[':
                        _5_15_grave.append(_)
                    elif i == '[15-18[':
                        _15_18_grave.append(_)
                    elif i == '[18-25[':
                        _18_25_grave.append(_)
                    elif i == '[25-35[':
                        _25_35_grave.append(_)
                    elif i == '[35-45[':
                        _35_45_grave.append(_)
                    elif i == '[45-55[':
                        _45_55_grave.append(_)
                    elif i == '[55-65[':
                        _55_65_grave.append(_)
                    elif i == '65etPlus':
                        _65etPlus_grave.append(_)

                for i in list_tranche_dage:
                    _ = filtered_df_4[filtered_df_4.Tranche_Age == f"{i}"].shape[0]

                    if i == '[0-1[':
                        _0_1_non_grave.append(_)
                    elif i == '[01-05[':
                        _1_5_non_grave.append(_)
                    elif i == '[05-15[':
                        _5_15_non_grave.append(_)
                    elif i == '[15-18[':
                        _15_18_non_grave.append(_)
                    elif i == '[18-25[':
                        _18_25_non_grave.append(_)
                    elif i == '[25-35[':
                        _25_35_non_grave.append(_)
                    elif i == '[35-45[':
                        _35_45_non_grave.append(_)
                    elif i == '[45-55[':
                        _45_55_non_grave.append(_)
                    elif i == '[55-65[':
                        _55_65_non_grave.append(_)
                    elif i == '65etPlus':
                        _65etPlus_non_grave.append(_)

                # afficher la figure
                col = st.columns(2)
                with col[1]:
                    st.subheader("Mappi Grave")
                    Nbr_mappi_tranche_age_grave = (
                        Bar()
                        .add_xaxis([selecteur_5])
                        .add_yaxis("[0-1[", _0_1_grave)
                        .add_yaxis("[1-5[", _1_5_grave)
                        .add_yaxis("[5-15[", _5_15_grave)
                        .add_yaxis("[12-18[", _15_18_grave)
                        .add_yaxis("[18-25[", _18_25_grave)
                        .add_yaxis("[25-35[", _25_35_grave)
                        .add_yaxis("[35-45[", _35_45_grave)
                        .add_yaxis("[45-55[", _45_55_grave)
                        .add_yaxis("[55-65[", _55_65_grave)
                        .add_yaxis("65etPlus", _65etPlus_grave)
                    )
                    # Affichage avec Streamlit
                    st_pyecharts(Nbr_mappi_tranche_age_grave, height="470px")
                with col[0]:
                    st.subheader("Mappi non Grave")
                    Nbr_mappi_tranche_age_non_grave = (
                        Bar()
                        .add_xaxis([selecteur_5])  # Doit être une liste
                        .add_yaxis("[0-1[", _0_1_non_grave)
                        .add_yaxis("[1-5[", _1_5_non_grave)
                        .add_yaxis("[5-15[", _5_15_non_grave)
                        .add_yaxis("[12-18[", _15_18_non_grave)
                        .add_yaxis("[18-25[", _18_25_non_grave)
                        .add_yaxis("[25-35[", _25_35_non_grave)
                        .add_yaxis("[35-45[", _35_45_non_grave)
                        .add_yaxis("[45-55[", _45_55_non_grave)
                        .add_yaxis("[55-65[", _55_65_non_grave)
                        .add_yaxis("65etPlus", _65etPlus_non_grave)
                    )
                    # Affichage avec Streamlit
                    st_pyecharts(Nbr_mappi_tranche_age_non_grave, height="470px")

            elif  filtre_sex == True and filtre_tranche_age == True:
                filtre_sex = False
            else:
                # Création du graphique
                Nbr_mappi_type_vaccin = (
                    Bar()
                    .add_xaxis([selecteur_5])  # Doit être une liste
                    .add_yaxis("Nombre de MAPPI non grave", [nbr_mappi_non_grave])
                    .add_yaxis("Nombre de MAPPI grave", [nbr_mappi_grave], itemstyle_opts=opts.ItemStyleOpts(color="#FF4B4B"))
                    .set_global_opts(title_opts=opts.TitleOpts(title="Distribution des MAPPI par Vaccin"))
                )

                # Affichage avec Streamlit
                st_pyecharts(Nbr_mappi_type_vaccin, height="470px")

        elif nav_bar2 == "Carte":
            latitude = []
            longitude = []
            selecteur_6 = st.selectbox("Choisir le Vaccin", options=liste_vaccin)
            # filtre par vaccin
            filtered_df = data[data['type_Vaccin'].isin(liste_vaccin)]
            # filtre sur le vaccin specifique
            filtered_df_2 = filtered_df[filtered_df['type_Vaccin'] == selecteur_6]

            st.map(filtered_df_2, latitude= "_gps_beginning_latitude", longitude= "_gps_beginning_longitude")
