import os
from bs4 import BeautifulSoup as bs 
import requests
import time
import sys
# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the Python path
sys.path.append(parent_dir)
from constants import LOC, BUILDINFO
         
years = ['2017','2018','2019' ,'2020', '2021', '2022', '2023']  # Add more years if needed
months = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30,
          '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}

count=0

for year in years:
    for month in months.keys():
        for day in range(1, months[month] + 1):
            if count>2:
                break
            count+=1
            day_str = str(day).zfill(2)  # Add leading zero for single-digit days
            directory_path = os.path.join(LOC, str(year), str(month), day_str)
            os.makedirs(directory_path, exist_ok=True)
            os.chdir(directory_path)
            time.sleep(5)
            
            url = f'{BUILDINFO}/{year}/{month}/{day_str}'
            
            page = requests.get(url)

            soup = bs(page.content,"html.parser")

            anchors = soup.find_all('a') 

            all_links = []
            for link in anchors:
                linkText = link.get('href') #find the html reference text mentioned between the anchor tags 
                all_links.append(linkText)

            all_links = [k for k in all_links if '.buildinfo' in k]  
            
            for j in all_links:
                web = url + j
                page = requests.get(web)
                data = bs(page.content,"html.parser")
                data = str(data)
                
                if ('\n\n') in data:
                    data = data.split('\n\n')[1]
                else:
                    data = data

                if '-----BEGIN PGP SIGNATURE-----' in data:
                    data = data.replace('-----BEGIN PGP SIGNATURE-----','')
                else:
                    data = data
                                
                with open (j, 'w') as g:
                    g.write(data)

