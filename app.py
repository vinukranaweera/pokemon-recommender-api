from flask import Flask, request, jsonify
from flask_cors import CORS
import pprint
#import os
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from io import StringIO
import random
# Load the dataset
import pandas as pd
import certifi
ca = certifi.where()

# api route
app = Flask(__name__)
CORS(app)
#MongoDb config
client = MongoClient('mongodb+srv://poke:z123123@cluster0.315hxqa.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client['pokemon']
pokeCollection = db['pokemon']

# Adjust file path to the file's location
pokemon_data = pd.DataFrame(list(pokeCollection.find({}, {"_id": 0}).sort("Pokedex Number")))

# Map 'Status' to the corresponding index
status_mapping = {
    'Normal': 0,
    'Sub Legendary': 1,
    'Mythical': 2,
    'Legendary': 3
}

pokemon_data['Status'] = pokemon_data['Status'].map(status_mapping)

# Extract relevant features and target variables for primary and secondary types
X = pokemon_data[['Generation', 'Status', 'Against Normal', 'Against Fire', 'Against Water', 'Against Electric', 
                  'Against Grass', 'Against Ice', 'Against Fighting', 'Against Poison', 'Against Ground', 'Against Flying',
                  'Against Psychic', 'Against Bug', 'Against Rock', 'Against Ghost', 'Against Dragon',
                  'Against Dark', 'Against Steel', 'Against Fairy']]
y_primary = pokemon_data['Primary Type']
y_secondary = pokemon_data['Secondary Type']
# Split into training and testing sets
X_train, X_test, y_primary_train, y_primary_test, y_secondary_train, y_secondary_test = train_test_split(
    X, y_primary, y_secondary, test_size=0.2, random_state=42
)
# Train the classifier for primary typing
rf_classifier_primary = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier_primary.fit(X_train, y_primary_train)
# Train the classifier for secondary typing
rf_classifier_secondary = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier_secondary.fit(X_train, y_secondary_train)
# Test set to predict the primary and secondary typing of Pokemon
y_primary_pred = rf_classifier_primary.predict(X_test)
y_secondary_pred = rf_classifier_secondary.predict(X_test)
# Calculate accuracy and other evaluation metrics for primary typing
accuracy_primary = accuracy_score(y_primary_test, y_primary_pred)
classification_rep_primary = classification_report(y_primary_test, y_primary_pred)
# Calculate accuracy and other evaluation metrics for secondary typing
accuracy_secondary = accuracy_score(y_secondary_test, y_secondary_pred)
classification_rep_secondary = classification_report(y_secondary_test, y_secondary_pred)
# Predict the primary and secondary types for one Pokemon

# Format is Generation, Status, Type effectiveness (Against Normal, Against Fire, ... , Against Fairy)
# Insert values in the correct order. Change 'Status' to its corresponding index
new_pokemon_attributes = [[1, 0, 1, 2, 0.5, 0.5, 0.25, 2, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 0.5]]  

# Create a DataFrame with the same column names for the test data
new_pokemon_data = pd.DataFrame(new_pokemon_attributes, columns=X.columns)

predicted_primary_type = rf_classifier_primary.predict(new_pokemon_data)
predicted_secondary_type = rf_classifier_secondary.predict(new_pokemon_data)

@app.route('/predict', methods=['POST'])
def predict():
    data = str(request.get_json()).replace(", ", ",").replace(": ", ":").replace("'", '"')
    string_io = StringIO(data)
    eval_data = pd.read_json(string_io, orient="split")
    # Map 'Status' to the corresponding index
    status_mapping = {
      'Normal': 0,
      'Sub Legendary': 1,
      'Mythical': 2,
      'Legendary': 3
    }
    eval_data['Status'] = eval_data['Status'].map(status_mapping)
    # Use the trained models to predict types
    predicted_primary_type = rf_classifier_primary.predict(eval_data)
    predicted_secondary_type = rf_classifier_secondary.predict(eval_data)
    # Create a DataFrame with the predicted types and the original data
    result_df = eval_data.copy()
    result_df['Predicted Primary Type'] = predicted_primary_type
    result_df['Predicted Secondary Type'] = predicted_secondary_type
    # Export the results to another CSV file
    res = result_df.to_json(orient="split")
    return res
@app.route('/pokemon', methods=['GET'])
def getPokemonByNameIdType():
    name = request.args.get('name')
    id = request.args.get('id')
    type = request.args.get('type')
    type1 = request.args.get('type1')
    type2 = request.args.get('type2')
    if(name):
        res = pokeCollection.find_one({"Name": name}, {"_id": 0})
        return res
    elif(id):
        res = pokeCollection.find_one({"Pokedex Number": int(id)}, {"_id": 0})
        return res
    elif(type):
        res = list(pokeCollection.find({ "$or": [{"Primary Type": type}, {"Secondary Type": type}] }, {"_id": 0}))
        return res
    else:
        res = list(pokeCollection.find({"$or": [{ "$and": [{"Primary Type": type2}, {"Secondary Type": type1}] }, { "$and": [{"Primary Type": type1}, {"Secondary Type": type2}] }]}, {"_id": 0}))
        return res

@app.route('/recommendations/<pokemon_name>', methods=['GET'])
def get_pokemon_recommendation(pokemon_name):
    myquery = {"Name": pokemon_name.capitalize()}
    result = pokeCollection.find_one(myquery)

    if result:
        # Extract relevant fields
        effectiveness = {
            'Fire': result['Against Fire'], 
            'Water': result['Against Water'], 
            'Electric': result['Against Electric'],
            'Grass': result['Against Grass'], 
            'Ice': result['Against Ice'], 
            'Fighting': result['Against Fighting'], 
            'Poison': result['Against Poison'],
            'Ground': result['Against Ground'], 
            'Flying': result['Against Flying'], 
            'Psychic': result['Against Psychic'], 
            'Bug': result['Against Bug'],
            'Rock': result['Against Rock'], 
            'Ghost': result['Against Ghost'], 
            'Dragon': result['Against Dragon'], 
            'Dark': result['Against Dark'],
            'Steel': result['Against Steel'], 
            'Fairy': result['Against Fairy']
        }
        
        stats = {
            'HP': result['HP'],
            'Attack': result['Attack'],
            'Defense': result['Defense'],
            'Sp_Attack': result.get('Sp', {}).get(' Attack'),
            'Sp_Defense': result.get('Sp', {}).get(' Defense'),
            'Speed': result['Speed']
        }

        primary_type = result['Primary Type']
        secondary_type = result.get('Secondary Type', None)

        # Resistance values for types: 0 = immune, 0.25 = 4x resistant, 0.5 = resistant, 1 = normal, 2 = weak, 4 = 4x weak
        type_resistances = {
            "Normal": {"Fighting": 2, "Ghost": 0},
            "Fire": {"Water": 2, "Rock": 2, "Ground": 2, "Fire": 0.5, "Grass": 0.5, "Ice": 0.5, "Bug": 0.5, "Steel": 0.5, "Fairy": 0.5},
            "Water": {"Electric": 2, "Grass": 2, "Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5},
            "Electric": {"Ground": 0, "Electric": 0.5, "Flying": 0.5, "Steel": 0.5},
            "Grass": {"Fire": 2, "Ice": 2, "Poison": 2, "Flying": 2, "Bug": 2, "Water": 0.5, "Electric": 0.5, "Grass": 0.5, "Ground": 0.5},
            "Ice": {"Fire": 2, "Fighting": 2, "Rock": 2, "Steel": 2, "Ice": 0.5},
            "Fighting": {"Flying": 2, "Psychic": 2, "Fairy": 2, "Bug": 0.5, "Rock": 0.5, "Dark": 0.5},
            "Poison": {"Ground": 2, "Psychic": 2, "Grass": 0.5, "Fighting": 0.5, "Poison": 0.5, "Bug": 0.5, "Fairy": 0.5},
            "Ground": {"Water": 2, "Grass": 2, "Ice": 2, "Poison": 0.5, "Rock": 0.5, "Electric": 0},
            "Flying": {"Electric": 2, "Ice": 2, "Rock": 2, "Grass": 0.5, "Fighting": 0.5, "Bug": 0.5, "Ground": 0},
            "Psychic": {"Bug": 2, "Ghost": 2, "Dark": 2, "Fighting": 0.5, "Psychic": 0.5},
            "Bug": {"Fire": 2, "Flying": 2, "Rock": 2, "Grass": 0.5, "Fighting": 0.5, "Ground": 0.5},
            "Rock": {"Water": 2, "Grass": 2, "Fighting": 2, "Ground": 2, "Steel": 2, "Normal": 0.5, "Fire": 0.5, "Poison": 0.5, "Flying": 0.5},
            "Ghost": {"Ghost": 2, "Dark": 2, "Poison": 0.5, "Bug": 0.5, "Normal": 0, "Fighting": 0},
            "Dragon": {"Ice": 2, "Dragon": 2, "Fairy": 2, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Grass": 0.5},
            "Dark": {"Fighting": 2, "Bug": 2, "Fairy": 2, "Ghost": 0.5, "Dark": 0.5, "Psychic": 0},
            "Steel": {"Fire": 2, "Fighting": 2, "Ground": 2, "Normal": 0.5, "Grass": 0.5, "Ice": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 0.5, "Dragon": 0.5, "Steel": 0.5, "Fairy": 0.5, "Poison": 0},
            "Fairy": {"Poison": 2, "Steel": 2, "Fighting": 0.5, "Bug": 0.5, "Dark": 0.5, "Dragon": 0},
        }

        # Calculate combined resistances
        combined_resistances = {}
        for attacking_type in type_resistances.keys():
            type1_modifier = type_resistances.get(primary_type, {}).get(attacking_type, 1)
            type2_modifier = type_resistances.get(secondary_type, {}).get(attacking_type, 1) if secondary_type else 1
            combined_resistances[attacking_type] = type1_modifier * type2_modifier

        # Filter for the most resistant type
        resistant_types = {k: v for k, v in combined_resistances.items() if v <= 1}
        if resistant_types:
            most_resistant_type = min(resistant_types, key=resistant_types.get)
        else:
            most_resistant_type = None
        
        # Determine if the Pokémon is mainly offensive or defensive
        offensive_stats = ['Attack', 'Sp_Attack', 'Speed']
        defensive_stats = ['HP', 'Defense', 'Sp_Defense']
        
        total_offensive = sum(stats[stat] for stat in offensive_stats)
        # print('total offensive stats:', total_offensive)
        total_defensive = sum(stats[stat] for stat in defensive_stats)
        # print('total defensive stats:', total_defensive)
        total = total_defensive + total_offensive
        # print('total:', total)

        # Choose offensive or defensive approach for recommendation
        recommendation_type = 'defensive' if total_offensive >= total_defensive else 'offensive'
        if total > 550:
            recommendation_type = 'offensive' if total_offensive >= total_defensive else 'defensive'

        # print(recommendation_type)

        # Filter out types with effectiveness less than 1
        filtered_types = [type for type, value in effectiveness.items() if value >= 1]

        if not filtered_types:
            return {"error": "No types with effectiveness found for this Pokémon."}

        # Find the type with maximum effectiveness
        max_effectiveness = max(filtered_types, key=effectiveness.get)

       # Query logic based on the total stats
        if total > 550 and most_resistant_type:
            query = {
                "$or": [
                    {"Primary Type": most_resistant_type},
                    {"Secondary Type": most_resistant_type}
                ]
            }
            # print('Resistant:', most_resistant_type)
        else:
            query = {
                "$or": [
                    {"Primary Type": max_effectiveness},
                    {"Secondary Type": max_effectiveness}
                ]
            }
            # print('Effective:', max_effectiveness)
        
        # Query for Backup Pokemon
        recommendation_query1 = {
            "$and": [
                {"$or": [
                    {"Primary Type": max_effectiveness},
                    {"Secondary Type": max_effectiveness}
                ]},
            ]
        }

        if recommendation_type == 'offensive':
            query["$and"] = [{"$or": [
                {"Attack": {"$gte": 100}},
                {"Sp_Attack": {"$gte": 100}},
                {"Speed": {"$gte": 100}}
            ]}]
        else:  # Defensive recommendation
            query["$and"] = [{"$or": [
                {"HP": {"$gte": 100}},
                {"Defense": {"$gte": 100}},
                {"Sp_Defense": {"$gte": 100}}
            ]}]

        matching_pokemon_cursor = pokeCollection.find(query)
        matching_pokemon_list = list(matching_pokemon_cursor)

        if matching_pokemon_list:
            random_recommendation = random.choice(matching_pokemon_list)

            response = {
                'Name': random_recommendation['Name'],
                'Primary Type': random_recommendation['Primary Type'],
                'Secondary Type': random_recommendation['Secondary Type'],
                'Pokedex Number': random_recommendation['Pokedex Number'],
                'Stats': {
                    'HP': random_recommendation['HP'],
                    'Attack': random_recommendation['Attack'],
                    'Defense': random_recommendation['Defense'],
                    'Sp': {
                        'Attack': random_recommendation.get('Sp', {}).get(' Attack'),
                        'Defense': random_recommendation.get('Sp', {}).get(' Defense')
                    },
                    'Speed': random_recommendation['Speed']
                }
            }
            return response
        else:
            # Backup if no recommendation
            matching_pokemon_cursor1 = pokeCollection.find(recommendation_query1)

            # Convert the cursor to a list
            matching_pokemon_list1 = list(matching_pokemon_cursor1)

            if matching_pokemon_list1:
            # Randomly choose one Pokemon from the list
                random_recommendation1 = random.choice(matching_pokemon_list1)

                response1 = {
                    'Name': random_recommendation1['Name'],
                    'Primary Type': random_recommendation1['Primary Type'],
                    'Secondary Type': random_recommendation1['Secondary Type'],
                    'Pokedex Number': random_recommendation1['Pokedex Number'],
                    'Stats': {
                        'HP': random_recommendation1['HP'],
                        'Attack': random_recommendation1['Attack'],
                        'Defense': random_recommendation1['Defense'],
                        'Sp': {
                            'Attack': random_recommendation1.get('Sp', {}).get(' Attack'),
                            'Defense': random_recommendation1.get('Sp', {}).get(' Defense')
                        },
                        'Speed': random_recommendation1['Speed']
                    }
                }
                return response1


#port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    app.run(debug=True)
