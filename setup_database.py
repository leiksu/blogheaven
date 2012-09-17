from library.core.database import init_db
init_db()
from library.core.database import db_session
from library.core.models import User
admin = User(1,'leiksu', 'default')
db_session.add(admin)
db_session.commit()