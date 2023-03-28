FROM python:3.9-alpine3.13
LABEL maintainer="Hamza Aqeel"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
# what this does is copy our requirements.txt file to tmp/requirements.txt file
# app will contain our django app
# workdir default directory from where our commands our gonna be run from wedont needto specify
# automatic
# 8000 port to connect django
####################
###we keep it false so by default we don't run it in
##development modes
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \ 
    #end of if command,for when the dev mode is on,helps save space and don't have to worry
    #aboit devlopment dependencies when you don't have them installed in your image 
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user
#Runs commandon alpine image we could put run behind all of them instead in a run block
#however that create mutiple image layers
#command 1:people dont find venv necessary however in edge cases some dependencies might
#conflict with base image,it doesnt add any overhead so no harm in it
#cmd2 we upgrade the pip,cmd3&4 we install the requirements file inside the docker image then
#we remove the tmp directory because we dont want unnecessary dependencies,it is best
#practice to kepp docker image as lightweight as possible so remove temp files if you dont 
#need them as is makes deployment quicker,cmd5 add user adds new user in our image it is best
#practice as default user is the root user whcih would be used if we didnt add new user
#the reason for this if app gets compromised the other side gets access to root user with
#full priveleges,cmd5i we dont want to login and get straight in and no home to keep app
#lightweight as possible,django-user is name of user can be anything,cmd6 updates  the
#path environemnt var in the image.Is the directory where the executables are run so when
#we run our project so when run any python commands it will run from our virtual env.
#cd6 we run as django-user not as root user
#.dockerignore exclude files docker doesnt need to be concerned with

#############################

# ARG DEV=false
# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     apk add --update --no-cache postgresql-client jpeg-dev && \
#     apk add --update --no-cache --virtual .tmp-build-deps \
#         build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp && \
#     apk del .tmp-build-deps && \
#     adduser \
#         --disabled-password \
#         --no-create-home \
#         django-user && \
#     mkdir -p /vol/web/media && \
#     mkdir -p /vol/web/static && \
#     chown -R django-user:django-user /vol && \
#     chmod -R 755 /vol && \
#     chmod -R +x /scripts

# ENV PATH="/scripts:/py/bin:$PATH"

# USER django-user

# CMD ["run.sh"]


#we have dev require file for when we build image and don't need it to run the project
#we use docker compose because it builds via docker file and tags 
#appropriately
#we will need to configure flake file to stop it from liniting some files as default
#django files have aalot of errors in it so it can cause issues.and app linting to code we
#create only,put it in app not in root otherwise file won't be picked up.
#Most files in .flake8 besides pychache are auto genrated by django
#docker-compose run --rm app sh -c "flake8"
#docker-compose run --rm app sh -c "django-admin startproject app .",have django installed
#in image so will run django with cli  like it would in local machine;. is important so it 
#create in current directory without it it will create in a sub directory inside the app
# from which we will have trouble running our commands.
#we were able to sync due to our volume so anything we create in container is maped to
#our project and anything we create in our project app directory gets mapped to the
#container
#docker-compose up;docker command for starting ourservices and see stuff in browser.

#for .github/workflows/checks.yml file on:push so when we git commit any changes it pushes
#file,for jobs we run test lint id of job so we might need to reference it so we ca run
#jobs in certain order,runs on is runner on which we run our job on e.g os like ubuntu,steps 
#this action is used to login into docker and you can reuse actions,with will pass info into
#docker,checkout to make code available for testing,linting , not done by default since
#alot of actions require no code. 
#docker compose is default in ubuntu runner so no need to install it in image again
