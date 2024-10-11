# EpiRecipeSearch Backend

## Project Description

The **EpiRecipeSearch Backend** is built using Flask, serving as the API for the EpiRecipeSearch application. It allows users to search for recipes, retrieve specific recipe details, filter recipes based on various criteria, and fetch recipe images using the Pexels API. The backend also integrates with OpenSearch for efficient search and retrieval of recipe data.

## Objectives

- Provide RESTful API endpoints for searching, filtering, and retrieving recipe details.
- Integrate with OpenSearch for indexing and searching recipes.
- Use the Pexels API to retrieve relevant images for recipes.
- Support CORS for seamless communication with the React frontend.

---

## Table of Contents

- [Project Description]
- [Objectives]
- [Technologies and Frameworks]
- [Setup and Installation]
- [Usage Guidelines]


---

## Technologies and Frameworks

- **Flask**: A lightweight web framework for creating the backend API.
- **OpenSearch**: For indexing and searching recipe data.
- **Pexels API**: For fetching images related to the recipes.
- **Flask-CORS**: To enable Cross-Origin Resource Sharing (CORS) for requests from the frontend.
- **Requests**: For making HTTP requests to external APIs (Pexels).
- **dotenv**: For managing environment variables.

---

## Setup and Installation

### Prerequisites

- **Python 3.x** (You can download it from [here](https://www.python.org/))
- **Flask** (Install via pip)
- **OpenSearch** (You can install or use OpenSearch as a service locally or in the cloud)
- **Pexels API Key** (Get one from [Pexels Developer](https://www.pexels.com/api/))

### Steps to Setup the Backend

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Kajal2209/EpiRecipeSearch-Backend.git
    cd EpiRecipeSearch-Backend
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the project root with the following content:
    ```bash
    PEXELS_API_KEY=<your_pexels_api_key>
    OPENSEARCH_HOST=localhost
    OPENSEARCH_PORT=9200
    ```

5. **Ensure OpenSearch is Running**:
   If OpenSearch is not running, start it on your local machine or ensure that your cloud instance is accessible. 

6. **Run the Flask Application**:
    ```bash
    flask run
    ```

    The backend should now be running on `  `.

---

## Usage Guidelines

### Running the Server

After completing the setup, you can start the Flask development server using the command:

```bash
python app.py


