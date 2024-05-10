#!/usr/bin/env python
# coding: utf-8

# In[228]:


def automate_process(summoner_name):
    summoner_data = get_summoner_data(summoner_name)
    if summoner_data:
        puuid = summoner_data['puuid']
        match_ids = get_match_ids(puuid)
        if match_ids:
            match_data_list = []
            for match_id in match_ids[:20]:  # Fetch data for the last 20 matches
                match_data = get_match_data(match_id)
                if match_data:
                    participant = next((p for p in match_data['info']['participants'] if p['puuid'] == puuid), None)
                    if participant:
                        new_augments = [' '.join(re.findall('[A-Z][^A-Z]*', augment.split('_', 2)[-1])) for augment in participant['augments']]
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

                        match_data_list.append({
                            'new_augments': new_augments,
                            'placement': placement,
                            'units': units,
                            'tiers': tiers,
                            'items': items,
                            'active_traits': active_traits,
                            'trait_tiers': trait_tiers
                        })
                    # Some debugging code
                    else:
                        print("Participant data not found for match ID:", match_id)
                else:
                    print("Match data not found for match ID:", match_id)
            return match_data_list
        else:
            print("Match IDs not found for summoner:", summoner_name)
            return None
    else:
        print("Summoner data not found for summoner:", summoner_name)
        return None


# In[125]:


from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_summoner_name', methods=['POST'])
def submit_summoner_name():
    summoner_name = request.form['summoner_name']
    result = automate_process(summoner_name)
    if result:
        units = result['units']
        items = result['items']
        formatted_output = generate_champion_image_tags(units, items)
        return render_template('formatted_output.html', formatted_output=formatted_output)
    else:
        return "Error: Summoner data not found."

def generate_champion_image_tags(units, items):
    output = '<div style="display: flex; flex-wrap: wrap; justify-content: left;">'
    for champion, champion_items in zip(units, items):
        image_path = champion_images.get(champion)
        if image_path:
            # Generate HTML for champion icon
            image_tag = f'<img src="{image_path}" alt="{champion}" height="50" width="50" style="margin-right: 0px;">'
            # Generate HTML for item images
            item_tags = ''.join([f'<img src="{item_images.get(item)}" alt="{item}" height="20" width="20" style="width: 16.66px; flex-grow: 1;">' for item in champion_items])
            # Concatenate champion icon HTML and item images HTML within a flex container
            output += f'<div style="display: flex; flex-direction: column; align-items: center;">{image_tag}<div style="display: flex; width: 50px; justify-content: center;">{item_tags}</div></div>'
    output += '</div>'
    return output


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

