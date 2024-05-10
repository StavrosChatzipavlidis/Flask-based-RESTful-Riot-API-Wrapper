# Flask-based-RESTful-Riot-API-Wrapper
Flask application that integrates with Riot's RESTful API to retrieve the match history of the last 20 games. This application leverages function chaining, API requests, and intermediate JSON indexing to provide comprehensive data, including champion icons and items used in each match.

# Project Structure

```bash
root/
 |-- api-data-retrieval/
 |   |-- get-summoner-data.py
 |   |-- get-match-data.py
 |   |-- get-match-ids-data-recursive
 |-- data processing/
 |   |-- index-data.py
 |   |-- parsing-data.py
 |-- flask-app/
 |   |-- app.py
 |   |-- automate_process.py
 |   |-- templates/
 |   |-- | -- index.html    
 |   |-- | -- formatted_output.html
 |   |-- static/
 |   |-- | -- img   
 |   |-- | -- items
 |   |-- | -- Augments    
 |   |-- | -- background.png
 |   |-- | -- background1.png

```

# Project Overview

## Interface
![Interface](./img/interface.png)

## Result
![Result](./img/result.png)

# TFT Summoner Data Retrieval

## Getting Started

Before running the script, ensure you have an API key from Riot Games. Do not share this API key with anyone.

## Project Prerequisites

```bash
Python 3
 |-- Libraries
 |   |-- requests
 |   |-- re
 |   |-- Collections
 |   |-- | -- Counter
 |   |-- | -- defaultdict
 |   |-- flask
 |   |-- | -- Flask 
 |   |-- | -- request
 |   |-- | -- render_template
```


You can install the requests and flask library using pip:

```python
pip install requests
pip install flask
```

You can now use the `requests` and `flask` library in your Python code to make HTTP requests and flask applications.

## Retrieving Summoner Data

The get-summoner-data function constructs the API URL with the provided summoner name, adds the necessary headers with an API key for authentication, and sends an HTTP GET request to the API endpoint. If the request is successful (status code 200), the function returns the summoner data in JSON format, including the Portable Unique ID (PUUID). Otherwise, it prints an error message and returns None. The provided example usage showcases how to call the function and extract the PUUID from the returned summoner data.

The script retrieves summoner data by following these steps:

1. Acquiring the Summoner PUUID
    - The function get_summoner_data takes a summoner name as input and queries the Riot Games API to retrieve summoner data.
    - Replace the placeholder API key in the script with your actual API key obtained from the Riot Games website.
    - After acquiring the summoner data, the PUUID (Portable Unique ID) is extracted from the response.
2. Using the Summoner PUUID
    - The obtained PUUID can be used for further API requests to fetch more specific data about the summoner, such as match history, match details, and more.

```python
def get_summoner_data(summoner_name):
    url = f'https://eun1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}'
    
    headers = {'X-Riot-Token': API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code)
        return None
    
summoner_data = get_summoner_data('Ariel%20Ibagaza%207')
puuid = summoner_data['puuid']
```

## Retrieving Match IDs

The purpose of coding the function to retrieve the IDs of the last 20 matches for a summoner with a specific PUUID is to facilitate the collection of recent match data for integration into our flask app.

```python
def get_match_ids(puuid):
    url = f'https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20'
    headers = {'X-Riot-Token': API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code)
        return None
```
We will store the last 20 games to iterate through them for the flask application but also the last game to experiment indexing with the returned json file to get the data needed.

```python
match_ids = get_match_ids(puuid)
match_id = get_match_ids(puuid)[0]
```
## Retrieving Match Data

Using the unique match ID obtained earlier, we can now retrieve the JSON file for a specific match associated with a summoner's PUUID. This allows us to access detailed information about the match, including participants and game events.

```python
def get_match_data(matchid):
    url = f'https://europe.api.riotgames.com/tft/match/v1/matches/{matchid}'
    
    headers = {
        'X-Riot-Token': API_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code)
        print('Response Content:', response.text)
        return None

get_match_data(match_id)
```

## Finding Specific Summoner

In a match with multiple participants, we often need to isolate data specific to a particular summoner. To accomplish this, we iterate through the participants' data and filter based on the summoner's unique ID (PUUID). The following code snippet achieves this:

```python
participant = next((p for p in get_match_data(match_id)['info']['participants'] if p['puuid'] == summoner_data['puuid']), None)
```

Here's how it works:

- Generator Expression: Using (p for p in ... if p['puuid'] == summoner_data['puuid']), we create a generator that iterates over each participant in the match data, filtering them based on their PUUID matching that of the summoner we're interested in.
- Next Function: The next(...) function retrieves the next item from the generator expression. It returns the first participant whose PUUID matches that of the summoner. If no such participant is found, it returns None.

