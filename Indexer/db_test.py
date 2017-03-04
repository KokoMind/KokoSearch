from Indexer.db_model import *

create_data_base()

d = Document.get(Document.id == 4)
print(d.c1.num_of_docs)
