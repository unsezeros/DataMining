#//region[rgba(241, 1, 15, 0.15)]
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import string
#//endregion
#//region[rgba(25, 255, 0, 0.1)]
#Fetch credentials to acess twitter
with open("credentials.txt", "r", newline="", encoding="utf-8") as file:
    credentials=file.readline()
    credentials=re.split(",",credentials)
    credentials_username=credentials[0]
    credentials_password=credentials[1]
# Set up Selenium webdriver
driver = webdriver.Chrome("/chromedriver_win32")  #Selenium Working...
# Open Twitter login page
driver.get("https://twitter.com/login")
time.sleep(2)
# Enter Twitter credentials
username = driver.find_element("xpath", '//input[@autocomplete="username"]')
username.send_keys(credentials_username)
username.send_keys(Keys.ENTER)
time.sleep(2)
password = driver.find_element("xpath", '//input[@autocomplete="current-password"]')
password.send_keys(credentials_password)
time.sleep(2)
password.send_keys(Keys.RETURN)
time.sleep(2)
# Search for the user's query
search_box = driver.find_element("xpath", '//input[@aria-label="Search query"]')
search_box.clear()
# search_box.send_keys(f'"inject disinfectant" "trump" OR "president" min_faves:1 since:2020-04-23_00:00:01_EST until:2020-04-30_11:59:01_EST -filter:replies') #23 to 30 (Week of the speech)
# search_box.send_keys(f'"inject disinfectant" "trump" OR "president" min_faves:1 since:2020-05-01_00:00:01_EST until:2020-05-8_11:59:01_EST -filter:replies') #Trying to week after
# search_box.send_keys(f'"inject disinfectant" "trump" OR "president" min_faves:1 since:2020-05-01_00:00:01_EST until:2020-05-31_11:59:01_EST -filter:replies') #Trying the month after
# search_box.send_keys(f'"inject disinfectant" min_faves:1 since:2020-04-15_00:00:01_EST until:2020-04-22_11:59:01_EST -filter:replies') #Week before
search_box.send_keys(Keys.RETURN)
time.sleep(2)
# Click on the "Latest" tab
latest_tab = driver.find_element("xpath", '//a[contains(@href, "f=live")]')
latest_tab.click()
time.sleep(2)
body = driver.find_element("tag name", "body")
#//endregion
#//region[rgba(255, 255, 0, 0.25)]
#Extract the tweets
tweets = []
fullsoup=""
for _ in range(70):
    #Wait, then capture the soup
    time.sleep(0.6)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    fullsoup = fullsoup+str(soup)
    
    # Scroll to load more tweets
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
#//endregion
#//region[rgba(210, 105, 320, 0.2)]
#Split tweets one by one 
print("Scrape completed, creating dataset...")
tweets = re.split("<article",fullsoup)
counter=1
tweets_csv=[]
csv_file = "tweets.csv"
#Write csv variable header
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    file.writelines(['TwitterName,TwitterTag,Timestamp,Tweet\n'])
for tweet in tweets:
    #Beautiful soup parser to extract elements
    soup = BeautifulSoup(tweets[counter], 'html.parser')
    #Subdivision of the full tweet into just the main part text (Still has trash)
    tweet_text = soup.get_text()
    #Final subdivision, only tweet text & metadata
    tweet_text2 = [text for text in soup.strings]
    tweet_text2 = ''.join(tweet_text2[5:])
    tweet_text3 = re.split(">", tweet_text)[1] 
    username = re.split("@", tweet_text3)[0]
    username = username.translate(str.maketrans('', '', string.punctuation))
    usertag = re.split("@", tweet_text3)[1]
    usertag = re.split("·", usertag)[0]
    try:
        timestamp = re.split('datetime="',tweets[counter])[1]
        timestamp = re.split("T",timestamp)[0]
    except Exception:
        #These will be all ads, redundant when in latest page
        timestamp="0000-00-00"
    #Clean tweettext (Purge punctuation, \n and rubbish text)
    try:
        tweet_text_final = tweet_text2.replace(".","")
    except Exception:
        pass
    try:
        tweet_text_final = tweet_text2.replace('"',"")
    except Exception:
        pass
    try:
        tweet_text_final = tweet_text2.replace(',',"")
    except Exception:
        pass
    if "Quote Tweetterno" in tweet_text_final:
        tweet_text_final = re.split("Quote Tweetterno", tweet_text_final)[0]
    elif "Search filters" in tweet_text_final:
        tweet_text_final = re.split("Search filters", tweet_text_final)[0]
    else:
        pass
    try:
        tweet_text_final = tweet_text_final.replace("\n"," ")
    except Exception:
        pass
    #Save the tweet into database
    tweets_csv.append(f"'{username}','{usertag}','{timestamp}','{tweet_text_final}'\n")
    counter+=1
    if counter == len(tweets)-1:
        break
#//endregion
#//region[rgba(52, 152, 300, 0.2)]
#Remove the repeated entries (As twitter only loads in chunks, BeautifulSoup can't get everything in one go, so I have to keep repeating the scrape)
new_list=[]
for _ in tweets_csv:
    if _ not in new_list:
        new_list.append(_)

# Write the tweets into the csv
with open(csv_file, "a", newline="", encoding="utf-8") as file:
    for data in new_list:
        file.writelines([data])

# Close the Selenium webdriver
driver.quit()
#//endregion