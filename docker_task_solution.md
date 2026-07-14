# OUTPUT of `docker ps`

```
(venv) PS C:\Internship\food-delivery-updated> docker ps
CONTAINER ID   IMAGE                              COMMAND                  CREATED          STATUS         PORTS                    NAMES
330b246b7c28   food-delivery-updated-django-web   "python manage.py ru…"   2 minutes ago    Up 2 minutes   0.0.0.0:8000->8000/tcp   django-docker
f19e990a13d1   postgres:17                        "docker-entrypoint.s…"   15 minutes ago   Up 2 minutes   0.0.0.0:5432->5432/tcp   food-delivery-updated-db-1
```

# OUTPUT of `docker images`

```
(venv) PS C:\Internship\food-delivery-updated> docker images
REPOSITORY                         TAG       IMAGE ID       CREATED         SIZE
django-docker                      latest    29df72691340   6 minutes ago   1.41GB
food-delivery-updated-django-web   latest    2f41f0c0ebf8   6 minutes ago   1.41GB
postgres                           17        a931c7282521   11 hours ago    454MB
postgres                           16        4d79c308564d   7 months ago    451MB
minio/minio                        latest    69b2ec208575   8 months ago    175MB
dpage/pgadmin4                     latest    ca58f4842a04   8 months ago    532MB
```

# OUTPUT of `docker compose ps`

```
(venv) PS C:\Internship\food-delivery-updated> docker compose ps
NAME                         IMAGE                              COMMAND                  SERVICE      CREATED          STATUS         PORTS
django-docker                food-delivery-updated-django-web   "python manage.py ru…"   django-web   4 minutes ago    Up 4 minutes   0.0.0.0:8000->8000/tcp
food-delivery-updated-db-1   postgres:17                        "docker-entrypoint.s…"   db           17 minutes ago   Up 4 minutes   0.0.0.0:5432->5432/tcp
```
