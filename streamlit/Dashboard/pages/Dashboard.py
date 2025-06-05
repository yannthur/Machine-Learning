import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts import options as opts

liste_vaccin = ['YELLOW FEVER', 'Penta', 'VPO', 'VPI', 'nOPV2', 'TD','Mosquirix', 'PCV13', 'MEASLES', 'BCG', 'Janssen', 'Rota', 'MENINGO', 'HPV', 'Mencevax', 'Hepatite B']

region_district = {
    "ADAMAOUA" : ["Bankim","Banyo","Belel","Dang","Djohong","Meiganga","Ngaoundal","Ngaoundere Rural","Ngaoundere Urbain","Tibati","Tignere"],
    "CENTRE" : ["Akonolinga","Awae","Ayos","Bafia","Biyem Assi","Cite Verte","Djoungolo","Ebebda","Efoulan","Elig Mfomo","Eseka","Esse","Evodoula","Mbalmayo","Mbandjock","Mbankomo","Mfou","Monatele","Mvog-Ada","Nanga Eboko","Ndikinimeki","Ngog Mapubi","Ngoumou","Nkolbisson","Nkolndongo","Ntui","Obala","Odza","Okola","Sa'a","Soa","Yoko"],
    "EST": ["Abong_Mbang","Batouri","Belabo","Bertoua","Betare_Oya","Doume","Garoua_Boulai","Kette","Lomie","Mbang","Messamena","Moloundou","Ndelele","Nguelemendouka","Yokadouma"],
    "EXTREME NORD" : ["Bogo","Bourha","Fotokol","Gazawa","Goulfey","Guere","Guidiguis","Hina","Kaele","Kar Hay","Kolofata","Kousseri","Koza","Mada","Maga","Makary","Maroua 1","Maroua 2","Maroua 3","Meri","Mindif","Mogode","Mokolo","Mora","Moulvoudaye","Moutourwa","Mozogo","Pette","Roua","Tokombere","Vele","Waza","Yagoua"],
    "LITTORAL": ["Abo","Bangue","Boko","Bonassama","Cite Des Palmiers","Deido","Dibombari","Edea","Japoma","Logbaba","Loum","Manjo","Manoka","Mbanga","Melong","Ndom","New Bell","Ngambe","Njombe Penja","Nkondjock","Nkongsamba","Nylon","Pouma","Yabassi"],
    "NORD" : ["Bibemi","Figuil","Garoua I","Garoua II","Gaschiga","Golombe","Guider","Lagdo","Mayo Oulo","Ngong","Pitoa","Poli","Rey Bouba","Tchollire","Touboro"],
    "NORD OUEST" : ["Ako","Bafut","Bali","Bamenda","Bamenda 3","Batibo","Benakuma","Fundong","Kumbo East","Kumbo West","Mbengwi","Misaje","Ndop","Ndu","Njikwa","Nkambe","Nwa","Oku","Santa","Tubah","Wum"],
    "OUEST" : ["Bafang","Baham","Bamendjou","Bandja","Bandjoun","Bangangte","Bangourain","Batcham","Dschang","Foumban","Foumbot","Galim","Kekem","Kouoptamo","Malantouen","Massangam","Mbouda","Mifi","Penka Michel","Santchou"],
    "SUD" : ["Ambam","Djoum","Ebolowa","Kribi","Kye-ossi","Lolodorf","Meyomessala","Mintom","Mvangan","Niete","Olamze","Sangmelima","Zoetele"],
    "SUD OUEST": ["Akwaya","Bakassi","Bamusso","Bangem","Buea","Ekondo Titi","Eyumodjock","Fontem","Konye","Kumba-North","Kumba-South","Limbe","Mamfe","Mbonge","Mundemba","Muyuka","Nguti","Tiko","Toko","Tombel","Wabane"]
}

list_tranche_dage = ["[0-1[","[01-05[","[05-15[","[15-18[","[18-25[","[25-35[","[35-45[","[45-55[","[55-65[","65etPlus"]

