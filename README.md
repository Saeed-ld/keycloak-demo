# Keycloak Access Control Project

This project demonstrates user authentication and role-based access control using Keycloak and Flask.

Users are assigned to groups, and each group has its own role. The Flask application checks the roles in the Keycloak access token before allowing access to different pages.

## Running Keycloak

Load the provided Docker image:

```bash
docker load -i keycloak-image.tar
```

Start the container:

```bash
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD=Admin12345 \
  quay.io/keycloak/keycloak:latest \
  start-dev
```

Keycloak will be available at:

`http://localhost:8080`

## Running the Flask application

Install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

The application will run at `http://localhost:8081`.

## Test endpoints

- `/engineering` – requires the `engineering-access` role.
- `/finance` – requires the `finance-access` role.

Both endpoints require a valid Keycloak access token.
