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
- Run `python manage.py runserver` to run the server on `127.0.0.1:8000/`
- Go to `127.0.0.1:8000/admin` and login to access admin page. You can check out models and related fields here.
