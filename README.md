# INSTALLING:
The following things should be done in the project root directory.
1. Run pip install -r requirements.txt (NOTE! Make sure to include the -r)
2. Run python3 generatesecretkey.py
    * The script will generate a new secret key and save it in a file called .env
3. Run python3 manage.py makemigrations
4. Run python3 manage.py migrate
5. Run python3 manage.py runserver
    * You can now access the app by navigating to localhost:8000 in your browser
6. Create a superuser using Linux: 
    * Run python3 manage.py createsuperuser and provide credentials
7. Create a normal user using the sign up page:
    * Run python3 manage.py runserver
    * Navigate to localhost:8000 in your browser and click the ‘Sign up’ link
    * Provide a username, email, and password for your user and click ‘Sign up’. Note that the default implementation does not require a good username or password!
8. In addition, you should also add some move objects to the project database. This can be done by navigating to localhost:8000/moves/addmove

# FLAW 1: INSECURE DESIGN
* Flaw and fix:
  * https://github.com/ylireetta/csbproject/blob/master/csbproject/settings.py#L137

The first flaw can be found from the settings.py file of the project. If a user has logged in and navigates to a different site or even closes the browser completely, their session on the project site does not end. This means that anyone who has access to the same computer that the “victim” has used also has access to the project site and can operate in the system with the victim’s authority.

This flaw can be fixed by simply adding a boolean value to the project’s settings.py file – SESSION_EXPIRE_AT_BROWSER_CLOSE = True. By adding this, the user session will end when the browser window is closed. However, if the user simply leaves the site and continues to use the same browser window, the sessions is not terminated. The fix has been commented out as of now, but it can easily be implemented by removing the line comment on line 137.


# FLAW 2: BROKEN ACCESS CONTROL
* Rename this method:
https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L52
* Remove or rename this method:
https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L79
* Remove the flawed form and use this instead:
https://github.com/ylireetta/csbproject/blob/master/moves/templates/moves/searchsessions.html#L29
* Remove comments to check admin status:
https://github.com/ylireetta/csbproject/blob/master/moves/templates/moves/searchsessions.html#L40
* Remove the flawed implementation:
https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L161
* Remove line comment to use the fixed method instead:
https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L157

The second flaw can be found in the view where a user can search for sessions completed on a specific date. When the user clicks the ‘Search’ button, a GET request is sent with GET parameters included in the url. If we inspect the url in the browser after a completed search, we can see that there is an interesting parameter called ‘admin’ whose value is either 0 or 1. If admin=1, the user is given a delete link with each session that matches the query. So by manipulating the GET request url, a user with no admin authority gains access to delete links that can be used to delete other users’ sessions from the database. However, the delete function is not secure even if an unauthorized user does not have access to direct links. Anyone can simply type the delete link to their browser and delete other users’ sessions this way.

This flaw can be fixed by using a POST request instead of GET when searching for data with forms. When POSTing a request, the url does not change and the parameters are not visible to the user. The posted data can still be tampered with, but not as easily as with GET requests. The search forms in searchsessions.html should be modified so that the form method is POST. It is unnecessary to send info about whether the user is admin or not to the server, because this can easily be checked in the template itself by using Django’s magic. The fixes have been commented out in searchsessions.html on lines 19—23 and 30–32, so to fix the flaw:
1) rename the searchSessionsViewToRename to searchSessionsView on line 52 of views.py.
2) rename the flawed searchSessionsView on line 79 of views.py to something else or remove it completely.
3) remove comments around the fixed elements on lines 30–33 and 41–43 in searchsessions.html template.
4) remove the flawed elements in searchsessions.html on lines 19–27 and 47—50.
5) remove the flawed deleting functionality on lines 158-161 and remove the line comment on line 157 to call the secure delete method in views.py.


# FLAW 3: IDENTIFICATION AND AUTHENTICATION FAILURES
* Flaw:
  * https://github.com/ylireetta/csbproject/blob/master/templates/signup.html#L33
* Fix:
  * https://github.com/ylireetta/csbproject/blob/master/templates/signup.html#L25
  * https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L224
  * https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L234


The third flaw lies on the sign up page. The flawed form does not require anything special from the username or password – i.e. you can register a new user called ‘admin’ whose password is ‘admin’, or the password can simply be ‘password’.

This flaw can be fixed by using Django’s user creation form, which automatically instructs the user to come up with a good username and password. If the data is deemed invalid, the user will be redirected to the sign up page and given an error message. Remove all line comments starting from line 235 in views.py. Remove the flawed code on lines 225-232 of views.py. Finally, in signup.html, remove the flawed form on lines 34-45 and remove comments around the fixed form on lines 26-30.


# FLAW 4: INJECTION
* Flaw:
  * https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L206
* Fix:
  * https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L208
* Alternate fix:
  * https://github.com/ylireetta/csbproject/blob/master/static/styles.css#L73


The fourth security flaw in the project is that users can make raw SQL queries to the database in the Search for sessions view. The query string uses placeholders, which means that an attacker can use e.g. UNION SELECT queries to access tables other than the one specified in the code (i.e., the table that hold the Move objects). For example, if the attacker types the following string to the search box 1=1’ UNION SELECT id, username FROM auth_user’ they get the Ids and usernames of all users in the system database. This functionality can be tested by making queries to the following tables: movestable, sessionstable, setstable, auth_user.

This flaw can be fixed by not making raw SQL queries to the database. Queries can easily be made using Django’s models. The fixed method can be taken into use by 1) removing the line comment on line 208, and 2) commenting out or removing line 210 in views.py.

There is also another fix available: change the display style of the live search input and result div from none to block on line 73 of styles.css.

# FLAW 5: CROSS SITE REQUEST FORGERY
* Flaw and fix:
  * https://github.com/ylireetta/csbproject/blob/master/moves/views.py#L110
  * https://github.com/ylireetta/csbproject/blob/master/moves/templates/moves/addsession.html#L16

The fifth flaw of this project is that some of the views use the @csrf_exempt decorator, which makes the system vulnerable to Cross Site Request Forgery. The flawed code does not require CSRF tokens to be posted to addSessionView.

To fix this flaw, remove the @csrf_exempt decorator in views.py on line 110. Also make sure to include the {% csrf_token %} in the addsession.html template on line 16 when posting data. The token has been included in the fixed implementations but it is commented out as default.
