## Top hospitality values mentioned in Accor Hotel reviews

*This project was completed as part of my cursus at Ironhack (a 9-week intensive coding bootcamp).*

The objective of this project was to understand **which hospitality values are the most sought-after** by the customers of **Accor Hotels premium brands**, from the scrapping of **online hotel reviews**.

#### PROJECT SCOPE

In total, **11,694 reviews** on **265 hotels** were scrapped from a well-known hotel review website.
- **Locations**: Top 10 French cities
	- Paris, Marseille, Lyon, Toulouse, Nice, Nantes, Strasbourg, Montpellier, Bordeaux, Lille
- **Brands**: Accor Hotels
	- *Premium brands*:  Raffles, Sofitel, Pullman, MGallery
	- *Intermediary brands*: Novotel, Mercure, Adagio, Mama Shelter
	- *Economic brands*: Ibis, hotelF1
- **Values**: Top 10 hospitality values, each one of them being characterized by a set of keywords (*keyword can be found in the* `data.py` *file of this repository, under the* `values_dict` *variable*)
	- Authenticity, Adventure, Community, Creativity, Cool, Fairness, Friendliness, Inner Harmony, Instantaneity, Love, Indulgement, Safety, Service, Status, Trustworthiness

#### METHODOLOGY

The scraping pipeline was composed of **three main steps**:

- **Step #1 - Acquisition: scrapping of hotel reviews** - *Output files:*
	- 10 *hotel_tables* (1 per city)
	- 10 *filtered_hotel_tables* (1 per city), removing non-Accor Hotels brands from the scraping output
	- 10 *review_tables* (1 per city)
- **Step #2 - Preparation of collected data** - *Output files:*
	- 1 *scrapped_table* for France (aggregation of the *filtered_hotel_tables* and *review_tables* of all cities, filtered on the selected range of Accor Hotel brands: *premium, intermediary or economic*)
	- 1 *study_table* (transformed *scrapped_table*, featuring a count of values occurrences)
- **Step #3 - Reporting** - *Output file*:
	- 1 *bar chart* summarizing the percentage of total reviews mentioning each one of the hospitality values

#### REPOSITORY STRUCTURE
 
 This repository is composed of **three types of Python files**:
 
 - *Project resources:*
	 - `libraries.py`
	 - `data.py` (on Top French cities, Accor Hotel brands and hospitality values)
 - *Executable pipelines:*
	 - `pipeline-acquisition.py`
	 - `pipeline-preparation-reporting.py`
 - *Functions used in executable pipelines:*
	 - `functions-acquisition.py`
	 - `functions-preparation-reporting.py`

A **directory containing pipeline outputs** was also added to this repository (scraping date: 2019.01.25). 
The `pipeline-outputs` directory contains:
- the **output tables of the acquisition step**
- the **output tables of the preparation step** and associated **bar charts**, on **two distinct study perimeters**: *premium* brands, and *intermediary* brands

#### HOW DID WE SPOT VALUES IN HOTEL REVIEWS?

This project was a great opportunity to get acquainted with ***Natural Language Processing*** (NLP) terminology and associated Python library, *nltk*.

To detect values occurrences in hotel reviews, **two parallel workflows were performed**:
- **On values keywords**: stem values keywords (i.e. extract the root of the words) with the *nltk* library
- **On hotel reviews**: original reviews were transformed in a three step process: 1. translate reviews from French to English with the *googletrans* library, as *nltk* achieves a better performance on English texts, 2. remove stop words and punctuation with the *nltk* library, and 3. stem transformed reviews with the *nltk* library.

As a final step, **the stemmed forms of values keywords and hotel reviews were matched to count values occurrences**.

#### RESULTS

- Regardless of the hotel range, ***friendliness*, *instantaneity* and *service*/*creativity*** are the Top 4 values that are the most sought-after by Accor Hotels customers.
- The ***service*** value seem to have **a greater importance for the customers of premium brands** than intermediary brands (appears respectively in 48% vs. 30% of hotel reviews).
- Quite logically, **intermediary customers** also seem to be **more attentive to *price fairness***, while **premium customers give a greater importance to *status***.

The two below charts show the **proportion of hotel reviews (in %) mentioning each one of the values**:

Analysis conducted on **949 reviews of *premium* Accor Hotels brands**:
![](https://github.com/gabrielleberanger/hotel-reviews-scrapping/blob/master/pipeline-outputs/prepartion-reporting-outputs-premium/bar-chart-top-10-values-premium.png)

Analysis conducted on **4,575 reviews of *intermediary* Accor Hotels brands**:
![](https://raw.githubusercontent.com/gabrielleberanger/hotel-reviews-scrapping/master/pipeline-outputs/preparation-reporting-outputs-intermediary/bar-chart-top-10-values-intermediary.png)