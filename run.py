from poorcms import app, db
from poorcms.models import User, StaticPage

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, StaticPage=StaticPage)
