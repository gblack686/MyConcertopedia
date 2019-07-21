from imagesoup import ImageSoup 
import requests
import datetime
import os
import sqlite3 as sql
import base64
import pandas as pd


soup = ImageSoup()

date = datetime.datetime.today()
todays_date = datetime.datetime.now().strftime("%d.%m.%y")
imgblobs = []

image_preferences = '''
    image_size: string, tuple(width, height)
    Find images in any size you need.
    (width, height)
    icon
    medium
    large
    400x300+
    640x480+
    800x600+
    1024x768+
    2mp+
    4mp+
    8mp+
    10mp+
    12mp+
    15mp+
    20mp+
    40mp+
    70mp+
    aspect_ratio: string
    Specify the shape of images.
    tall
    square
    wide
    panoramic
    '''  


try: 
    os.makedirs("concertopedia_links_"+todays_date)
except:
    print("Folder already created.")
    

folder = "concertopedia_links_"+str(todays_date)

search_term = input('Image Search Keywords:')
parameters = input('Do you want to specify parameters? (Y/N)')
# image_size = '640x480+'

if parameters != 'Y':
    image_size='640x480+'
    aspect_ratio='square'
    n_images=4
    try:
        images = soup.search(search_term, image_size=image_size, aspect_ratio=aspect_ratio, n_images=n_images)
        links = [y.URL for y in images]
        counter = 0
        df = {'url':links,'search_term':search_term, 'image_size':image_size, 'image_size':image_size, 'aspect_ratio':aspect_ratio}
    except:
        print("SEARCH ERROR")

    try:
        for y in links:
            r = requests.get(y, allow_redirects=True)
            counter += 1
            filename = folder+'\\'+str(search_term)+'_'+str(counter)+'.jpeg'
            open(filename, 'wb').write(r.content)
            with open(filename, "rb") as imageFile:
                imgblob = base64.b64encode(imageFile.read())
            imgblobs.append(imgblob)
    except:
        print("DOWNLOAD ERROR")

else:
    print(image_preferences)
    image_size = input('Input Image Size Preferences (See Above):')
    aspect_ratio = input('Input Aspect Ratio (See Above):')
    n_images = max(10,int(input('Input Desired Image Quantity (Max 10):')))
    
    try:
        images = soup.search(search_term, image_size=image_size, aspect_ratio=aspect_ratio, n_images=n_images)
        links = [y.URL for y in images]
        counter = 0
        df = {'url':links,'search_term':search_term, 'image_size':image_size, 'image_size':image_size, 'aspect_ratio':aspect_ratio}
    except:
        print("SEARCH ERROR")

    try:
        for y in links:
            r = requests.get(y, allow_redirects=True)
            counter += 1
            filename = folder+'\\'+str(search_term)+'_'+str(counter)+'.jpeg'
            open(filename, 'wb').write(r.content)
            with open(filename, "rb") as imageFile:
                imgblob = base64.b64encode(imageFile.read())
                imgblobs.append(imgblob)
    except:
        print("DOWNLOAD ERROR")  

try:
    con = sql.connect('concertopedia.db')
except:
    print('Database connection error')

data = {'url':links,'search_term':search_term, 'image_size':image_size, 'aspect_ratio':aspect_ratio, 'date':date, 'image_blob':imgblobs}
df = pd.DataFrame(data)
df.to_sql('image_scrapes', con=con, if_exists='append', index=False)


# EXTRACT IMAGES FROM BLOB
# http://numericalexpert.com/blog/sqlite_blob_time/
