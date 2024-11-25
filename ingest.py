
from app import db
from app.models import UserPoints
from app import create_app
app = create_app()


def run():
    # Start Flask's app context
    with app.app_context():
        # Perform your database operations here
        user1 = UserPoints(address='0x12345167890abcdef1234567890abcdef12345678', points=100)
        user2 = UserPoints(address='0xabcde1fabcdefabcdefabcdefabcdefabcdefabcdef', points=200)

        # Add to the session
        db.session.add(user1)
        db.session.add(user2)

        # Commit to the database
        db.session.commit()

        print("Users have been added to the database!")


# Execute the script
if __name__ == "__main__":
    run()
