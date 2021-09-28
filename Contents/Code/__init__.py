import os, json, urllib, re

class JSONAgent(Agent.Artist):
    name = 'JSON Metadata'
    languages = [Locale.Language.English]
    primary_provider = True
    persist_stored_files = False
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang):
        return
        
    def update(self, metadata, media, lang):
        return

class JSONAgent(Agent.Album):
    name = 'JSON Metadata'
    languages = [Locale.Language.English]
    primary_provider = True
    persist_stored_files = False
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang):
        path = os.path.join(os.path.dirname(urllib.unquote_plus(media.filename)), 'Info.json')

        if os.path.exists(path):
            results.Append(MetadataSearchResult(id = path, name=media.album, score = 100, lang=lang))

    def update(self, metadata, media, lang):
        path = metadata.id
        
        info = JSON.ObjectFromString(Core.storage.load(path))
        Log('----------------------------------Album Update--------------------------------------------------')
        try: Log(Core.storage.load(path))
        except: pass
        try: Log(re.sub(r'(\d)(st|nd|rd|th)', r'\1', info['date']))
        except: pass
        try: Log(Datetime.ParseDate(re.sub(r'(\d)(st|nd|rd|th)', r'\1', info['date'])))
        except: pass
        try: Log(info['title'])
        except: pass
        try: Log(info['authors'])
        except: pass
        try: Log(info['series'])
        except: pass
        try: Log(info['narrators'])
        except: pass
        try: Log(info['studio'])
        except: pass
        try: Log(float(info['rating']) * 2)
        except: pass
        try: Log(info['genres'])
        except: pass
        try: Log(info['description'])
        except: pass
        Log('------------------------------------------------------------------------------------------------')

        metadata.originally_available_at = Datetime.ParseDate(re.sub(r'(\d)(st|nd|rd|th)', r'\1', info['date']))
        metadata.title = info['title']
        media.artist = info['authors']
        metadata.moods.clear()
        metadata.moods.add(info['series'])
        
        metadata.genres.clear()
        for g in info['narrators']:
            metadata.styles.add(g)
            
        metadata.studio = info['studio']
        metadata.rating = float(info['rating']) * 2
        
        metadata.genres.clear()
        for g in info['genres']:
            metadata.genres.add(g)
            
        metadata.summary = info['description']
