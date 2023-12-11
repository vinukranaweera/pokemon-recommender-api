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

        # Find the weakest and strongest stats of the input Pokemon
        weakest_stat = min(stats, key=stats.get)
        strongest_stat = max(stats, key=stats.get)
        
        print(weakest_stat)
        # Filter out types with effectiveness less than 1
        filtered_types = [type for type, effectiveness in effectiveness.items() if effectiveness >= 1]

        # Find the type(s) with the maximum effectiveness
        max_effectiveness = max(filtered_types, key=effectiveness.get)

        # Query for Backup Pokemon
        recommendation_query1 = {
            "$and": [
                {"$or": [
                    {"Primary Type": max_effectiveness},
                    {"Secondary Type": max_effectiveness}
                ]},
            ]
        }

        # Query for Pokemon with the chosen type(s) and stats
        recommendation_query = {
            "$and": [
                {"$or": [
                    {"Primary Type": max_effectiveness},
                    {"Secondary Type": max_effectiveness}
                ]},
            ]
        }
        # List to store conditions
        # Check if all stats are equal (for Mythicals)
        if all(value == 100 for value in stats.values()):
            conditions = [
                {'Sp_Attack': {'$gte': 100}},
                {'Sp_Defense': {'$gte': 100}},
            ]
        else:
            conditions = []

            # Maximum number of conditions
            max_conditions = 3

            # Defensive Conditions
            if strongest_stat in ['Attack', 'Sp_Attack'] and stats[strongest_stat] >= 150:
                if stats['Attack'] > stats['Sp_Attack']:
                    if stats[strongest_stat] >= 150 and stats['Speed'] >= 100 and len(conditions) < max_conditions:
                        conditions.extend([
                        {'Defense': {'$gte': 150}},
                        {'Speed': {'$gte': 100}}
                    ])
                else:
                    if stats[strongest_stat] >= 150 and stats['Speed'] >= 100:
                        conditions.extend([
                        {'Sp_Defense': {'$gte': 150}},
                        {'Speed': {'$gte': 100}}
                    ])
            elif strongest_stat in ['Attack', 'Sp_Attack'] and 150 > stats[strongest_stat] >= 100:
                if stats['Attack'] > stats['Sp_Attack']:
                    if stats['Speed'] >= 75 and len(conditions) < max_conditions:
                        conditions.extend([
                        {'Defense': {'$gte': 100}},
                        {'Speed': {'$gte': 75}}
                    ])
                else:
                    if stats['Speed'] >= 75:
                        conditions.extend([
                        {'Sp_Defense': {'$gte': 100}},
                        {'Speed': {'$gte': 75}}
                    ])
            else:
                if stats['Attack'] > stats['Sp_Attack']:
                    if stats['Speed'] >= 50 and len(conditions) < max_conditions:
                        conditions.extend([
                        {'Defense': {'$gte': 75}},
                        {'Speed': {'$gte': 50}}
                    ])
                else:
                    if stats['Speed'] >= 50:
                        conditions.extend([
                        {'Sp_Defense': {'$gte': 75}},
                        {'Speed': {'$gte': 50}}
                    ])
            
            # Offensive Conditions
            if weakest_stat in ['Sp_Defense', 'Defense'] and stats[weakest_stat] < 150:
                if stats['Defense'] < stats['Sp_Defense']:
                    if stats[weakest_stat] >= 100 and len(conditions) < max_conditions:
                        conditions.append({'Attack': {'$gte': 120}})
                else:
                    if stats[weakest_stat] >= 100 and len(conditions) < max_conditions:
                        conditions.append({'Sp_Attack': {'$gte': 120}}) 
            elif weakest_stat in ['Sp_Defense', 'Defense'] and stats[weakest_stat] < 100:
                if stats['Defense'] < stats['Sp_Defense']:
                    if stats[weakest_stat] > 50 and len(conditions) < max_conditions:
                        conditions.append({'Attack': {'$gte': 100}})
                else:
                    if stats[weakest_stat] > 50 and len(conditions) < max_conditions:
                        conditions.append({'Sp_Attack': {'$gte': 100}})
            else:
                if stats['Defense'] < stats['Sp_Defense']: 
                    if stats[weakest_stat] < 50 and len(conditions) < max_conditions:
                        conditions.append({'Attack': {'$gte': 80}})
                else:
                    if stats[weakest_stat] < 50 and len(conditions) < max_conditions:
                        conditions.append({'Sp_Attack': {'$gte': 80}})

            # Miscellaneous Conditions
            if weakest_stat == 'HP' and stats['HP'] < 150:
                attack_condition1 = {'$or': [
                    {'Speed': {'$gte': 100}},
                    {'HP': {'$gte': 100}}
                ]}
                attack_condition2 = {'$or': [
                    {'Speed': {'$gte': 80}},
                    {'HP': {'$gte': 80}}
                ]}
                attack_condition3 = {'$or': [
                    {'Speed': {'$gte': 60}},
                    {'HP': {'$gte': 60}}
                ]}
                if stats['HP'] >= 100 and len(conditions) < max_conditions:
                    conditions.append(attack_condition1)
                elif weakest_stat == 'HP' and stats['HP'] < 100:
                    if 100 > stats['HP'] > 50 and len(conditions) < max_conditions:
                        conditions.append(attack_condition2)
                else:
                    if stats['HP'] < 50 and len(conditions) < max_conditions:
                        conditions.append(attack_condition3)

            if weakest_stat == 'Speed' and stats['Speed'] < 150:
                defense_condition1 = {'$or': [
                    {'HP': {'$gte': 100}},
                    {'Speed': {'$gte': 100}}
                ]}
                defense_condition2 = {'$or': [
                    {'HP': {'$gte': 80}},
                    {'Speed': {'$gte': 80}}
                ]}
                defense_condition3 = {'$or': [
                    {'HP': {'$gte': 60}},
                    {'Speed': {'$gte': 60}}
                ]}
                if stats['Speed'] >= 100 and len(conditions) < max_conditions:
                    conditions.append(defense_condition1)
                elif weakest_stat == 'Speed' and stats['Speed'] < 100:
                    if stats['Speed'] > 50 and len(conditions) < max_conditions:
                        conditions.append(defense_condition2)
                else:
                    if stats['Speed'] < 50 and len(conditions) < max_conditions:
                        conditions.append(defense_condition3)
        
        # Print conditions before extending recommendation query
        #print(f"Conditions before extending: {conditions}")
        # Extend recommendation query with conditions
        if conditions:
            recommendation_query["$and"].extend(conditions)

        matching_pokemon_cursor = pokeCollection.find(recommendation_query)

        # Convert the cursor to a list
        matching_pokemon_list = list(matching_pokemon_cursor)

        if matching_pokemon_list:
            # Randomly choose one Pokemon from the list
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
            #print(f"Recommendation query: {recommendation_query}")
            return response
        else:
            # Backup if no recommendation
            matching_pokemon_cursor1 = pokeCollection.find(recommendation_query1)

            # Convert the cursor to a list
            matching_pokemon_list1 = list(matching_pokemon_cursor1)
            print(matching_pokemon_list1)

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
