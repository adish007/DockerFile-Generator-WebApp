# Automatic Dockerfile Generator with ChatGPT API

This project provides a WebApp that automates the generation of Dockerfiles using a fine-tuned OpenAI model. It analyzes the structure of your repository, identifies dependency files, and generates tailored Dockerfiles based on the provided information.

## Features

- **WebApp Interface:** A user-friendly interface to interact with the application.
- **Automatic Dependency Analysis:** Scans the repository for files like `requirements.txt`, `package.json`, and others to determine the dependencies.
- **ChatGPT Integration:** Leverages a custom-trained OpenAI model trained on existing Dockerfile data to generate Dockerfiles better suited for the repository.


**Here is a video link showcasing the example:**

https://drive.google.com/file/d/1GBKYl9iqcgeKPIXyrakD71OQAoveNoh8/view?usp=sharing
---

## Prerequisites

1. Python 3.7 or higher.
2. A valid OpenAI API key.
3. Javascript

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set the OpenAI API key:**
   Export your OpenAI API key to the environment variable:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

---

## Usage

1. **Run the WebApp:**
   Execute the `main.py` file to start the application:
   ```bash
   python main.py
   ```

2. **Access the WebApp:**
   Open your browser and go to the following address:
   ```
   http://127.0.0.1:5000
   ```

3. **Generate Dockerfile:**
   - Upload your repository or point to a GitHub repository.
   - The application will scan your repository for dependency files such as:
     - `requirements.txt` for Python
     - `package.json` for Node.js
     - Any other recognized dependency file types
   - If dependency files are found, they are sent via API to the fine-tuned OpenAI model to generate a Dockerfile.
   - If no dependency files are found, the application will return a Dockerfile.

---

## How It Works

1. **Repository Analysis:**
   - The application scans the repository’s root directory for dependency files.
   - Files like `requirements.txt`, `package.json`, and other relevant files are parsed to extract necessary information.

2. **Dockerfile Generation:**
   - The extracted dependency data is sent to the OpenAI API using a fine-tuned model.
   - The model generates a Dockerfile optimized for the detected dependencies and project structure.

3. **WebApp Interface:**
   - Provides a clean and intuitive interface for users to upload repositories and view generated Dockerfiles.

---