## Retrieving Active Traits

Once we've identified the specific participant, we can extract their traits by iterating through their data. For instance, the following code snippet:

```python
traits_head = participant['traits'][:2]
```

returns a list containing the first 2 trait dictionaries associated with the summoner. These dictionaries provide details about the summoner's traits, such as their name, number of units, and tier.

To determine the active traits, we focus on those with a current tier greater than 0. For instance:

```python
print("Is 8 Bit active?", participant['traits'][0]['tier_current'] > 0,
      "\nIs Crowd Diver active ?", participant['traits'][1]['tier_current'] > 0)
```
This code snippet checks if the trait "8 Bit" is active (tier_current > 0), as well as the trait "Crowd Diver". The output reveals whether each trait is active based on their current tier.

## Retrieving Augments

Retrieving augments for a summoner is a straightforward process. Accessing the participant['augments'] data provides a list of augments associated with the summoner. For example, it returns: ['TFT10_Augment_SticksAndStones', 'TFT9_Augment_YouHaveMySword', 'TFT9_Augment_HedgeFundPlusPlus'].

To present the augments in a more readable format, we can clean the list using the following code snippet:
cleaning it:

```python
new_augments = [' '.join(re.findall('[A-Z][^A-Z]*', augment.split('_', 2)[-1])) for augment in participant['augments']]
```

This code snippet utilizes regex to split each augment string into words, capitalizing the first letter of each word. For instance, the cleaned list looks like: ['Sticks And Stones', 'You Have My Sword', 'Hedge Fund Plus Plus'].

## Retrieving Final Units

To retrieve the final units for a summoner, we employ a straightforward method. Iterating through the participant's units data, we extract the character IDs associated with each unit. Here's how it's done:

```python
units = []

for unit in participant['units']:
    # Extracting character ID
    character_id = unit['character_id']

    # Cleaning character ID
    underscore_index = character_id.find('_')
    if underscore_index != -1:
        character_id = character_id[underscore_index + 1:]
    # Appending cleaned character ID to the units list
    units.append(character_id)
```

This code snippet iterates through each unit in the participant's data, extracts the character ID, and cleans it by removing any prefix before the underscore. The cleaned character IDs are then added to the units list.

## Retrieving Items

To retrieve the items associated with a summoner's units, we follow a similar process. Iterating through the participant's units data, we extract the item names and format them appropriately. Here's how it's done:

```python
items = []

for unit in participant['units']:
    if 'itemNames' in unit:
        item_names_list = unit['itemNames']
        stripped_item_names = []
        for item in item_names_list:
            # Stripping item name
            stripped_item_name = item.split('_', 2)[-1]
            
            # Formatting item name
            formatted_item_name = ' '.join(re.findall(r'\d+|[a-zA-Z][a-z]*', stripped_item_name))
            
            # Appending formatted item name to the list
            stripped_item_names.append(formatted_item_name)
        
        # Appending list of formatted item names to the items list
        items.append(stripped_item_names)
```

This code snippet iterates through each unit in the participant's data and checks if the unit has associated item names. If item names are found, it strips each item name, formats it using regex to separate digits and words, and appends the formatted item names to the items list.

# Function Chaining: Automating Data Retrieval and Formatting

In this section, we chain together a series of functions to automate the process of fetching and formatting data for a summoner's recent matches.

## Automating Match Data Retrieval and Processing

The `automate_process` function orchestrates the retrieval of summoner data, match IDs, and match data. It operates in the following steps:
1. **Fetching Summoner Data**: Utilizes the `get_summoner_data` function to retrieve summoner data using the summoner's name. This data includes the summoner's PUUID (Portable Unique ID).
2. **Fetching Match IDs**: Calls the `get_match_ids` function with the summoner's PUUID to retrieve a list of match IDs corresponding to the summoner's recent matches.
3. **Fetching Match Data**: Iterates through the retrieved match IDs (limited to the last 20 matches) and collects match data for each match ID using the `get_match_data` function.
4. **Extracting Participant Data**: Within each match, identifies the specific participant (the summoner) using their PUUID and retrieves relevant data such as placement, units, traits, and items.

By chaining these functions together, we streamline the process of gathering and presenting relevant data for analysis or display in a Flask application. This approach enhances code modularity, readability, and maintainability.

