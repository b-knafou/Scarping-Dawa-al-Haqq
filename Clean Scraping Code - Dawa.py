#!/usr/bin/env python
# coding: utf-8

# In[2]:


#This code scrapes the links for all the issues of the magazine. These are links to individual issues. 


#Importing the necessary libraries
import requests
from bs4 import BeautifulSoup



url = requests.get("http://habous.gov.ma/daouat-alhaq/index.php?Itemid=120&option=com_blankcomponent&view=default")


soup = BeautifulSoup(url.content, 'lxml')

#This code finds the list of links for issues in the HTML
main_list = soup.find("div", {"id" : "k2ModuleBox112" })

maybe_links = main_list.find_all("li")


link_list = list()
   
        
base_link = "http://habous.gov.ma"

for element in maybe_links:
    proto_link = element.find("a")
    part_link = proto_link["href"]
    actual_link = base_link + part_link
    link_list.append(actual_link)
    
    

    
    


# In[10]:


#This bit of code scrapes the links of the individual articles from within the individual issues. 

base_url = "http://habous.gov.ma"

sub_links_list = list()


        
for link in link_list:
    url = requests.get(link)
    soup = BeautifulSoup(url.content, 'lxml')
    item_list = soup.find("div", {"class" : "itemList"})
    if item_list == None: 
        pass
    else:
        links = item_list.find_all("h3")
        for link in links:
            sub_link = link.find("a")
            actual_link = sub_link["href"]
            full_link = base_url + actual_link
            sub_links_list.append(full_link)
        
        

        

        


# In[24]:


#This code goes through the list of articles themselves and scrapes, the author, the title, the issue number, and the text. 

#The code works as intended except for the second to last article. That article is a poem and as such it takes a different,
#less readable form. For the final project I will be removing all poetry because poems are irrevelant to my 
#research question. 


#For the very last article (the last article of issue 2) no text was scraped. This was because, for whatever reason, 
#that aricle has no text. "http://habous.gov.ma/daouat-alhaq/item/20-%D8%AE%D8%B7%D8%A7%D8%A8-%D8%A3%D9%85%D9%8A%D8%B1%D9%8A"


master_list = list()

issue_list = list()







for article in sub_links_list:
    url = requests.get(article)
    #This is the new line
    soup = BeautifulSoup(url.content, 'lxml')
    title = soup.find("div", {"class" : "itemHeader"})
    test_list = list()
    test_list.append(article)
    if title == None:
        pass
    else:
        title_2 = title.find("h2")
        actual_title = (title_2.text)
        test_list.append(actual_title.strip())
    author = title.find("span")
    if author == None:
        pass
    else:
        actual_author = (author.text)
        test_list.append(actual_author.strip())
    issue = title.find("p")
    if issue == None:
        pass
    else:
        issue_number = issue.text
        test_list.append(issue_number)
        issue_list.append(issue_number)
        
    article = soup.find("div", {"class" : "itemBody"})
    text = article.find_all("p")
    whole_article = str()
    text_all_articles = list()

    
    for paragraph in text: 
        words = paragraph.text + " "
        whole_article += words

            
    test_list.append(whole_article)
    master_list.append(test_list)

  
    
    

#Saving to a CSV
import csv

with open("dawa_big_test.csv", mode = "w", encoding = "utf-8") as dawa_file:
    dawa_writer = csv.writer(dawa_file)
    
    dawa_writer.writerow(["link", "title", "author", "issue number", "text"])
    for item in master_list:
        dawa_writer.writerow(item)
    
dawa_file.close()

            

