# Build a RESTful API - endpoints require role-based authorization with JWT gathered from Auth0 user

Third piece of coursework in the [Udacity Full Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004): Identity and Authentication Management

The goal of the project was to build a simple API with endpoints which would require a valid JWT be passed to it containing a valid user permission. We were to use a single-page application setup in Auth0 to handle the user login and JWT creation and validation process.

Project tasks completed:
1. Build RESTful API using Python, Flask & SQLAlchemy, containing GET, POST, PATCH and DELETE requests which respond to different permissions provided by the JWT.
2. Setup Single-Page Application in Auth0. Add Permissions, Roles and Users.
3. Setup authentication decorator method to get the auth header, check permissions and verify the Json Web Token
4. Use Postman to create a collection of test cases for each API endpoint and appropriate error handlers.
5. Deploy and test Ionic frontend
