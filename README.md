# Flask-based-RESTful-Riot-API-Wrapper
Flask application that integrates with Riot's RESTful API to retrieve the match history of the last 20 games. This application leverages function chaining, API requests, and intermediate JSON indexing to provide comprehensive data, including champion icons and items used in each match.

# Project Structure

- project/
  - api-data-retrieval/
    - get-summoner-data.py
    - get-match-data.py
    - get_match-ids-data-recursive
  - data_processing/
    - index-data.py
    - parsing-data.py
  - flask-app/
    - app.py
    - templates/
      - index.html
    - static/
      - style.css
- README.md

# Project Overview

## Interface
![Interface](./img/interface.png)

## Result
![Result](./img/result.png)