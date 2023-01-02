import requests
import bs4
import re
import csv
import pandas as pd


final = []
reviews= []
name = []
heading = []

website = input("Provide the full link of the product page:")

result = requests.get(website)

soup = bs4.BeautifulSoup(result.text,"html.parser")

for div in soup.find_all("div", {'class':'row'}): 
    div.decompose()


title = soup.find('span',class_="B_NuCI").text

title = title.replace(' ','_')
title = title.replace('/','-')
title = title.split()[0] + '.csv'
print(title)


link =  soup.find('a',attrs={'href':re.compile("/product-reviews/")})
   
link_text = link.get('href')

base_url = "https://www.flipkart.com" + link_text + "&page={}"

result = requests.get(base_url.format(1))

soup = bs4.BeautifulSoup(result.text,"html.parser")



page = soup.find('div',class_='_2MImiq _1Qnn1K')


x = page.span.text

     
end_page = int(x[10:])
end_page+=1


for i in range(1,end_page):
    
    
    scrape_url = base_url.format(i)
    result = requests.get(scrape_url)
    soup = bs4.BeautifulSoup(result.text,"html.parser")

    for x in soup.find_all('p',class_="_2-N8zT"):
        heading.append(x.text)
    
    for x in soup.find_all('p',class_="_2sc7ZR _2V5EHH"):
        name.append(x.text)
    
    for x in soup.find_all('div',class_="t-ZTKy"):
        reviews.append(x.text[0:-9])

final.append(name)
final.append(heading)
final.append(reviews)

df = pd.DataFrame(final)
df = df.T
df.to_csv( title , index=False, header=False)