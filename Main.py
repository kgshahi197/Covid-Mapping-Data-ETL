import requests
import json
from unidecode import unidecode
from textblob import TextBlob
import nltk
import pickledb

nltk.download('brown')
nltk.download('punkt')
reddit = praw.Reddit(client_id = 'ICy11BzMfMvZDQ', 
                     client_secret = '1YNi5EzkghO5MIrTkuMjYhtUaXk',
                     user_agent = 'Covid Case Maps')
# Do stuff with the reddit instance!

my_app_name = "CovidCaseMaps"
#creating an app name

def covid_posts(subreddit): #declaring a function 
    """returns useful data about Reddit posts from a given subreddit.
    (Define more details later)   
    """
    #Docstring
   
    #Get the full reddit listings object
    url = f'https://www.reddit.com/r/{subreddit}.json'
    head = {'user-agent': my_app_name} #creating a dictionary with key
    redditdata = requests.get(url, headers=head).json() 

    #Return just the items of interest
    listings = redditdata['data']['children']
    returndata = [] #needed to put all the items in a list
    for item in listings: #creating nested objects with an empty dictionary
        thisitem = dict()
        thisitem['itemdomain'] = item['data']['domain']
        thisitem['title'] = unidecode(item['data']['title']).replace(","," ").replace("\n", " ")
        thisitem['ups'] = int (item['data']['ups'])
        returndata.append(thisitem)
    return(returndata)


def analyze_cases(sourcefile, floor=0):
  with open(sourcefile, 'r') as file:
    print("Reading file...\n")
    input = file.read().replace('\n', '').replace('.', ' ').replace(',', ' ')
    blob = TextBlob(input)
    output = blob.noun_phrases
    returndata = []
    for term in set(output):
      termcount = output.count(term)
      if termcount > floor:
        returndata.append((term, termcount))
      else:
        pass
    return returndata


returndata = covid_posts("CovidMapping")
with open('COVIDcases.csv', 'w') as myfile: 
  for post in returndata:
    if post ['ups'] > 5:
      line = (f"{post['itemdomain']},{post['ups']},{post['title']}\n") 
      myfile.write(line)
    else:
      pass

      
data = analyze_cases('COVIDcases.csv')
with open('exportdata.csv', 'w') as output:
  for pair in data:
    output.write(f'{pair[0]},{pair[1]}\n')