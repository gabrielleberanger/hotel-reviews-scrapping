# coding: utf-8

cities_dict = {
    'Paris':'https://www.***.fr/Hotels-g187147-oa0-Paris_Ile_de_France-Hotels.html',
    'Marseille':'https://www.***.fr/Hotels-g187253-oa0-Marseille_Bouches_du_Rhone_Provence_Alpes_Cote_d_Azur-Hotels.html',
    'Lyon':'https://www.***.fr/Hotels-g187265-oa0-Lyon_Rhone_Auvergne_Rhone_Alpes-Hotels.html',
    'Toulouse':'https://www.***.fr/Hotels-g187175-oa0-Toulouse_Haute_Garonne_Occitanie-Hotels.html',
    'Nice':'https://www.***.fr/Hotels-g187234-oa0-Nice_French_Riviera_Cote_d_Azur_Provence_Alpes_Cote_d_Azur-Hotels.html',
    'Nantes':'https://www.***.fr/Hotels-g187198-oa0-Nantes_Loire_Atlantique_Pays_de_la_Loire-Hotels.html',
    'Strasbourg':'https://www.***.fr/Hotels-g187075-oa0-Strasbourg_Bas_Rhin_Grand_Est-Hotels.html',
    'Montpellier':'https://www.***.fr/Hotels-g187153-oa0-Montpellier_Herault_Occitanie-Hotels.html',
    'Bordeaux':'https://www.***.fr/Hotels-g187079-oa0-Bordeaux_Gironde_Nouvelle_Aquitaine-Hotels.html',
    'Lille':'https://www.***.fr/Hotels-g187178-oa0-Lille_Nord_Hauts_de_France-Hotels.html'}

accor_brands = [
    'Raffles','Sofitel','Pullman','MGallery',
    'Novotel','Mercure','Adagio','Mama Shelter',
    'Ibis','hotelF1']

values_dict = {
    'Authenticity': ['genuine','authentic','original','homemade','diy','craft','typical'],
    'Adventure': ['exotic','explore','thrill'],
    'Community': ['neighbor','community','local','regional'],
    'Creativity': ['art','creativity','decoration','paintings','design','ornament','accessories','furniture'],
    'Cool': ['cool','fun','trendy','hip','hype','laidback','chill'],
    'Fairness': ['cheap', 'expensive', 'price', 'steal', 'reasonable', 'bargain', 'competitive', 'economical'],
    'Friendliness': ['affable','affectionate','amiable','amicable','attentive','cordial','familiar','receptive','kind','smile','welcome','hospitable','hospitality','thoughtful','considerate','smile','hearty','friendly'],
    'Inner Harmony': ['spirituality','faith','meditate','calm','stress','harmony','detox'],
    'Instantaneity': ['speed','quick','fast','immediate','snappy','prompt','swift','rapid','slow','late'],
    'Love': ['romantic','wife','wedding','fiance','honeymoon','glamor','glamour'],
    'Indulgement': ['treat','comfort','cosy','bubble','relax','delicious','yummy','pleasure'],
    'Safety': ['safe','secure','protect','guard','danger','unsafe'],
    'Service': ['service','competency','professional','helpful','knowledge','respect','assist','personalised'],
    'Status': ['leader','loyal','gold','silver','platinum','valued','rewarded','reward','superior','upgrade','success','luxury'],
    'Trustworthiness': ['trust','honest','dishonest','trustful','transparent','responsibility']}

values_dict_stemmed = {}
for key,value in values_dict.items():
    values_dict_stemmed[key] = [PorterStemmer().stem(i) for i in value]
