# coding: utf-8

def get_next_city_url(url):
    
    """Function taking as a parameter a city URL, and returning the URL of the next page (still for the same city):
    - Input: https://www.***.fr/Hotels-g187147-oa30-Paris_Ile_de_France-Hotels.html
    - Output: https://www.***.fr/Hotels-g187147-oa60-Paris_Ile_de_France-Hotels.html"""
    
    i = int(int(re.findall(r'-oa(\d*)-',url)[0])/30)
    next_url = '-'.join(url.split('-',3)[:2])+f'-oa{30*(i+1)}-'+'-'.join(url.split('-',3)[3:])
    return next_url

def get_next_hotel_url(url):
    
    """Function taking as a parameter a hotel URL, and returning the URL of the next page (still for the same hotel):
    - Input: https://www.***.fr/Hotel_Review-g187075-d197335-Reviews-or5-Mercure_Strasbourg_Palais_des_Congres-Strasbourg_Bas_Rhin_Grand_Est.html
    - Output: https://www.***.fr/Hotel_Review-g187075-d197335-Reviews-or10-Mercure_Strasbourg_Palais_des_Congres-Strasbourg_Bas_Rhin_Grand_Est.html"""
        
    if bool(re.search(r'-or(\d*)-',url)):
        i = int(int(re.findall(r'-or(\d*)-',url)[0])/5)
        next_url = '-'.join(url.split('-',5)[:4])+f'-or{5*(i+1)}-'+'-'.join(url.split('-',5)[5:])
    else:   
        next_url = '-'.join(url.split('-',4)[:4])+'-or5-'+'-'.join(url.split('-',4)[4:])
    return next_url

def create_output_folders():
    
    """Function creating the folders in which scrapping outputs will be stored."""
    
    subfolder_names = ['hotel_tables','filtered-hotel-tables','review-tables']
    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join('scraping-outputs', subfolder_name))

def create_hotel_table(city,city_url):
    
    """Function returning (and saving) a city hotel_table, with the following columns:
    - city
    - hotel_name
    - hotel_rating
    - hotel_reviews
    - hotel_url"""
    
    print(f'***GENERATING HOTEL TABLE FOR {city}***')

    #Create empty hotel_table
    hotel_table = pd.DataFrame()

    #Scrap first city page to extract the city and maximum number of pages
    city_soup = bs(requests.get(city_url).content,'lxml')
    city_max_pages = int(city_soup.select('div.pageNumbers a:last-of-type')[0].text)
    
    #Scrap each city page to enrich to hotel_table
    for i in range(min(10,city_max_pages)):

        print(f'{city} - Scrapping page {i+1}/{min(10,city_max_pages)}...')

        #If city page number = 1, content has already been extracted
        if i==0:
            pass

        #If city page number > 1, content should be extracted
        else:
            city_soup = bs(requests.get(city_url).content,'lxml')

        #Extract hotel information
        hotel_url_list = ['https://www.***.fr'+i['href'] for i in city_soup.select('a.property_title')]
        hotel_name_list = [i.text for i in city_soup.select('a.property_title')]
        hotel_reviews_list = [int(re.sub(r'\xa0','',i.text).strip('avis')) for i in city_soup.select('a[class*=review_count]')]
        hotel_rating_list = [int(i['class'][1].strip('bubble_'))/10 for i in city_soup.select('div>a[class*=ui_bubble_rating]')]

        #Enrich hotel_table
        temp_table = pd.DataFrame()

        temp_table['hotel_url'] = hotel_url_list
        temp_table['hotel_name'] = hotel_name_list
        temp_table['hotel_reviews'] = hotel_reviews_list
        temp_table['hotel_rating'] = 0
        temp_table.loc[temp_table.hotel_reviews!=0,'hotel_rating'] = hotel_rating_list
        temp_table['city'] = city

        hotel_table = pd.concat([hotel_table,temp_table],ignore_index=True)

        #Set up a protection against bot detection
        time.sleep(3)

        #Get next city page URL (still for the same city)
        city_url = get_next_city_url(city_url)
    
    #Save final hotel_table
    hotel_table = hotel_table[['city','hotel_name','hotel_rating','hotel_reviews','hotel_url']].drop_duplicates()
    hotel_table.to_csv(f'scraping-outputs/hotel-tables/hotel_table_{city}.csv',sep=';',index=False)
    
    return hotel_table
        
def filter_hotel_table(city,hotel_table,brands=accor_brands):
    
    """Function filtering (and saving) a city hotel_table
    keeping Accor brands only, having at least 1 review."""
    
    filtered_hotel_table = pd.concat(\
        [hotel_table.loc[hotel_table.hotel_name.str.lower().str.contains(brand.lower())
        &(hotel_table.hotel_reviews>10)] for brand in accor_brands],ignore_index=True)
    
    filtered_hotel_table.to_csv(f'scraping-outputs/fitered-hotel-tables/filtered_hotel_table_{city}.csv',sep=';',index=False)

    return filtered_hotel_table

def create_review_table(city,hotel_table):
    
    """Function returning (and saving) a city reviews_table, with the following columns:
    - city
    - hotel_name
    - ind_rating
    - review_txt"""

    print(f'***GENERATING REVIEW TABLE FOR {city}***')

    #Create empty reviews_table
    review_table = pd.DataFrame()

    #Loop over hotel URLs
    for hotel_url in list(hotel_table.hotel_url.values):
    
        #Scrap first hotel page to extract the city, hotel name and maximum number of pages
        hotel_soup = bs(requests.get(hotel_url).content,'lxml')
        hotel_name = hotel_table.loc[hotel_table.hotel_url==hotel_url,'hotel_name'].values[0]
        hotel_max_pages = int(hotel_soup.select('div.pageNumbers a:last-of-type')[0].text)
    
        #Scrap each hotel page to enrich to reviews_table
        for i in range(min(10,hotel_max_pages)):
    
            print(f'{hotel_name} - Scrapping page {i+1}/{min(10,hotel_max_pages)}...')
        
            #If hotel page number = 1, content has already been extracted
            if i==0:
                pass
        
            #If hotel page number > 1, content should be extracted
            else:
                hotel_soup = bs(requests.get(hotel_url).content,'lxml')
    
            #Extract reviews information
            review_txt_list = [i.text for i in hotel_soup.select('q[class*=reviewText]')]
            ind_rating_list = [int(i['class'][1].strip('bubble_'))/10 for i in hotel_soup.select('div[class*=RatingLine]>span[class*=ui_bubble_rating]')]

            #Enrich reviews_table
            temp_table = pd.DataFrame()

            temp_table['ind_rating'] = ind_rating_list
            temp_table['review_txt'] = review_txt_list
            temp_table['city'] = city
            temp_table['hotel_name'] = hotel_name

            review_table = pd.concat([review_table,temp_table],ignore_index=True)

            #Set up a protection against bot detection
            time.sleep(3)

            #Get next hotel page URL (still for the same hotel)
            hotel_url = get_next_hotel_url(hotel_url)

    #Save final reviews_table
    review_table = review_table[['city','hotel_name','ind_rating','review_txt']].drop_duplicates()
    review_table.to_csv(f'scraping-outputs/review-tables/review_table_{city}.csv',sep=';',index=False)
    
    return review_table

def scrap_data(cities_dict):
    
    """Function creating (and saving) an hotel_table and a review_table per city."""
    
    for city, city_url in cities_dict.items():
        hotel_table = create_hotel_table(city,city_url)
        filtered_hotel_table = filter_hotel_table(city,hotel_table)
        review_table = create_review_table(city,filtered_hotel_table)
