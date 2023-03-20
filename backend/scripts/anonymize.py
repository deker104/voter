import simplejson as json

from pathlib import Path
from random import shuffle

from config import OWNER_ID

database = json.loads(Path('database.json').read_text())
shuffle(database)
for vote in database:
    vote['id'] = OWNER_ID
Path('anonymized.json').write_text(json.dumps(database))
