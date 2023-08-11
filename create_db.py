from app import create_app, db
from app.model import User_profile

# Create the Flask app
app = create_app()

# Create the database and tables
with app.app_context():
    db.create_all()



# Function to populate the database with sample data
def create_sample_data():
    with app.app_context():
        # Create sample users
        user1 = User_profile(name='John Doe', phone_number='1234567890', email='john@example.com', password  = 'spam@1')
        user2 = User_profile(name='Jane Smith', phone_number='9876543210', email='jane@example.com', password  = 'spam@2')
        user3 = User_profile(name='Mike Johnson', phone_number='5555555555', password  = 'spam@2')

        # Add the objects to the session
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        # Commit the changes to the database
        db.session.commit()

if __name__ == '__main__':
    create_sample_data()
