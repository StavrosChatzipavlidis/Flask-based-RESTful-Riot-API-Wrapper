#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_summoner_name', methods=['POST'])
def submit_summoner_name():
    summoner_name = request.form.get('summoner_name').replace(' ', '%20')
    match_data_list = automate_process(summoner_name)
    if match_data_list:
        average_placement = calculate_average_placement(match_data_list)
        formatted_output = generate_match_data_html(match_data_list)
        return render_template('formatted_output.html', formatted_output=formatted_output, average_placement=average_placement, summoner_name=summoner_name.replace('%20', ' '))
    else:
        return "Error: Summoner data not found."

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

