# coding: utf-8

from libraries import *
from data import *
from functions-preparation-reporting import *

if __name__=='__main__':
    
    #Preparation
    scraped_table = create_scraped_table()
    selected_brands = ['Raffles','Sofitel','Pullman','MGallery']
    filtered_table = narrow_study_perimeter(scraped_table,selected_brands)
    study_table = create_study_table(filtered_table)
    
    #Reporting
    create_graph(study_table,selected_brands)
