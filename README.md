# API_BackEnd

Before start, you need to create file .env and copy all from .env_example

1. Go to your project folder and use command "docker-compose -f docker-compose_dev.yml up --build"
2. To remove data from database you need to run "docker-compose -f docker-compose_dev.yml rm" that command 
remove containers. Then use 1 step.

Usage

    The Swagger is accessible at http://localhost:80 Use next credentials user admin, password admin.
    PGAdmin is accessible at http://localhost:7777/.
    Redis Commander is accessible at http://localhost:8081/.
    Flower (Celery monitoring tool) is accessible at http://localhost:8082/.

Shutdown

    To stop running containers and remove them:

docker-compose down

Accessing the Application

    The Django application is accessible at http://localhost:80/
    The Redis Commander can be accessed at http://localhost:8081/
    Flower (the Celery monitoring tool) is accessible at http://localhost:8082/
    The PostgreSQL database can be accessed on localhost with port 5432
    The PGAdmin tool can be accessed at http://localhost:3333/


delete all containers and images

docker-compose -f docker-compose_dev.yml down --rmi all --volumes

    To stop running containers and remove them but keep images:

docker-compose -f docker-compose_dev.yml down --rmi local

