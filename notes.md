# Intro

Notes on the source code of several example programs that might serve as basis for TopicTagger.

# JVFE`s TopicTagger

https://jvfe.github.io/wikidata_topictagger/

- Uses vue.js (maybe I should read a bit of Vue`s documentation)
- Uses vuetify too : https://vuetifyjs.com/en/getting-started/installation/


Vuetify seems a bit more complicated to use than just vue. I'll have to study that too (instead of trying to rush).
For the moment, I'll try to make the TopicTagger without vue, vuetify and additional complications.


# Art Depiction Explorer

https://art.wikidata.link/browse

Adds item label to page title: 

```html
  <title>
    Domine, Quo Vadis? (Q18599406)
  </title>
```

Picture goes on the left, content + editing box goes on the right
```html
<div class="container-fluid mt-2">
  <div class="row">
    <div class="col-md">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Domine%2C_quo_vadis%3F_%28Marco_Benefial%29_-_Nationalmuseum_-_17336.tif/lossy-page1-800px-Domine%2C_quo_vadis%3F_%28Marco_Benefial%29_-_Nationalmuseum_-_17336.tif.jpg" class="w-100" />
    </div>
      <div class="col-md">
      <!-- content from Wikidata -->
      <!-- depicts statements-->
      <!-- input form -->
    </div>
</div>
</div>
```

It seems like it uses vue.js

```html

<div id="app" class="mt-2">
        <div v-if="existing_depicts.length">
          <div>this artwork has {{ existing_depicts.length }} existing depicts statement</div>
        </div>

        <div class="mb-2" v-for="(hit, index) in existing_depicts">
          <div>
            <a :href="'https://www.wikidata.org/wiki/' + hit.qid">{{ hit.label }}</a>
            ({{ hit.qid }})
            &nbsp;
            <span v-if="hit.description" class="description">{{ hit.description }}</span>
            &mdash; {{ hit.count }} artworks
          </div>
        </div>

        <h3>what can you see in this artwork?</h3>
                <div v-if="people.length">
          <div>These people were born and died in the same years as appears in the title of the artwork.</div>
          <div v-for="person in people">
            <a href="#" @click.prevent="add_person(person)">{{ person.label || '[name missing]' }}</a>,
            {{ person.year_of_birth }}-{{ person.year_of_death}} ({{ person.qid }})
            <span v-if="person.description" class="description">{{ person.description }}</span>
            <a :href="'https://www.wikidata.org/wiki/' + person.qid">[wikidata]</a>
          </div>
        </div>

        <div v-if="new_depicts.length">
          <div>{{ new_depicts.length }} new items to add to artwork depicts statement</div>
        </div>

        <div v-for="(hit, index) in new_depicts">
          <input type="hidden" name="depicts" :value="hit.qid">
          <div>
            {{ hit.label }}
            <span v-if="hit.alt_label">({{ hit.alt_label }})</span>
            <a href="#" @click.prevent="remove(index)" >remove</a>
            &mdash; {{ hit.count }} existing artworks
            ({{ hit.qid }})
            <a :href="'https://www.wikidata.org/wiki/' + hit.qid">[wikidata]</a>
          </div>
          <div v-if="hit.description">
            <div class="description">{{ hit.description }}</div>
          </div>
        </div>

```

## Brazilian laws source code

https://github.com/WikiMovimentoBrasil/brazilianlaws

- Check how OAuth1 is implemented
- Check how it sends requests to the Wikidata API

### OAuth1

app.py:

```python
from flask import Flask, render_template, request, redirect, session, jsonify, g
from oauth_wikidata import get_username, get_token, post_request
from requests_oauthlib import OAuth1Session

__dir__ = os.path.dirname(__file__)
app = Flask(__name__)
app.config.update(yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))


@app.before_request
def init_profile():
    g.profiling = []


@app.before_request
def global_user():
    g.user = get_username()


@app.route('/login')
def login():
    next_page = request.args.get('next')
    if next_page:
        session['after_login'] = next_page

    client_key = app.config['CONSUMER_KEY'] 
    client_secret = app.config['CONSUMER_SECRET'] 
    base_url = 'https://www.wikidata.org/w/index.php'
    request_token_url = base_url + '?title=Special%3aOAuth%2finitiate'

    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          callback_uri='oob')
    fetch_response = oauth.fetch_request_token(request_token_url)

    session['owner_key'] = fetch_response.get('oauth_token')
    session['owner_secret'] = fetch_response.get('oauth_token_secret')

    base_authorization_url = 'https://www.wikidata.org/wiki/Special:OAuth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url,
                                                oauth_consumer_key=client_key, uselang=get_locale())
    return redirect(authorization_url)


@app.route("/oauth-callback", methods=["GET"])
def oauth_callback():
    base_url = 'https://www.wikidata.org/w/index.php'
    client_key = app.config['CONSUMER_KEY']
    client_secret = app.config['CONSUMER_SECRET']

    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=session['owner_key'],
                          resource_owner_secret=session['owner_secret'])

    oauth_response = oauth.parse_authorization_response(request.url)
    verifier = oauth_response.get('oauth_verifier')
    access_token_url = base_url + '?title=Special%3aOAuth%2ftoken'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=session['owner_key'],
                          resource_owner_secret=session['owner_secret'],
                          verifier=verifier)

    oauth_tokens = oauth.fetch_access_token(access_token_url)
    session['owner_key'] = oauth_tokens.get('oauth_token')
    session['owner_secret'] = oauth_tokens.get('oauth_token_secret')
    next_page = session.get('after_login')

    return redirect(next_page)


```

```html
<nav class="topnav" id="topnavbar">
    <a tabindex="0" id="home" href="{{url_for('home')}}" class="active" style="color:#029c36">{{_("Homepage")}}</a>
    <a tabindex="0" id="reconciliate" href="{{url_for('reconciliate')}}">{{_("Other tasks")}}</a>
{#    <a tabindex="0" id="tutorial" href="{{url_for('tutorial')}}">{{_("Ajuda")}}</a>#}
    {% if lang != 'en' %}
        <a class="right" tabindex="0" href="{{url_for('set_locale', return_to=request.script_root + request.full_path, lang='en')}}">EN</a>
    {% endif %}
    {% if lang != 'pt' and lang != 'pt-br' and lang != 'pt_BR' and lang != 'pt-BR' %}
        <a class="right" tabindex="0" href="{{url_for('set_locale', return_to=request.script_root + request.full_path, lang='pt')}}">PT</a>
    {% endif %}
    {% if username %}
        <a class="right" tabindex="0" target="_blank" href="https://www.wikidata.org/wiki/Special:Contributions/{{username}}">{{username}}</a>
    {% else %}
        <a class="right" tabindex="0" href="{{ url_for('login', next=request.script_root + request.full_path) }}">{{ _("Authenticate")}}</a>
    {% endif %}
    <a tabindex="0" id="menu" href="javascript:void(0);" class="icon" onclick="menuFunction()" aria-label='{{_("Menu")}}'><i class="fa fa-bars"></i></a>
</nav>

```