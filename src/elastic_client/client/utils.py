import json
from configs import EMBEDDING_DIM, configs_path
from elasticsearch.helpers import parallel_bulk

def print_query_result(obj):
  lang = obj['lang']
  print(f"ID: {obj['_id']}, SCORE: {obj['_score']}")
  print(f"LANG: {lang}, CONTENT: {obj[lang][0:50]}")
  print(f"CREATED: {obj['createdDate']}")

def load_pipeline(id: str):
  with open(configs_path / 'pipelines' / f"{id}.json") as f:
    return _replace_dim(json.load(f))

def load_mapping(id: str):
  with open(configs_path / 'mappings' / f"{id}.json") as f:
    return _replace_dim(json.load(f))

def load_query(id: str):
  with open(configs_path / 'queries' / f"{id}.json") as f:
    return json.load(f)
  
def _replace_dim(obj):
  if isinstance(obj, dict):
    for key, value in obj.items():
      if key == 'dims':
        obj[key] = EMBEDDING_DIM
      else:
        obj[key] = _replace_dim(value)
  elif isinstance(obj, list):
    for i in range(len(obj)):
      obj[i] = _replace_dim(obj[i])
  return obj

def bulk_index(client, index, pipeline_id, docs):
  og_length = len(docs)
  actions = [
    {
      '_index': index,
      '_id': doc['id'],
      'pipeline': pipeline_id,
      **doc
    } for doc in docs
  ]
  indexed = 0

  for succ, info in parallel_bulk(client, actions): 
    if(succ):
      indexed += 1
    else:
      print(f"ERROR INDEXING? \n {info}")
  return og_length, indexed


def get_by_id(client, index, id):
  result = client.get(index = index,id = id)
  return result['_source']

def get_content(source):
  return source.get('en') or source.get('hu') or source.get('de') 

