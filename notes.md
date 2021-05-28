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