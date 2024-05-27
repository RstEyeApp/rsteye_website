# RstEyeApp

RstEyeApp is an application designed to promote digital and mental well-being during computer usage.

## Using

Access the application at [http://13.201.70.105/](http://13.201.70.105/).

## Development

To set up the development environment:

    1. Create a virtual environment:
        python3 -m venv .venv

    2. Install required packages:
        python3 -m pip install -r requirements.txt

    3. Run the server:
        python3 server.py


## Deployment on AWS EC2

    To deploy the code on AWS EC2:

    1. SSH into the EC2 instance:
        sudo ssh -i <file.pem> ec2-user@<public_ip>

    2. Follow the development steps mentioned above, and then:

    3. Run the Gunicorn server with the provided configuration:
        gunicorn -c gunicorn_config.py server