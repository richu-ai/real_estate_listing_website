from app import app, db
from app.models import User
from sqlalchemy import inspect

def test_db():
    with app.app_context():
        inspector = inspect(db.engine)
        # Print all table names
        print("Tables in database:", inspector.get_table_names())
        # Query all users
        users = User.query.all()
        print("Users in database:", users)

if __name__ == "__main__":
    test_db()
