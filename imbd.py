# create a python script to scrape the imdb website and 
# extract the movie details like name, rating, genre.
# import required modules
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import csv
# defining header variable
#headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
# method in request module to suppress warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# requesting the page (browse by genre of imdb page)
r=requests.get('https://www.imdb.com/feature/genre/?ref_=nv_ch_gr', verify=False)
# creating a bs4 object after parsing(html) the response from the request
soup = BeautifulSoup(r.text, "html.parser")
# getting the href links in a tag of images and making them into a list
link_text = [i.attrs.get('href') for i in soup.select('.image a')]
# defining a empty list to store the data of all movies
res = []
# iterating through the list of href links
for i in link_text:
    # requesting the page stored in the link_text list
    r = requests.get(i,verify=False)
    # creating the bs4 object after parsing(html) the response from the request
    soup_in = BeautifulSoup(r.text,"html.parser")
   # getting the list of movies in the website
    list_obj = soup_in.find_all('div', class_='lister-item')
    # iterating through the list of movies for getting required   information of 5 movies
    for j in range(5):
        # creating a empty list to store the data of a movie
        in_res = []
        # name of the movies
        name = list_obj[j].find('h3', class_='lister-item-header').getText().split('\n')[2]
        # rating of the movies, 0 if the movies is not released yet
        if(list_obj[j].find('div',class_='ratings-imdb-rating')):
            rating = list_obj[j].find('div',class_='ratings-imdb-rating').attrs.get('data-value')
        else:
            rating = 0
        # list of genres of the movie
        list_genres = list_obj[j].find('span', class_='genre').getText().split(',')
        genres = [k.strip() for k in list_genres]
       # appending the result to the list in_res
        in_res.append(name)
        in_res.append(float(rating))
        in_res.append(genres)
        # appending the in_res to the list res
        res.append(in_res)
        res.sort(key= lambda x:x[1], reverse=True)
# creating a csv file with timestamp in the filename to store the data
with open('ratings_by_genre_{}.csv'.format(str(time.strftime('%b-%d-%Y_%H%M', time.localtime()))),"w") as f:
        # creating a csv writer object
        csvwriter = csv.writer(f)
        # writing the heading of the column
        head = ['Movie Name', 'Rating', 'Genres']
        csvwriter.writerow(head)
        # writing the data into csv file
        csvwriter.writerows(res)
#Function for a menu 
def option_execute():
    print("------------------------------------------------------")
    print("Display menu\n1. List of Movie Names\n2. Movies by name\n3. Movies by Genres\n4. Movies by rating")
    option = int(input("Enter the option number: "))
    print("------------------------------------------------------")
    if option==1:
        l=[]
        for i in res:
            l.append(i[0])
        l=set(l)
        print("Movie Names List : \n",list(l))
    elif option == 2:
        name = input("Enter the name of the movie: ")
        for i in res:
            if name in i:
                print("Name: {}, Rating: {}, Genres: {}".format(name, i[1], ", ".join(i[2])))
                break
    elif option == 3:
        temp = []
        genre = input("Enter the genre: ")
        for i in res:
            if genre in [j.lower() for j in i[2]]:
                if i not in temp:
                    temp.append(i)
        for i in temp:
            print("Name: {}, Rating: {}, Genres: {}".format(i[0], i[1], ", ".join(i[2])))
    elif option == 4:
        temp1 = []
        rate = float(input("Enter the rating: "))
        for i in res:
            if rate in i:
                if i not in temp1:
                    temp1.append(i)
        for i in temp1:
            print("Name: {}, Rating: {}, Genres: {}".format(i[0], i[1], ", ".join(i[2])))
    print("Want to search again?\nIf yes, type 'yes' to search again or 'no' to exit...")
    yes_no = input()
    if yes_no == 'yes':
        option_execute()
    else:
        print("Bye Bye!!Exiting...!")
#Function Call
option_execute()
