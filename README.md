## Django-Postgis Application

This is a Django-based application that allows you to perform CRUD operations on places, as well as find the nearest place. The application utilizes PostgreSQL with PostGIS extension for spatial database functionality. Docker Compose is used to simplify the deployment process.

### API Documentation
The API documentation for this application is available through Swagger. After running the application, you can access the Swagger documentation at http://localhost:8000/swagger/. Swagger provides a user-friendly interface to explore and interact with the API endpoints.

### Installation using Docker

<p>Before you begin, make sure you have Docker installed on your computer. To do this, run the following command:</p>

```shell
docker --version
```

<p>The result of the execution should be the docker version. If it is not, install docker on your computer, if everything is ok, follow these steps:</p>

1. Clone the project repository to your computer using the following command:
    ```shell
    git clone https://github.com/bihunva/django-postgis-api.git
    ```

2. Add the <strong>.env</strong> file to the root of the project. In this file you must specify the values of the
   environment variables, an example is in the file <strong>.env.sample</strong>.


3. Build Docker images by running the following command:
   ```shell
   docker-compose build
   ```

4. Run Docker containers by running the following command:
   ```shell
   docker-compose up
   ```

5. Once the containers are up and running, you can access the application in your web browser at http://localhost:8000.