def get_stopwords():
  # Copied from spacy lang modules, to prevent having to import spacy
  return ['fünftes', 'keine', 'geworden', 'kleines', 'does', 'míg', 'sometimes', 'anyhow', 'somewhere', 'ebenso', 'former', 'between', 'erst', 'e', 'since', 'außerdem', 'thus', 'hatten', 'dort', 'seine', 'really', 'grosser', 'their', 'gedurft', 'sagt', 'mancher', 'wenn', 'würden', 'while', 'dich', 'rechte', 'anyone', 'seien', 'diejenige', 'arra', 'two', 'ebben', 'derjenige', 'zusammen', 'meinem', 'ganzen', 'whatever', 'even', 'weiteres', 'unsere', 'onto', 'besonders', 'lett', 'the', 'nine', 'whereupon', 'á', 'geht', 'mochte', 'wart', 'afterwards', 'ganzer', 'him', 'yourselves', 'trotzdem', 'dir', 'formerly', 'vannak', 'serious', 'this', 'damals', 'moreover', 'például', 'keinen', 'előtt', 'mely', 'vierte', 'mi', 'szemben', 'jól', 'euch', 'denn', 'wenig', 'az', 'whom', 'mintha', 'done', 'soll', 'cikk', 'miért', 'mögen', 'nekem', 'wessen', 'minden', 'grossen', 'ilyenkor', 'else', 'schlecht', 'wurden', 'wherever', 'therefore', 'meiner', 'vom', 'ihn', 'gewollt', 'gern', 'oket', 'el', 'elsewhere', 'überhaupt', 'noch', 'hoch', 'meines', '‘m', 'diejenigen', '’d', 'allen', 'wem', 'then', 'rechter', 'ganzes', 'egyes', 'therein', 'meine', 'three', 'same', 'túl', 'twelve', 'mine', 'dürft', 'jedem', 'nein', 'schon', 'én', 'ehhez', 'statt', 'however', 'dieselben', 'ekkor', 'five', 'lange', 'egy', 'eigenen', 'unless', 'of', 'anyway', 'myself', 'wollen', 'gekonnt', 'ugyanis', 'auch', 'a', 'say', 'amely', 'voltak', 'dürfen', 'und', 'ahogy', 'wieder', 'csak', 'für', 'einer', 'forty', 'his', 'anderen', 'became', 'zweiten', 'jahren', 'ott', 'dessen', 'wahr', 'át', 'guter', 'must', 'nicht', 'neben', 'keiner', 'nun', 'na', 'siebter', 'will', 'bisher', 'oder', 'bald', 'part', 'call', 'sechs', 'számára', 'ohne', 'sixty', 'mochten', 'than', 'amikor', 'diesen', 'meinen', 'everyone', 'hätte', 'dadurch', 'danach', 'könnt', 'egyik', 'durften', 'fünften', 'dermassen', '‘re', 'ami', 'gutes', 'dementsprechend', 'waren', 'több', 'whither', '‘d', 'ezen', 'still', 'amit', 'einigen', '‘s', 'te', 'eleven', 'großen', 'with', 'siebenten', 'ehrlich', 'möglich', 'össze', 'dass', 'enough', 'leicht', 'achtes', 'tel', 'um', 'ha', 'sah', 'másik', 'fel', 'daraus', 'offen', 'seeming', 'nincs', 'indeed', 'hinter', 'etwa', 'wirklich', 'after', 'einmaleins', 'daran', 'azon', 'darauf', 'anything', 'twenty', 'thereby', 'gegenüber', 'valaki', '’m', 'zweiter', 'more', 'macht', 'they', 'noone', 'gemocht', 'wen', 'im', 'each', 'vergangenen', 'become', 'van', 'cannot', 'lenne', 'gesagt', 'jene', 'igen', 'tat', 'war', 'amelyet', 'zum', 'jenem', 'behind', 'being', "'m", 'elég', 'least', 'demselben', 'dritten', 'őket', 'sagte', 'kaum', 'vagyok', 'welches', 'eddig', 'dasselbe', 'néhány', 'jemand', 'bereits', 'take', 'ezért', 'through', 'or', 'als', 'milyen', 'anders', 'over', 'ön', 'fünf', 'seid', 'dahin', 'mögt', 'werden', 'have', 'something', 'azzal', 'inkább', 'regarding', 'darum', 'kurz', 'ismét', 'mindent', 'wer', 'sollte', 'erre', 'due', 'deinem', 'amolyan', 'ennek', 'szerint', 'einen', 'yet', 'zeit', 'nélkül', 'keresztül', 'gab', 'vele', 'tage', 'úgy', 'seit', 'auf', 'eigener', 'jahre', 'nichts', 'eight', 'új', 'dazu', 'bekannt', 'almost', 'an', 'mein', 'ihres', 'azt', 'been', 'them', 'beide', 'deiner', 'ende', 'kommen', 'muß', 'acht', 'solcher', 'welchem', 'dieselbe', 'heute', 'sollen', 'dein', 'wird', 'sowie', 'neki', 'konnte', 'derselben', 'sok', 'derselbe', 'jeden', 'damit', 'morgen', 'dann', 'siebtes', 'wenige', 'wirst', 'pedig', 'becoming', 'hereupon', 'if', 'get', 'mit', 'között', 'that', 'egész', 'zweite', 'valami', 'zweites', 'itt', 'cikkek', 'mittel', 'n’t', 'vielleicht', 'using', 'große', 'közül', 'except', 'make', 'most', '’ll', 'can', 'see', 'niemand', 'sechstes', 'gerade', 'wollte', 'doing', 'ill', 'en', 'sei', 'andere', 'általában', 'einander', 'amongst', 'mostly', 'kívül', 'kein', 'weniger', 'szét', 'fifty', 'lenni', 'wollt', 'we', 'neunten', 'jenes', 'wegen', 'your', 'großer', 'ganze', 'amount', 'groß', 'ezzel', 'hers', 'also', 'because', 'dritte', 'semmi', 'lieber', 'mert', 'anderem', 'legyen', 'ag', 'nagyobb', 'otherwise', 'jedermanns', 'demgemäss', 'viszont', 'whether', 'jede', 'werde', 'during', 'desselben', 'sollten', 'nagyon', 'somehow', 'einiges', 'akik', 'thence', 'gleich', 'sechsten', 'tun', 'until', 'zehntes', 'továbbá', 'lehetett', 'erstes', 'next', 'dank', 'ihrer', 'de', 'stb.', 'musst', 'dahinter', 'nur', 'when', 'less', 'daselbst', 'durchaus', 'siebten', 'either', 'am', 'doch', 'man', 'welcher', 'von', 'keep', 'about', 'jemanden', 'ő', 'felé', 'musste', 'dazwischen', 'sie', 'gross', 'ill.', 'hätten', 'jobban', 'gemacht', 'why', 'allerdings', 'recht', 'ganz', 'herein', 'move', 'jemandem', 'natürlich', 'werdet', 'but', 'gar', 'utána', 'last', 'one', 'machte', 'wohl', 'lesz', 'daß', 'zehnten', 'volna', 'us', 'ihm', 'whole', 'neither', 'unter', 'welche', 'dieses', 'illetve', 'seines', 'seitdem', 'kellett', 'viertes', 'mint', 'alatt', 'put', 're', 'újabb', 'einmal', 'amelyek', 'jenen', 'neun', 'zwischen', 'solches', 'bár', 'darunter', 'diese', 'hanem', 'ab', 'where', 'würde', 'zurück', 'all', 'ins', 'tag', 'again', 'other', 'wäre', 'aztán', 'deswegen', 'valamint', 'niemanden', 'neunter', 'daher', 'me', 'daneben', 'gekannt', 'manches', 'kann', 'beside', 'hogy', 'beiden', 'jedoch', 'mehr', 'hereafter', 'darüber', 'durfte', 'amelyekben', 'empty', 'zehnter', 'újra', 'maga', 'himself', 'indem', 'own', 'ne', 'durch', 'denselben', 'whereas', 'once', 'eigenes', 'ist', 'außer', 'zunächst', 'darfst', 'deine', 'seinem', 'hundred', 'kell', 'belül', 'nem', 'has', "'d", '’s', 'allem', 'may', 'fünfte', 'before', 'front', 'mussten', 'seems', 'eigene', 'zur', 'few', 'nothing', 'jedermann', 'wherein', 'egyéb', 'einem', 'lang', 'aller', 'ja', 'dieser', 'give', 'wir', 'még', 'back', 'des', 'benne', 'satt', "n't", 'dermaßen', 'side', 'magst', 'among', 'together', 'who', 'beim', 'below', 'such', 'you', 'i', 'diesem', 'many', 'gemusst', 'vielen', 'mikor', 'n‘t', 'du', 'hat', "'s", 'már', 'hereby', 'sondern', 'zuerst', 'against', 'bottom', 'in', 'toward', 'elso', 'deren', 'everything', 'yourself', 'kleinen', 'mich', 'willst', 'grosse', 'niemandem', 'first', 'immer', 'amelynek', 'thereupon', 'achter', 'viele', 'könnte', 'for', 'által', 'manchen', 'might', 'dem', 'nagy', 'ison', 'wurde', 'ahol', 'zwei', 'whereafter', 'denen', 'very', 'be', 'siebente', 'various', 'ausserdem', 'sem', 'nor', 'under', 'besser', 'vierter', 's', 'derjenigen', 'wenigstens', 'vagy', 'sokat', 'großes', 'meanwhile', 'any', 'well', 'genug', 'infolgedessen', 'across', 'können', 'only', 'should', 'its', 'down', 'off', 'from', 'irgend', 'mondta', 'besten', 'these', 'weiteren', 'sind', 'eben', 'egyre', 'what', 'ach', 'ihr', 'ezt', 'entweder', 'sonst', 'való', 'my', 'becomes', 'are', 'nevertheless', 'tehát', 'there', 'anywhere', 'did', 'ging', 'just', 'teil', 'vier', 'abban', 'fünfter', 'achten', 'now', 'out', 'beispiel', 'yours', 'sechste', 'never', 'keinem', 'beforehand', '’ve', 'mir', 'those', 'zu', 'could', 'not', 'solchem', 'weitere', 'után', 'le', 'do', 'ihnen', 'weniges', 'sich', 'demzufolge', 'here', 'azok', 'others', 'several', 'uhr', 'annak', 'nahm', 'none', 'je', 'eine', 'siebte', 'bin', 'dies', '‘ll', 'gute', 'zugleich', 'akár', 'both', 'towards', 'neuntes', 'davor', 'währenddem', 'neunte', 'seinen', 'ich', 'kleiner', 'emilyen', 'majd', 'how', 'rund', 'übrigens', 'drittes', 'wollten', 'go', 'dritter', 'ausser', 'gegen', 'no', 'although', 'zwanzig', 'around', 'he', 'up', 'show', 'upon', 'hence', 'aber', 'los', 'später', 'über', 'worden', 'nobody', 'beyond', 'eigen', 'darf', 'weil', 'heisst', 'thereafter', 'jó', 'ilyen', 'es', 'saját', 'often', 'neue', 'rechtes', 'azután', 'nowhere', 'mindig', 'aus', 'solchen', 'siebenter', 'haben', 'ours', 'manchem', 'solche', 'zehn', 'much', '’re', 'azért', 'jener', 'nach', 'thru', 'rá', 'grosses', 'warum', 'mivel', 'andern', 'gewesen', 'habt', 'dagegen', "'re", 'and', 'perhaps', 'ti', 'ihrem', 'volt', 'heißt', 'alles', 'aki', 'konnten', 'further', 'so', 'within', 'please', 'solang', 'our', 'wann', 'another', 'kam', 'allgemeinen', 'rechten', 'unser', 'hier', 'más', 'geschweige', 'amíg', 'always', 'das', 'six', 'alle', 'jetzt', 'elf', 'above', 'akkor', 'as', 'without', 'machen', 'sein', 'wo', 'fifteen', 'four', 'hiszen', 'miatt', 'talán', 'olyan', 'melyek', 'ten', 'whenever', 'vagyis', 'viel', 'ersten', 'hát', 'it', 'ez', 'mindenki', 'ellen', 'everywhere', 'erste', 'oft', 'weit', 'meg', 'tovább', 'herself', 'oben', 'at', 'bei', 'die', 'gibt', 'ca', 'és', 'magát', 'drei', 'top', 'ihre', 'sechster', 'whose', 'themselves', 'welchen', 'sometime', 'elott', 'dasein', 'möchte', 'mag', 'arról', 'achte', 'by', 'gut', 'éppen', 'hatte', 'mellett', 'siebentes', 'ourselves', 'ein', 'o', 'via', 'nie', 'selbst', 'er', 'richtig', '‘ve', 'were', 'name', 'vielem', 'müsst', 'sehr', 'latter', 'ok', 'ever', 'ahhoz', 'per', 'seiner', 'hast', 'jahr', 'jeder', 'nachdem', 'her', 'gehen', 'währenddessen', 'every', 'demgemäß', 'manche', 'leider', 'is', 'alone', 'lehet', 'unserer', "'ve", 'weiter', 'some', 'used', 'namely', 'to', 'früher', 'azonban', 'vissza', 'da', 'bis', 'zehnte', 'den', 'tagen', 'allein', 'zwar', 'amelyeket', 'third', 'itself', 'darin', 'dafür', 'deshalb', 'someone', 'egyetlen', 'full', 'der', 'davon', 'whoever', 'während', 'etwas', 'sieben', 'neuen', 'ezek', 'voltunk', 'einige', 'vor', 'kannst', 'erster', 'kommt', 'muss', 'uns', 'ma', 'persze', 'einiger', 'vergangene', 'made', 'wie', 'oda', 'kleine', 'bist', 'gehabt', 'dabei', 'she', 'utolsó', 'keressünk', 'endlich', 'vierten', 'eines', 'along', 'already', 'whence', 'müssen', 'teljes', 'which', 'ide', 'too', 'was', 'whereby', 'on', 'seem', 'had', "'ll", 'szinte', 'legalább', 'though', 'drin', 'demgegenüber', 'eloször', 'seemed', 'habe', 'elo', 'besides', 'into', 'hin', 'throughout', 'így', 'latterly', 'cikkeket', 'ihren', 'rather', 'ob', 'sokkal', 'would', 'hogyan', 'ki', 'quite', 'voltam', 'néha']