```python
def automate_process(summoner_name):
    # Fetch summoner data using their name
    summoner_data = get_summoner_data(summoner_name)
    
    # Check if summoner data was successfully retrieved
    if summoner_data:
        # Extract summoner's PUUID
        puuid = summoner_data['puuid']
        
        # Fetch match IDs associated with the summoner's PUUID
        match_ids = get_match_ids(puuid)
        
        # Check if match IDs were successfully retrieved
        if match_ids:
            # Initialize an empty list to store processed match data
            match_data_list = []
            
            # Iterate over a maximum of 20 recent match IDs
            for match_id in match_ids[:20]:
                # Fetch match data for the current match ID
                match_data = get_match_data(match_id)
                
                # Check if match data was successfully retrieved
                if match_data:
                    # Find the participant data for the summoner within the match data
                    participant = next((p for p in match_data['info']['participants'] if p['puuid'] == puuid), None)
                    
                    # Check if participant data was found for the summoner
                    if participant:
                        # Extract and format new augments used by the summoner
                        new_augments = [' '.join(re.findall('[A-Z][^A-Z]*', augment.split('_', 2)[-1])) for augment in participant['augments']]
                        
                        # Extract placement, units, tiers, and items of the summoner
                        placement = participant['placement']
                        units = [unit['character_id'].split('_')[-1] for unit in participant['units']]
                        tiers = [unit.get('tier', None) for unit in participant['units']]
                        items = []
                        for unit in participant['units'][:14]:
                            if 'itemNames' in unit:
                                item_names_list = unit['itemNames']
                                stripped_item_names = []
                                for item in item_names_list:
                                    stripped_item_name = item.split('_', 2)[-1]
                                    formatted_item_name = ' '.join(re.findall(r'\d+|[a-zA-Z][a-z]*', stripped_item_name))
                                    stripped_item_names.append(formatted_item_name)
                                items.append(stripped_item_names)
                        
                        # Extract active traits and their tiers
                        active_traits = []
                        trait_tiers = []
                        for trait in participant['traits']:
                            if trait.get('tier_current', 0) > 0:
                                trait_name = trait['name']
                                stripped_trait_name = trait_name.split('_')[-1]
                                active_traits.append(stripped_trait_name)
                                trait_tiers.append(trait['tier_current'])
                        
                        # Append processed data to the list of match data
                        match_data_list.append({
                            'new_augments': new_augments,
                            'placement': placement,
                            'units': units,
                            'tiers': tiers,
                            'items': items,
                            'active_traits': active_traits,
                            'trait_tiers': trait_tiers
                        })
```

## Format Output

The `format_output` function takes the processed match data and formats it into a readable output. It performs the following tasks:
1. **Formatting Match Details**: Constructs a formatted string containing details such as summoner name, match ID, placement, and used augments.
2. **Formatting Active Traits**: Extracts active traits and their respective tiers, then formats them into a readable list.
3. **Formatting Units and Items**: Formats information about the units controlled by the summoner, including their tiers and equipped items.

```python
def format_output(result, summoner_name, match_id):
    # Check if the result dictionary is not empty
    if result:
        # Replace '%20' in summoner's name with a space for formatting
        summoner_name_formatted = summoner_name.replace('%20', ' ')
        
        # Join new augments into a single string separated by commas
        new_augments = ', '.join(result['new_augments'])
        
        # Retrieve summoner's placement in the match
        placement = result['placement']
        
        # Retrieve lists of units and their respective tiers
        units = result['units']
        tiers = result['tiers']
        
        # Retrieve lists of items equipped by summoner's units
        items = result['items']
        
        # Retrieve lists of active traits and their respective tiers
        active_traits = result['active_traits']
        trait_tiers = result['trait_tiers']
        
        # Calculate the total number of items equipped by summoner's units
        num_items = sum(len(items) for items in result['items'])
        
        # Construct the initial part of the formatted output string
        formatted_output = f"{summoner_name_formatted} in game with match_id {match_id} placed {formatted_placement} using {new_augments} augments.\n"
        
        # Sort the active traits in descending order based on their tiers
        sorted_active_traits = [trait for _, trait in sorted(zip(trait_tiers, active_traits), reverse=True)]
        
        # Append the formatted active traits to the output string
        formatted_output += "Active Traits: " + ', '.join(f"{trait} (Tier {tier})" for trait, tier in zip(sorted_active_traits, sorted(trait_tiers, reverse=True))) + "\n"
        
        # Iterate over each unit and its tier, and append the formatted unit information to the output string
        for i, (unit, tier) in enumerate(zip(units, tiers)):
            champion = unit
            # Retrieve the list of items equipped by the unit, or an empty list if no items
            item_list = items[i] if i < len(items) else []
            formatted_output += f"Champion {champion} (Tier {tier}) equipped with items: {', '.join(item_list)}\n"
        
        # Return the formatted output string containing information about the summoner's performance in the match
        return formatted_output
```

