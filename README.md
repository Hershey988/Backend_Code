# webapp2 sample

This sample code creates a basic webapp2 server with three end-points.

* `MainPage` referes to the page launched at base URL
* `GetListPage` refers to end-point `get_list`
* `SendMsgPage` refers to end-point `send_msg`

## Code Structure

There is only one Python file required for this server code. The code is in file main.py

* Each page is described by a class which inherits RequestHandler class from 
webapp2 For eg.: `class GetListPage(webapp2.RequestHandler):`
* End point for this class is defined in the `app` object by adding `('/get_list', GetListPage)`
to the list.
* Each end-point needs to create a `get` or `post` function for GET and POST requests respectively.
* In these functions, the request and response objects for the call can be accessed as members of the
class itself.
* For accessing datastore, a class inheriting `ndb.Model` is created that allows us to define fields
of type provided by NDB. In this code, this class is: `class Message(ndb.Model)`
* In order to add an entry to the datastore, an object of this class is to be created and then 
the `put` method on it to store the data.

## Deployment

* File app.yaml is provided for using the app with Google cloud.
* For local deployment, run 
    ```
     dev_appserver.py app.yaml
     ```
* For hosting on Google cloud, create a project on Google cloud, initialize SDK, and then run
    ```
     gcloud app deploy app.yaml
     ```
     
## Example Deployment

An example deployment of this code is hosted on [https://cmps121-webapp.appspot.com](https://cmps121-webapp.appspot.com)