nav_bar1 = option_menu(None,
                   ["global", "Resume"],
                    icons=['file-earmark-bar-graph-fill'],
                    menu_icon="cast",
                    default_index=0,
                    orientation="horizontal")

# Initialization
if 'data' not in st.session_state:
    st.session_state['data'] = None

if 'dataframe_mappi_region' not in st.session_state:
    st.session_state['dataframe_mappi_region'] = None

if st.session_state['data'] is None:
    st.warning("Veuillez entrer les données")
else:

    data = st.session_state['data']

    temp = liste_vaccin.copy()
    temp.append("Global")

    if nav_bar1 == "Resume":
        ## resume mappi grave
        # filtre des donnees pour garder les mappi grave
        filtered_df = data[data['type_Vaccin'].isin(liste_vaccin)]  
        filtered_df_2 = filtered_df[filtered_df['seriousness/serious'] == 1.0]
        df = (filtered_df_2[["admininfo/states","admininfo/district",'patien',"admininfo/safetyreportid","Age","Tranche_Age","Sexe","type_Vaccin", "event/reactionstartdate", "event/primarysourcereaction","reporter/reportergivename", "reporter/reportertel", "reporter/reporteremail", "_index",
                "Semaine_Epid","seriousness/seriousnessdeath", "healthproduct/drugadmin/intervention"]])
        df['devenir'] = df["seriousness/seriousnessdeath"].apply(lambda x: 'décédé' if x == 1.0 else 'vivant')
        df.loc[df["type_Vaccin"] == "nOPV2", "healthproduct/drugadmin/intervention"] = "masscampaign"
        if pd.api.types.is_numeric_dtype(df["event/reactionstartdate"]):
            df["event/reactionstartdate"] = pd.to_datetime(
                df["event/reactionstartdate"], origin="1899-12-30", unit="D"
            ).dt.date
        else:
            df["event/reactionstartdate"] = pd.to_datetime(df["event/reactionstartdate"]).dt.date

        
        df = df.rename(columns={"admininfo/states": "REGIONS"})
        df = df.rename(columns={"admininfo/district": "DISTRICT"})
        df = df.rename(columns={"patien": "INITIAUX DU PATIENT"})
        df = df.rename(columns={"admininfo/safetyreportid": "NUM EPID"})
        df = df.rename(columns={"Age": "AGE"})
        df = df.rename(columns={"Tranche_Age": "TRANCHE AGE"})
        df = df.rename(columns={"Sexe": "SEXE"})
        df = df.rename(columns={"type_Vaccin": "TYPE VACCIN"})
        df = df.rename(columns={"event/reactionstartdate": "DATE DEBUT REACTION"})
        df = df.rename(columns={"event/primarysourcereaction": "PREMIERS SIGNES"})
        df = df.rename(columns={"reporter/reportergivename": "NOTIFICATEURS"})
        df = df.rename(columns={"reporter/reportertel": "NUMERO NOTIFICATEURS"})
        df = df.rename(columns={"reporter/reporteremail": "ADRESSE NOTIFICATEURS"})
        df = df.rename(columns={"_index": "NUMERO INDEX"})
        df = df.rename(columns={"Semaine_Epid": "SEMAINE EPI"})
        df = df.rename(columns={"healthproduct/drugadmin/intervention": "CIRCONSTANCE DE VACCINATION"})
        df = df.rename(columns={"devenir": "DEVENIR"})

        expander_0 = st.expander("resume")
        with expander_0:
            st.write(df[["REGIONS","DISTRICT",'INITIAUX DU PATIENT',"NUM EPID","AGE","TRANCHE AGE","SEXE","TYPE VACCIN","DATE DEBUT REACTION", "PREMIERS SIGNES","NOTIFICATEURS", "NUMERO NOTIFICATEURS", "ADRESSE NOTIFICATEURS", "NUMERO INDEX",
                      "SEMAINE EPI", "CIRCONSTANCE DE VACCINATION", "DEVENIR"]])
        st.write("___")
        col1,col2, col3, col4, col5 = st.columns([1,1,1,2,2])
        with col1:
            nbr_region_contnair = st.container(border=True)
            with nbr_region_contnair:
                st.write("Nombre de regions")
                st.subheader(len(list(df["REGIONS"].unique())))
        
        with col2:
            nbr_district_contnair = st.container(border=True)
            with nbr_district_contnair:
                st.write("Nombre de district")
                st.subheader(len(list(df["DISTRICT"].unique())))

        with col3:
            nbr_cas_contnair = st.container(border=True)
            with nbr_cas_contnair:
                st.write("Nombre de cas")
                st.subheader(df.shape[0])

        with col4:
            repartition_sex_contnair = st.container(border=True)
            with repartition_sex_contnair:
                st.write("Repartitions pas sexe")
                st.subheader(f"{len(df[df.SEXE == 'Masculin'])} Hommes / {len(df[df.SEXE == 'Féminin'])} Femmes")

        with col5:
            nbr_mort_contnair = st.container(border=True)
            with nbr_mort_contnair:
                st.write("Rapport mort/survivant")
                st.subheader(f"{df[df.DEVENIR == 'décédé'].shape[0]} mort / {df[df.DEVENIR != 'décédé'].shape[0]} survivants")

        col1, col2 = st.columns([2.3,4])
        with col1:
            circonstance_vaccination_contnair = st.container(border=True)
            with circonstance_vaccination_contnair:
                st.write("Circonstances de vaccination")
                st.subheader(f"{len(df[df['CIRCONSTANCE DE VACCINATION'] == 'masscampaign'])} masscampaign / {len(df[df['CIRCONSTANCE DE VACCINATION'] != 'masscampaign'])} routineimmunization")

        with col2:
            reppartition_type_vaccin = st.expander("Repartission des vaccins",expanded=True)
            with reppartition_type_vaccin:
                for i in sorted(list(df["TYPE VACCIN"].unique())):
                    st.write(f"{i} : {df[df['TYPE VACCIN'] == i].shape[0]}")
    else:


    
        vaccin_type = st.selectbox("Choissisez le type de vaccin", options= temp, index=len(temp)-1)

        # filtre de donnees pour isolees les mappi
        filtered_df = data[data['type_Vaccin'].isin(liste_vaccin)]      
        if vaccin_type == "Global":
            filtered_df_2 = filtered_df
        else:
            # filtre les donnees par vaccin
            filtered_df_2 = filtered_df[filtered_df["type_Vaccin"] == vaccin_type]

        # affichage de la carte et des indicateur par type de vaccin
        col1, col2 = st.columns([4,6])
        with col1:
            filtre_carte = st.pills("filtre de carte", options=["Mappi grave", "Mappi non grave"], label_visibility="collapsed")
            if filtre_carte is None:
                st.map(filtered_df_2, latitude= "_gps_beginning_latitude", longitude= "_gps_beginning_longitude", use_container_width=True, height=608)
            elif filtre_carte == "Mappi grave":
                filtered_df_5 = filtered_df_2[filtered_df_2["seriousness/serious"] == 1.0]
                st.map(filtered_df_5, latitude= "_gps_beginning_latitude", longitude= "_gps_beginning_longitude", use_container_width=True, height=608)
            elif filtre_carte == "Mappi non grave":
                filtered_df_5 = filtered_df_2[filtered_df_2["seriousness/serious"] == 2.0]
                st.map(filtered_df_5, latitude= "_gps_beginning_latitude", longitude= "_gps_beginning_longitude", use_container_width=True, height=608)
            # affichage des card (nbr mappi , nbr mappi grave, nbr mappi non grave)

        with col2:
            col = st.columns(4)
            nbr_mappi = filtered_df_2.shape[0]
            nbr_mappi_grave = filtered_df_2[ (filtered_df_2['seriousness/serious'] == 1.0) ].shape[0]
            nbr_mappi_non_grave = filtered_df_2[ (filtered_df_2['seriousness/serious'] == 2.0) ].shape[0]
            nbr_desces = filtered_df_2[filtered_df_2["seriousness/seriousnessdeath"] == 1.0].shape[0]
            # nbr mappi
            with col[0]:
                nbr_mappi_card = st.container(border=True)
                with nbr_mappi_card :
                    st.markdown("Nombre de MAPPI")
                    st.header(f"{nbr_mappi}")
            # nbr mappi grave
            with col[1]:
                nbr_mappi_grave_card = st.container(border=True)
                with nbr_mappi_grave_card:
                    st.markdown("Nombre de MAPPI grave")
                    st.header(f"{nbr_mappi_grave}")
            # nbr mappi non grave
            with col[2]:
                nbr_mappi_non_grave_card = st.container(border=True)
                with nbr_mappi_non_grave_card:
                    st.markdown("Nombre de MAPPI non grave")
                    st.header(f"{nbr_mappi_non_grave}")
            # nbr desces
            with col[3]:
                nbr_desces_card = st.container(border=True)
                with nbr_desces_card:
                    st.markdown("Nombre de deces")
                    st.header(f"{nbr_desces}")

            # graphe repartition des mappi
            graph_mappi = st.container(border=True)
            with graph_mappi:
                col1, col2, col3, col4 = st.columns([1,1,1,1])
                with col1:
                    filtre_1 = st.pills(" ", options=["Distribution"], label_visibility="collapsed")
                with col2:    
                    filtre_2 = st.toggle("Sexe")
                with col3:    
                    filtre_3 = st.toggle("Tranche d'age")
                with col4:
                    if filtre_1 is None:
                        filtre = st.pills("", options=["Par region", "Par semaine épidémiologique"], label_visibility= "collapsed")
                    else:
                        filtre = st.pills("", options=["Par region", "Par semaine épidémiologique"], label_visibility= "collapsed", disabled=True)

                if filtre is None and filtre_1 is None:
                    if filtre_2 == True and filtre_3 == False:
                        # filtrer par sexe
                        # mappi grave
                        filtered_df_3 = filtered_df_2[filtered_df_2["seriousness/serious"] == 1.0]
                        mappi_grave_homme = filtered_df_3[filtered_df_3["Sexe"] == "Masculin"].shape[0]
                        mappi_grave_femme = filtered_df_3[filtered_df_3["Sexe"] != "Masculin"].shape[0]
                        # mappi non grave
                        filtered_df_3 = filtered_df_2[filtered_df_2["seriousness/serious"] == 2.0]
                        mappi_grave_non_homme = filtered_df_3[filtered_df_3["Sexe"] == "Masculin"].shape[0]
                        mappi_grave_non_femme = filtered_df_3[filtered_df_3["Sexe"] != "Masculin"].shape[0]
                        # desces
                        filtered_df_3 = filtered_df_2[filtered_df_2["seriousness/seriousnessdeath"] == 1.0]
                        desces_homme = filtered_df_3[filtered_df_3["Sexe"] == "Masculin"].shape[0]
                        desces_femme = filtered_df_3[filtered_df_3["Sexe"] != "Masculin"].shape[0]

                        ## afficher les graphes
                        col = st.columns(2)
                        with col[0]:
                            st.subheader("Homme")
                            Nbr_mappi_type_vaccin = (
                                Bar()
                                .add_xaxis(["Mappi grave", "Mappi non grave", "Deces"])  # Assurez-vous que c'est une liste
                                .add_yaxis("Nombre de MAPPI grave", [mappi_grave_homme, mappi_grave_non_homme, desces_homme])
                            )
                            # Affichage du graphique
                            st_pyecharts(Nbr_mappi_type_vaccin, height="330px")

                        with col[1]:
                            st.subheader("Femme")
                            Nbr_mappi_type_vaccin = (
                                 Bar()
                                 .add_xaxis(["Mappi grave", "Mappi non grave", "Deces"])  # Assurez-vous que c'est une liste
                                 .add_yaxis("Nombre de MAPPI grave", [mappi_grave_femme, mappi_grave_non_femme, desces_femme])
                             )
                             # Affichage du graphique
                            st_pyecharts(Nbr_mappi_type_vaccin, height="303px")

                    elif filtre_3 == True and filtre_2 == False:
                        _0_1_grave = None
                        _1_5_grave = None
                        _5_15_grave = None
                        _15_18_grave = None
                        _18_25_grave = None
                        _25_35_grave = None
                        _35_45_grave = None
                        _45_55_grave = None
                        _55_65_grave = None
                        _65etPlus_grave = None

                        _0_1_non_grave = None
                        _1_5_non_grave = None
                        _5_15_non_grave = None
                        _15_18_non_grave = None
                        _18_25_non_grave = None
                        _25_35_non_grave = None
                        _35_45_non_grave = None
                        _45_55_non_grave = None
                        _55_65_non_grave = None
                        _65etPlus_non_grave = None

                        filtered_df_3 = filtered_df_2[filtered_df_2["seriousness/serious"] == 1.0]
                        filtered_df_4 = filtered_df_2[filtered_df_2["seriousness/serious"] == 2.0]

                        for i in list_tranche_dage:
                            _ = filtered_df_3[filtered_df_3.Tranche_Age == f"{i}"].shape[0]
                            if i == '[0-1[':
                                _0_1_grave = _
                            elif i == '[01-05[':
                                _1_5_grave = _
                            elif i == '[05-15[':
                                _5_15_grave = _
                            elif i == '[15-18[':
                                _15_18_grave = _
                            elif i == '[18-25[':
                                _18_25_grave = _
                            elif i == '[25-35[':
                                _25_35_grave = _
                            elif i == '[35-45[':
                                _35_45_grave = _
                            elif i == '[45-55[':
                                _45_55_grave = _
                            elif i == '[55-65[':
                                _55_65_grave = _
                            elif i == '65etPlus':
                                _65etPlus_grave = _

                        for i in list_tranche_dage:
                            _ = filtered_df_4[filtered_df_4.Tranche_Age == f"{i}"].shape[0]
                            if i == '[0-1[':
                                _0_1_non_grave = _
                            elif i == '[01-05[':
                                _1_5_non_grave = _
                            elif i == '[05-15[':
                                _5_15_non_grave = _
                            elif i == '[15-18[':
                                _15_18_non_grave = _
                            elif i == '[18-25[':
                                _18_25_non_grave = _
                            elif i == '[25-35[':
                                _25_35_non_grave = _
                            elif i == '[35-45[':
                                _35_45_non_grave = _
                            elif i == '[45-55[':
                                _45_55_non_grave = _
                            elif i == '[55-65[':
                                _55_65_non_grave = _
                            elif i == '65etPlus':
                                _65etPlus_non_grave = _

                        col = st.columns(2)  
                        with col[0]:  
                            # Création du graphique
                            Nbr_mappi_tranche_age_grave = (
                                Bar()
                                .add_xaxis(list_tranche_dage)
                                .add_yaxis(
                                    "Mappi grave",
                                    [_0_1_grave, _1_5_grave, _5_15_grave, _15_18_grave, _18_25_grave, 
                                     _25_35_grave, _35_45_grave, _45_55_grave, _55_65_grave, _65etPlus_grave]
                                )
                            )

                            # Affichage avec Streamlit
                            st_pyecharts(Nbr_mappi_tranche_age_grave, height="370px")
                        with col[1]:
                            Nbr_mappi_tranche_age_grave = (
                                Bar()
                                .add_xaxis(list_tranche_dage)
                                .add_yaxis(
                                    "Mappi non grave",
                                    [_0_1_non_grave, _1_5_non_grave, _5_15_non_grave, _15_18_non_grave, _18_25_non_grave, 
                                     _25_35_non_grave, _35_45_non_grave, _45_55_non_grave, _55_65_non_grave, _65etPlus_non_grave]
                                )
                            )
                            # Affichage avec Streamlit
                            st_pyecharts(Nbr_mappi_tranche_age_grave, height="370px")
                    else:
                        Nbr_mappi_type_vaccin = (
                            Bar()
                            .add_xaxis([vaccin_type])  # Assurez-vous que c'est une liste
                            .add_yaxis("Nombre de MAPPI grave", [filtered_df_2[filtered_df_2['seriousness/serious'] == 1.0].shape[0]], itemstyle_opts=opts.ItemStyleOpts(color="#FF4B4B"))
                            .add_yaxis("Nombre de MAPPI non grave", [filtered_df_2[filtered_df_2['seriousness/serious'] == 2.0].shape[0]], itemstyle_opts=opts.ItemStyleOpts(color="#0F52BA"))
                            .add_yaxis("Nombre deces", [filtered_df_2[filtered_df_2["seriousness/seriousnessdeath"] == 1.0].shape[0]], itemstyle_opts=opts.ItemStyleOpts(color="#FFA62B"))
                        )
                        # Affichage du graphique
                        st_pyecharts(Nbr_mappi_type_vaccin, height="370px")

                elif filtre == "Par region" and filtre_1 is None:
                    ## recalcule des elements par region
                    # donnees selon le vaccin "filtered_df_2"
                    # liste des mappi grave par region
                    mappi_grave = []
                    mappi_non_grave = []
                    desces = []
                    for i in list(region_district.keys()):
                       mappi_grave.append(filtered_df_2[(filtered_df_2['seriousness/serious'] == 1.0) & (filtered_df_2["admininfo/states"] == f"{i}")].shape[0])
                       mappi_non_grave.append(filtered_df_2[(filtered_df_2['seriousness/serious'] == 2.0) & (filtered_df_2["admininfo/states"] == f"{i}")].shape[0])
                       desces.append(filtered_df_2[(filtered_df_2['seriousness/seriousnessdeath'] == 1.0) & (filtered_df_2["admininfo/states"] == f"{i}")].shape[0])
                    # afficher le graphe
                    district_silencieux_bar = (
                            Bar()
                            .add_xaxis(list(region_district.keys()))
                            .add_yaxis("MAPPI NON GRAVE", mappi_non_grave, itemstyle_opts=opts.ItemStyleOpts(color="#F1F54F"))
                            .add_yaxis("MAPPI GRAVE",mappi_grave, itemstyle_opts=opts.ItemStyleOpts(color="#ECA412"))
                            .add_yaxis("Deces", desces, itemstyle_opts=opts.ItemStyleOpts(color="#FF4B4B"))
                            .set_global_opts(title_opts=opts.TitleOpts(title="Distribution des Régions"))
                        )
                        # Affichage avec Streamlit
                    st_pyecharts(district_silencieux_bar, height="370px")

                elif filtre == "Par semaine épidémiologique" and filtre_1 is None:
                    # repartition des MAAPI par semaines vaccinal
                    semaine_epidemiologique = list(filtered_df["Semaine_Epid"].unique())
                    semaine_epidemiologique.sort()
                    _ = []
                    for i in semaine_epidemiologique:
                        if vaccin_type == "Global":
                           temp = filtered_df_2[(filtered_df_2["Semaine_Epid"] == f"{i}")] 
                        else:
                            temp = filtered_df_2[(filtered_df_2["Semaine_Epid"] == f"{i}") & (filtered_df_2["type_Vaccin"] == vaccin_type)]
                        _.append(temp.shape[0])
                    # evolution des mappi par semaine vaccinal
                    MAPPI_semaine_vaccinal_bar = (
                            Bar()
                            .add_xaxis(semaine_epidemiologique)
                            .add_yaxis("Nombre d'apparitions",_)
                            .set_global_opts(title_opts=opts.TitleOpts(title="Nombre de MAPPI"))
                    )
                    st_pyecharts(MAPPI_semaine_vaccinal_bar, width="100%", height="370px")

                elif filtre_1 is not None:
                    # Définition des catégories et valeurs
                    labels = ["MAPPI grave", "MAPPI non grave", "Deces"]
                    values = [
                        filtered_df_2[filtered_df_2['seriousness/serious'] == 1.0].shape[0],
                        filtered_df_2[filtered_df_2['seriousness/serious'] == 2.0].shape[0],
                        filtered_df_2[filtered_df_2["seriousness/seriousnessdeath"] == 1.0].shape[0]
                    ]               

                    # Création du Pie Chart
                    pie_chart = (
                        Pie()
                        .add("", [list(z) for z in zip(labels, values)])
                        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))  # Affichage des pourcentages
                    )               

                    # Affichage du graphique dans Streamlit
                    st_pyecharts(pie_chart, height="370px")
        st.write("___")
        # gestion des district silentieux
        col1,col2= st.columns([3.5,2])
        with col1:
            compte_district_silencieux = st.container(border=True)
            with compte_district_silencieux:
                #distribution = st.pills("filtre distribution", options=["Distribution"], label_visibility="collapsed", key= 1)
                if vaccin_type == "Global":
                    region = []
                    district = []
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
                    region_counts = district_silencieux.Region.value_counts().to_dict()
                    regions = list(region_counts.keys())
                    counts = list(region_counts.values())
                    # Création du graphique
                    # bar chart
                    district_silencieux_bar = (
                        Bar()
                        .add_xaxis(regions)
                        .add_yaxis("Nombre d'apparitions", counts)
                        .set_global_opts(title_opts=opts.TitleOpts(title="Repartition district silencieux"))
                    )
                    # Affichage avec Streamlit
                    st_pyecharts(district_silencieux_bar, height="534px")
                else:
                    region = []
                    district = []
                    for i in list(region_district.keys()):
                        for k in region_district[f"{i}"] :
                            if filtered_df_2[filtered_df_2["admininfo/district"] == f"{k}".upper()].shape[0] == 0 :
                                region.append(i)
                                district.append(k)
                    district_silencieux = {
                        "Region" : region,
                        "District": district
                    }
                    district_silencieux = pd.DataFrame(district_silencieux)
                    region_counts = district_silencieux.Region.value_counts().to_dict()
                    regions = list(region_counts.keys())
                    counts = list(region_counts.values())
                    # Création du graphique
                    # bar chart
                    district_silencieux_bar = (
                        Bar()
                        .add_xaxis(regions)
                        .add_yaxis("Nombre d'apparitions", counts)
                    )
                    # Affichage avec Streamlit
                    st_pyecharts(district_silencieux_bar, height="534px")

        with col2:
            # carte du nombre de district silencieux
            col = st.columns(2)
            with col[0]:
                nbr_district_silencieux_card = st.container(border=True)
                with nbr_district_silencieux_card:
                    st.write("Nombre de district manquant")
                    st.subheader(f"{district_silencieux.shape[0]}")

            with col[1]:
                taux_dabstention_card = st.container(border=True)
                with taux_dabstention_card:
                    st.write("Taux de district manquant")
                    st.subheader(f"{round((district_silencieux.shape[0]/205)*100,2)} %")

            st.write("___")
            taux_abstention_region = st.container(border=True)
            with taux_abstention_region:
                _ = []
                for i in list(region_district.keys()): # liste des regions
                    # nombre de district de la region
                    nbr_region_district = len(region_district[f"{i}"])
                    # nombre de district silencieux de la region
                    nbr_silenc_region_district = (district_silencieux[district_silencieux.Region == f"{i}"].shape[0])
                    _.append((nbr_silenc_region_district/nbr_region_district)*100)

                taux_de_district_silencieux = {
                    "region" : list(region_district.keys()),
                    "taux de district silencieux" : [round(k,2) for k in _]
                }
                taux_de_district_silencieux = pd.DataFrame(taux_de_district_silencieux)          
                st.dataframe(taux_de_district_silencieux, use_container_width=True)
        # liste des district manquants
        expander_1 = st.expander("Liste des district manquant", expanded=True)
        with expander_1:
            col1, col2 = st.columns([4,1])
            with col1:
                region = st.selectbox("Choisir la region",options=list(region_district.keys()))
            with col2:
                st.write("")
                st.write("")
                btn_1 = st.button("Appliquer", use_container_width=True)
            if btn_1:
                district_silencieux = district_silencieux[district_silencieux["Region"] == f"{region}"]
                st.dataframe(district_silencieux, use_container_width=True)
            else:
                st.dataframe(district_silencieux, use_container_width=True)