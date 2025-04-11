from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_url_list(url:str) -> list:
    '''
        Takes url string and returns the attribute
        provided
    '''
    data = requests.get(url+ "market/genres")
    soup = BeautifulSoup(data.text, features="html.parser")
    table_soup = soup.find("table")
    return [links['href'] for links in table_soup.find_all("a", href=True)]

genre_url = "https://www.the-numbers.com/"

def get_data_table(url_list:list, url:str):
    '''extracts rows and columns and places into CSV'''
    data_list = list()
    for i in url_list:
        data = requests.get(url+i)
        soup = BeautifulSoup(data.text, features="html.parser")
        tables_list = soup.find_all("table")[1]
        for headers in tables_list.find_all("th"):
            data_list.append(headers.text)
        df = pd.DataFrame(columns = data_list[:8])
        rows = tables_list.find_all("tr")
        file_path = 'C:\\Users\\flynnbe\\Desktop\\data\\'
        for data_in_rows in rows[1:]:
            length = len(df)
            individual_row_data = [d.text.strip() for d in data_in_rows.find_all("td")]
            df.loc[length] = individual_row_data
            df.to_csv(file_path + str(i.split("/")[-1]) + '.csv')
    return True

    
    
if __name__ == "__main__":
    get_data_table(get_url_list(genre_url), genre_url)