# Flask Application: Visualizing Summoner Match Data

This Flask application serves as a tool for visualizing match data for a given summoner in the game. The application allows users to input a summoner name, retrieves their match data, and presents it in a visually appealing format.

```python
app = Flask(__name__)
```

Here, we initialize a Flask application instance.

```python
@app.route('/')
def index():
    return render_template('index.html')
```

This route handles requests to the root URL and renders the index.html template, which contains a form for submitting summoner names.

```python
@app.route('/submit_summoner_name', methods=['POST'])
def submit_summoner_name():
    summoner_name = request.form.get('summoner_name').replace(' ', '%20')
    #This route handles form submissions, retrieves the summoner name entered by the user, and replaces spaces with %20 to format it appropriately for the Riot Games API.
    match_data_list = automate_process(summoner_name) # The automate_process function retrieves match data for the specified summoner.
    #If match data is successfully retrieved, the application calculates the average placement of the summoner and generates HTML to display the match data. This HTML is then rendered using the formatted_output.html template.
    if match_data_list:
        average_placement = calculate_average_placement(match_data_list)
        formatted_output = generate_match_data_html(match_data_list)
        return render_template('formatted_output.html', formatted_output=formatted_output, average_placement=average_placement, summoner_name=summoner_name.replace('%20', ' '))
    else:
        return "Error: Summoner data not found."

def calculate_average_placement(match_data_list): # This function calculates the average placement of the summoner across multiple matches.
    total_placement = sum(match_data['placement'] for match_data in match_data_list)
    return total_placement / len(match_data_list) if len(match_data_list) > 0 else 0

#This function generates HTML to display the match data, including placement and images of champions and their equipped items.
def generate_match_data_html(match_data_list):
    output = ''
    for i in range(0, len(match_data_list), 2):
        output += '<div style="margin-bottom: 20px; display: flex; justify-content: space-between;">'
        for match_data in match_data_list[i:i+2]:
            output += '<div style="width: 48%; margin-left: 60px;">'  # Set width to 48% and add left margin
            output += f'<p>Placement: {match_data["placement"]}</p>'
            output += generate_champion_image_tags(match_data['units'], match_data['items'])
            output += '</div>'
        output += '</div>'
    return output

def generate_champion_image_tags(units, items):
    output = '<div style="display: flex; flex-wrap: wrap; justify-content: left;">'
    for champion, champion_items in zip(units, items):
        image_path = champion_images.get(champion)
        if image_path:
            # Generate HTML for champion icon
            image_tag = f'<img src="{image_path}" alt="{champion}" height="50" width="50" style="margin-right: 0px;">'
            # Generate HTML for item images
            item_tags = ''.join([f'<img src="{item_images.get(item)}" alt="{item}" height="20" width="20" style="width: 16.66px; flex-grow: 0;">' for item in champion_items])
            # Concatenate champion icon HTML and item images HTML within a flex container
            output += f'<div style="display: flex; flex-direction: column; align-items: center;">{image_tag}<div style="display: flex; width: 50px; justify-content: center;">{item_tags}</div></div>'
    output += '</div>'
    return output

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
#This block of code ensures that the Flask application runs when the script is executed directly, with debugging enabled for development purposes.
```

# Welcome to My Flask Application

You can input a summoner name, and the application will fetch and display various statistics and information about that summoner's recent matches.

## How to Use

1. **Enter the summoner name in the input field below.**
2. **Click on the "Submit" button to retrieve and display the data.**

## Index Main Body

```html
<body>
    <form action="/submit_summoner_name" method="POST">
        <label for="summoner_name" style="text-align: center;">Summoner Name:</label>
        <input type="text" id="summoner_name" name="summoner_name" required>
        <input type="submit" value="Submit">
    </form>
</body>
```

This HTML code represents the main body of the application's interface. It includes a form where you can input the summoner name and a submit button to trigger the retrieval of data from the backend server.

## Match History Page

On this page, you can view the match history for the summoner "{{ summoner_name }}" along with some additional information.

### Header

```html
<div class="header">
    <h1>{{ summoner_name }} Match History</h1>
    <p>Average Placement: {{ average_placement }}</p>
</div>
```

The header section displays the summoner's name and their average placement in matches.

### Match History

```html
{{ formatted_output | safe }}
```

This section displays the formatted match history data retrieved from the backend server. It includes details such as placement, champion images, and equipped items for each match.