# Searchy

Searchy is a flask app to for metascience-aware semantic searches on Wikidata.
A live version of the tool is hosted at <https://searchy.toolforge.org>.
It is currently a prototype in beta version written as a final project for CS50.

#### Video Demo: https://youtu.be/ahYwxNtO4GI
  
#### Description:

If you want to search the web for scientific articles, it is rather easy: there is [PubMed](https://pubmed.ncbi.nlm.nih.gov/), and [Europe PMC](https://europepmc.org/), [Google Scholar](https://scholar.google.com/), [Semantic Scholar](https://www.semanticscholar.org) and so on. However, what if you want to find articles written by women? Or articles from a latin american country? 

Searchy becomes metascience-aware by using [Wikidata](https://www.wikidata.org), a sister project of Wikipedia which is building a collaborative graph of the sum of human knowledge. Wikidata includes information about researchers and their works, and so is apt to power search engines that consider metascientific information. It presents that information through a number of public APIs.
  
    
#### Technology

The project uses a simple [Flask](https://flask.palletsprojects.com/en/1.1.x/) backend to handle the logic for user requests. 

The user selects a topic from an autocomplete input box, either from the home page or from the search page.

By clicking on the link, the user is redirected to a dashboard containing all articles that are tagged in Wikidata with that key concept. Note that the ID of the concept is part of the URL, so queries can be shared with ease. 

  ![image](https://user-images.githubusercontent.com/7917951/121785215-d8eae780-cb8e-11eb-9551-2f6c2d6a3730.png)


Once you have your query, it is possible to filter it using information Wiikidata has on the authors of those articles. Two filters are implemented in the current version of Searchy: filter by gender and filter by region. Both options are automatically retrieved from Wikidata, and will be flexible when new genders and regions are created in the database. 

  ![image](https://user-images.githubusercontent.com/7917951/121785241-08015900-cb8f-11eb-93c4-d3f0de6eedcd.png)

The visualization of the results is done via a series of embedded SPARQL queries. SPARQL is similar to SQL, but operates on graph databases, like Wikidata. The queries are organized in a python module I currently maintain, wbib, and embedded from the Wikidata Query Service directly on Searchy. 


This final project will be continuously improved, and user feedback will be accounted for on its GitHub page. It is also part of a larger effort to connect Wikidata with the research community, which includes projects like [WikiCite](http://wikicite.org/) and [Scholia](https://scholia.toolforge.org/). 

#### About
  
  You can read more about Searchy on the [tool's about page](https://searchy.toolforge.org/about). 
