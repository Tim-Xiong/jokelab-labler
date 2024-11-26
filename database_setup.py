import pandas as pd
import random
import argparse
from app import app, db
from models import Joke

def setup_database(num_jokes):
    """
    Sets up the database by creating tables and populating it with a specified number of jokes from a CSV file.
    Args:
        num_jokes (int): The number of jokes to add to the database.
    Raises:
        FileNotFoundError: If the CSV file containing jokes is not found.
        ValueError: If the CSV file does not contain the required 'Joke' column.
    Notes:
        - The function reads jokes from a CSV file named 'shortjokes.csv'.
        - If the number of jokes requested exceeds the number available in the CSV file, it will add all available jokes.
        - The jokes are randomly selected from the CSV file.
    """
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Load jokes from CSV
        csv_file_path = 'shortjokes.csv'  # Adjust the path if needed
        jokes_df = pd.read_csv(csv_file_path)
        
        # Ensure the number of jokes requested is not more than available
        num_jokes = min(num_jokes, len(jokes_df))
        
        # Randomly select the specified number of jokes
        selected_jokes = jokes_df.sample(n=num_jokes)
        
        # Add jokes to the database
        for _, row in selected_jokes.iterrows():
            joke = Joke(text=row['Joke'])
            db.session.add(joke)
        
        db.session.commit()
        print(f"{num_jokes} jokes added successfully!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Set up the jokes database.")
    parser.add_argument(
        '--num_jokes',
        type=int,
        default=10,
        help='Number of jokes to import into the database'
    )
    args = parser.parse_args()
    
    setup_database(args.num_jokes)
