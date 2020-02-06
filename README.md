# Penn Labs Server Challenge

## To Run
1. To run this project, first run `$ pipenv install flask-sqlalchemy` to initialize flask-sqlalchemy.
2. Next, run `$ pipenv run python index.py`
3. Demo user has username `jen` and password `P3nnLabs!`, enjoy!

## Features / Functionality
1. Utilize a SQL database for data management and persistent storage.
   - Database contains two tables, a 'clubs' table and a 'users' table for user and club objects.
   - Users table contains a username, hashed password, and list of favorited clubs.
   - Clubs table contains a club name, tags, description, and number of "favorites".
2. Implementation of user sessions
   - User **registration**, **login**, and **logout** features all fully functional and consistent with maintaining unique user sessions.
   - Only users that are logged in are able to 'favorite' a club
3. API Features fully functional
   - [x] `/api/clubs` `GET` Returns a JSON of all of the attributes of every club
   - [x] `/api/clubs` `POST` Allows for the addition of new clubs. Navigate to `localhost:5000/club_form` to test out the submission of a new club with tags via a dynamic form. Click on individual tags to remove them.
   - [x] `/api/user/<username>` `GET` returns a JSON of the specified user
   - [x] `/api/favorite` `POST` allows for a user to favorite a club if not done before. Test this out by logging in and favoriting a club. Try doing so with multiple accounts
4. Scraping
   - All web-scraping functions work, and add unique clubs to the database upon first initialization of the application.
5. Frontend
   - Developed a basic Bootstrap frontend to test functionality: registration, login, logout, club-homepage, favoriting clubs, adding new clubs
6. Modification of user and club objects.
   - While not explicitly written into frontend functionality, through the `modify` function in `db_func.py` a user or club object can have any value (bar the unique ID) modified.
7. Use of JavaScript, JQuery, and AJAX to update values
   - The dynamic club-form requires AJAX and JQuery to send a POST-request to the new club information to the server.
   - Favoriting clubs also uses AJAX POST-request methods.
   - **See the static folder for JS, AJAX, and JQuery files**
