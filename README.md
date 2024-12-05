# AuraPura_chatbot_api

AuraPura_chatbot_api is an API for a LangChain-based chatbot designed to provide tailored responses to users based on their emotional states, such as anxiety, depression, and stress. The API integrates Gemini's response-generation capabilities and aims to support users emotionally and enhance their well-being.

## Key Features

- **Emotionally Tailored Responses**: Generates specific responses based on the user's emotional input.
- **Gemini API Integration**: Leverages Gemini's capabilities through LangChain to create meaningful interactions.
- **Support for Key Emotional States**: Anxiety, depression, and stress.
- **Extendable**: Easily extendable to support additional emotional states or features.
- **Dockerized**: Simplified deployment with Docker and Docker Compose.

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose installed on your machine

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Install Dependencies

Install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Set up your environment variables for the Gemini API and other configurations:

- Create a `.env` file in the root directory.
- Add your environment variables:

```env
GEMINI_API_KEY=your_api_key_here
```

### Step 4: Run the API Using Uvicorn
Run the API using uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## Docker Instructions

### Step 1: Build and Run Using docker-compose.yml

Ensure the docker-compose.yml file is in the root directory. Here’s an example:

```yaml
version: '3.8'

services:
  aurapura_chatbot_api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    env_file:
      - .env
```
### Step 2: Build and run the Docker container:

```bash
docker-compose up --build
```
---

## Usage
### Base URL
The API is accessible via the base URL:

```
http://<your-server-address>:8080
```

### Endpoint: /chat

#### Request Example

```bash
curl -X 'POST' \
  'http://<your-server-address>:8080/chat/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'user_input=I%20am%20not%20ok&depression=100&anxiety=0&stress=0'
```

#### Response Example

```json
{
  "response": "I hear you. It sounds like you're going through something really tough right now. I'm here to listen, without judgment. Just know that you're not alone, and even though it feels overwhelming right now, feelings do change. I'm here for you."
}
```
---

## File Structure
- `main.py`: Contains the core logic and routes for the API.
- `requirements.txt`: Specifies Python dependencies for the project.
- `Dockerfile`: Used to containerize the application for deployment.
- `.gitignore`: Lists files and directories to be excluded from version control.
- `docker-compose.yml`: Defines the Docker Compose configuration for building and running the application.
