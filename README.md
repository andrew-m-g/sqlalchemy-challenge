# sqlalchemy-challenge
#code sources
    #Tutor
    #ChatGPT
    #Class Files and materials from gitlab
climate_starter.ipynb
    used to query the hawaii.sqllite file located in the 'Resources' folder and extract data relevant to the number of weather stations, precipitation levels, temprature records in order to generate graphs to visually presented the queried data


app.py
    used to host a Flask api
    generates a number of routes, each of which have utilize sqlalchemy queries to extract data from the hawaii.sqllite file in order to produce an api that displays the queried data on the users web browser
        generates a route that alters the displayed results based on user input in the url