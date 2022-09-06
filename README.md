# Team 4 Cool Finland Materials Delivery Scheduling System (Customer Facing)

### File Structure 

In accordance with Flask, all HTML and Jinja files will be saved in ``` templates/ ``` and rendered with ``` render_template ```. <br>
All Jinja templates are saved with the extension <b>.html.jinja</b>. All CSS and JS files will be saved in ```static/``` folder.

### Database Schematic 

<img src="schema.png">

### Initializing Database

In order to use and interact with the database it has to be initialize. To initialize the database run the ``` init_db.py ``` python script. This will create a database file called ``` database.db ``` if it does not exist. The database only needs to be initialized once.

FOLLOW THIS TO INITIALIZE PROJECT

python -m pip install flask
python -m pip install passlib
python -m pip install bcrypt
$env:FLASK_APP="main.py"
python -m flask run

