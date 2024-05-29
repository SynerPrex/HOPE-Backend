import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # Strip any leading/trailing whitespace from column names
        df.columns = df.columns.str.strip()
        return df
    except pd.errors.ParserError as e:
        print(f"Error reading {file_path}: {e}")
        return None

df = load_csv('data/data.csv')
if df is None:
    raise Exception("Failed to load CSV file")

# Print DataFrame columns for debugging
print(f"DataFrame columns after stripping whitespace: {df.columns.tolist()}")

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    
    if 'mood' not in data:
        return jsonify({"error": "Mood not provided"}), 400
    
    user_mood = data['mood'].strip().lower()  # Trim leading and trailing spaces, convert to lowercase

    # Check if 'Mood' column exists in the DataFrame
    if 'Mood' not in df.columns:
        return jsonify({"error": "'Mood' column not found in data"}), 500

    try:
        # Filter songs by the provided mood
        filtered_songs = df[df['Mood'].str.lower().str.strip() == user_mood]['Song Name'].tolist()
        
        if filtered_songs:
            return jsonify({"recommended_songs": filtered_songs})
        else:
            print(f"No songs found for mood: {user_mood}")
            print("All moods in the dataset:", df['Mood'].unique())
            return jsonify({"error": "No song found for the given mood"}), 404
    except Exception as e:
        print(f"Error during recommendation: {e}")
        return jsonify({"error": "An error occurred during recommendation"}), 500

