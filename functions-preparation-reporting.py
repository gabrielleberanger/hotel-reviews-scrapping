# coding: utf-8

def create_scraped_table():
    
    """Function concatenating previously saved hotel_tables and review_tables into a final_table."""

    #Extract saved hotel_tables and review_tables, and concatenate them into 2 unique tables
    hotel_tables_list = [pd.read_csv(f'scraping-outputs/fitered-hotel-tables/filtered_hotel_table_{city}.csv',sep=';') for city in cities_dict]
    review_tables_list = [pd.read_csv(f'scraping-outputs/review-tables/review_table_{city}.csv',sep=';') for city in cities_dict]
    
    hotel_table = pd.concat(hotel_tables_list,ignore_index=True).drop(['hotel_url','Unnamed: 0'],axis=1)
    review_table = pd.concat(review_tables_list,ignore_index=True).drop(['city','Unnamed: 0'],axis=1)
    
    #Join tables to create the final_table
    scraped_table = hotel_table.join(review_table.set_index('hotel_name'),on='hotel_name').reset_index(drop=True)

    #Add an hotel_brand column
    for brand in accor_brands:
        scraped_table.loc[scraped_table.hotel_name.str.lower().str.contains(brand.lower()),'hotel_brand']=brand
    scraped_table = scraped_table[['city','hotel_brand','hotel_name','hotel_rating','hotel_reviews','ind_rating','review_txt']]
    
    #Save final_table
    scraped_table.to_csv('scraped_table.csv',sep=';',index=False)
    
    return scraped_table

def narrow_study_perimeter(scraped_table,selected_brands):
    
    """Function filtering the final_table on a list of selected brands."""
    
    filtered_table = scraped_table.loc[scraped_table.hotel_brand.isin(selected_brands)].reset_index(drop=True)
    
    return filtered_table

def strip_emoji(text):
    
    """Function stripping emoji from a string."""
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00010000-\U0010FFFF"  # emoticons
                           "]+", flags=re.UNICODE)

    stripped_text = emoji_pattern.sub(r'', text)
    stripped_text = re.sub(r'\xa0',' ',stripped_text)
    
    return stripped_text

def translate_review(text):
    
    """Function translating a text into English."""
    translated_text = Translator().translate(text).text
    time.sleep(2)
    
    #translated_text = TextBlob(text).translate(to='en')
    #time.sleep(2)
    
    return translated_text

def standardize_review(text):
    
    """Function returning a text on which:
    - Stopwords and punctuation have been removed
    - Words have been stemmed to their root"""
    
    stop = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    #Remove stopwords and punctuation
    words = [i for i in words if (i not in stop)&(i not in string.punctuation)]
    #Stem words
    words = [PorterStemmer().stem(word) for word in words]
    
    return ' '.join(words)

def create_study_table(filtered_table):
    
    """Function returning (and saving) a study_table, with the following columns:
    - city
    - hotel_brand
    - 1 column per value (boolean)"""
    
    #Apply the translate_review and standardize_review to the review_txt column
    for i in range(filtered_table.shape[0]):
        filtered_table.review_txt[i] = standardize_review(translate_review(strip_emoji(filtered_table.review_txt[i])))
        print(f'{i}/{filtered_table.shape[0]}')
    
    #Create boolean columns for each value
    for key, values in values_dict_stemmed.items():
        for value in values:
            filtered_table.loc[filtered_table.review_txt.str.contains(value)==True,key] = 1
            filtered_table[key].fillna(0,inplace=True)
        filtered_table[key] = filtered_table[key].astype(int)
    
    #Drop irrelevant columns, and save study_table
    study_table = filtered_table.drop(['hotel_name','hotel_rating','hotel_reviews','ind_rating','review_txt'],axis=1)
    study_table.to_csv('study_table.csv',sep=';',index=False)
    
    return study_table

def create_graph(study_table,selected_brands):
    
    """Function saving an histogram:
    - x: values
    - y: percentage of reviews mentioning the value"""
    
    results = study_table.iloc[:,3:].sum().sort_values(ascending=False)
    results_per = round(results/study_table.shape[0]*100,2)

    values_name = list(results_per.index)
    values_per = list(results_per.values)
    
    title = f'Top 10 values (brands: {", ".join(selected_brands)})'
    fig, ax = plt.subplots(figsize=(15,8))
    ax.bar(values_name,values_per)
    ax.set_xticklabels(values_name,rotation=45)
    plt.title(title,fontsize=16)

    fig.savefig(f'bar-chart-top-10-values.png')
