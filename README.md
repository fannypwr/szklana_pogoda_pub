-FLOW

    -- Registration:
            - very simple registration process (can be changed if necessary)
            - no mails (activation mails with token or any other mails)
            - automatic activation of the account (role id and active status are assigned to the user automatically)
            - no nicknames/ usernames, email serves as login

    -- Looking up data

    -- Displaying data




-API:



        -- Resources and endpoints:
        - Temperature (no authentication requested, it can be done with a decorator and depending upon a role of a user):
        *api/temperatures/places/place_id - all the temperatures for a given place. place_id == 0 --> all the temperatures
        are displayed GET
        *api/temperatures/temperature_id - endpoint to get a given temperature object GET
        *api/temperatures/ - creating new temperature objects POST. Please note what date formats are accepted (models.py,
        Temperature, from_json, date_regex)

        - Place
        *api/places/ - list of all places (GET) or create new place (POST)
        *api/places/place_id - info regarding a given place (GET)
        - User
        *api/users/ (GET) all users
        *api/users/user_id (GET) a given user
        *api/users/ (POST) - adding a new user
        - Role - not implemented



#TODO
- styles



- I18N
- tests


