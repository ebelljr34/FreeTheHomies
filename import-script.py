from app import db, DBTable

from bs4 import BeautifulSoup
import requests
import csv    

def free_tha_homies():
    url = "https://www.sentencingproject.org/publications/color-of-justice-racial-and-ethnic-disparity-in-state-prisons/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    incarceration_data = []
    first_table = soup.find('table')
    rows = first_table.findAll('tr')
    
    for row in soup.select('tr')[1:]:
        try:
            states = list(row.select('td')[0].strings)
            state = states[0]
           
            
            white = list(row.select('td')[1].strings)[0]
            states.append(white)
            
            black = list(row.select('td')[2].strings)[0]
            states.append(black)
            
            black_white_differential = (int(black)/int(white))
            rounded = str(round(black_white_differential, 2))
            states.append(rounded)
            print(states)

            data = [state,white,black,rounded]
            incarceration_data.append(data)
            
            #black_white_differential = black / white
            #print (black_white_differential)
        except IndexError:
            break

    return incarceration_data


# set up your scraping below



# this `main` function should run your scraping when 
# this script is ran.
def main():
    incarceration_data = free_tha_homies()
    db.drop_all()
    db.create_all()
    for data in incarceration_data: 
        new_row = DBTable(states = data[0], white = data[1], black = data[2], rounded = data[3])
        print(new_row)
        db.session.add(new_row)
        db.session.commit()

if __name__ == '__main__':
    main()