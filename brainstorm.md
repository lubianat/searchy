# TopicTagger: tag articles with semantic keywords via Wikidata

## Idea:

- OAuth1 login connection via Wikidata
- 
Given some input QID Wikidata identifier, TopicTagger will:

- Retrieve its abstract from Europe PMC and display to the user
- Serve a field to the user where they can add wikidata keywords via a selectize dropdown (similar to https://jvfe.github.io/wikidata_topictagger/)
- Write informations to Wikidata

## Technology

- Flask application. No need for sqlite database (although could be implemented as a plus)


## Goals

- Minimal: Given QID, gets abstract and link for tabernacle (where then user logs in and does editing)
- Basic: Given QID, gets abstract and user adds information via the interface, which renders the topics as a
series of quickstatements commands (where then user logs in and paste the commands for editing)
- Halfway: Users can login with the Wikimedia account and perform edits to the interface
- Complete: Something like the https://art.wikidata.link/browse 

## Similar apps:

- https://brazilianlaws.toolforge.org/home 
- https://art.wikidata.link/browse
- scholia.toolforge.org/ 
- https://jvfe.github.io/wikidata_topictagger/

## Game plan:

- Build skeleton of Flask App that gets information from the APIs
  - Follow https://flask.palletsprojects.com/en/2.0.x/quickstart/

- Figure out how to do an Wikidata search with selectize
  - Read source code and take notes on the the art depiction explorer and the other similar apps
  - Add selectize input both for articles and for topics
  - Code the logic to render quickstatements commands
- Set up login and logout via OAuth1 and Wikidata
  - Do the tutorial of https://wikitech.wikimedia.org/wiki/Help:Toolforge/My_first_Flask_OAuth_tool
- Implement advanced features for selecting articles
  - Articles that match a given topic and other filters


## Change of plans:

Tutorial leads to a bug + I realize this might be too much for the first tool.

Simpler idea: toolforge-hosted, Wikidata-based engine for biomedical articles. 

3 input fields: 

- Main Subject
- Gender 
- Region


Articles are, then, retrieved and displayed to the end user.

