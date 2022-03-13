import os
from datetime import datetime
import json

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData


class Database:
    def __init__(self):
        self.Base = automap_base()
        self.db_path = 'sqlite:///{}'.format(os.path.abspath('application/database/counter_results.db'))
        self.engine = create_engine(self.db_path)
        self.Base.prepare(self.engine, reflect=True)
        self.metadata = MetaData()
        self.results = self.Base.classes.Results
        self.session = Session(self.engine)

    def insert(self, site_name, url, tags_dict):
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
        self.session.add(self.results(site_name=site_name, url=url, date=date_time, tags_dict=json.dumps(tags_dict)))
        self.session.commit()

    def fetch(self, domain):
        result = self.session.query(self.results).where(self.results.site_name == domain).first()
        if result is None:
            tags_dict = None
        else:
            tags_dict = json.loads(result.tags_dict)

        return tags_dict
