Clone the repository:

    Make a new folder and open a Git Bash terminal in it
        git clone https://you@bitbucket.org/thrive-memo/mvp.git
    Close the terminal

Set up backend environment:

    In the root directory (testing2) open a PowerShell terminal
    
    Enter
        python -m venv env
    to create the virtual environment
    
    Activate the environment by entering
        .\env\scripts\activate.ps1
    
    Install dependencies:
        pip install -r requirements.txt
        
    Change to myproject directory
        cd myproject
        
    Migrate django models to database
        python manage.py makemigrations myapi
        python manage.py migrate

    Create admin user for database
        python manage.py createsuperuser
    (no need for email, just pick a username/pword you can remember)
    
    To run server
        python manage.py runserver
        
Backend admin GUI will by default be available at localhost:8000/admin

Set up frontend environment:

    In the myproject/frontend directory open another PowerShell terminal
    
    Install dependencies
        npm install
        
    To run development server
        npm run serve
