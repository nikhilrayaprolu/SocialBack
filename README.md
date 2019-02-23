# SocialBack
Django Application for social Wall

### Contributing
While contributing make a new branch in the same repository and push the new branch to the origin. Then make a pull request for the branch made to the master.

### Folder Structure
- The Django app is contained in `socialbackmain/socialbackmain`
- The models are structured in `SocialBack/apps/api/models` according to the given UML.
- This UML is not strictly followed
![UML](UML.png)

### Running the server
- Clone the repo: `git clone "https://github.com/YoungSphere/SocialBack.git"`
- Create virtual environment using virtualenv and install the requirements: `pip install -r requirements.txt`
- Run `python manage.py migrate`
- Run `python manage.py createsuperuser` to create a new admin. Fill in the prompts next for admin creation.
- Run `python manage.py loaddata testdata.json` to load dummy data into server
- Run `npm install` to install frontend requirements
- Run `npm run start` to compile the react application, this creates `dist`
in `assets` directory which will be used by django templates to display the react components
- Or you can run `npm run watch` which autocompiles for each change in the frontend.
- Run `python manage.py runserver` to run the server on `127.0.0.1:8000/`
- Go to `127.0.0.1:8000/admin` and login to access admin page. You can check out models and related fields here.

### Heroku deployment
- Staging app deployed to [https://socialback-stage.herokuapp.com/](https://socialback-stage.herokuapp.com/).
- Production app deployed to [https://youngspheresocialback.herokuapp.com/](https://youngspheresocialback.herokuapp.com/).
- Admin created with username `admin` and password `admin123`.
- Auto-deployment for staging enabled.
- Review apps enabled for reviewing pull requests.

###JWT-Authentication
-JWT-Authentication implemented.
-The frontend will request from the url('http://127.0.0.1:8000/api-token-auth/') using post method only and give a JSON object of format :-
{
    "username": "",
    "password": ""
}
-The response will be a JSON object of the form ({"token":"tokenvalue"}) and of the form:- 
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}  if the given username and password do not exist.

###Reference:
- https://medium.com/labcodes/configuring-django-with-react-4c599d1eae63
- https://owais.lone.pw/blog/webpack-plus-reactjs-and-django/ 
- https://edx-document.readthedocs.io/en/latest/user_interface_development.html
