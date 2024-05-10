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

