from GUI.gui_login import run_login_screen
from sqlalchemy.orm import close_all_sessions
from domain.database import init_db, session
from domain.user import User
from domain.plants import Plant
import seed
from sqlalchemy.exc import OperationalError

def is_database_initialized():
    try:
        session.query(Plant).first()
        close_all_sessions()
        return True
    except OperationalError:
        return False

if not is_database_initialized():
    init_db()
    seed.seed_data()
    test = session.query(User).first()
    print("This is your first time running the app. A test user has been setup for you")
    print("The username is: " + test.username)
    print("The password is: " + test.password)

run_login_screen() 
