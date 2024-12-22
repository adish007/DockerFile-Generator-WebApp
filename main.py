from flask import Flask, request, render_template, jsonify
import os
import subprocess
import logging
from clone_repo import clone_repo
from process_files import create_prompt_files_folder, DependencyNotFoundError
from generate_dockerfile import generate_dockerfile

app = Flask(__name__)
CLI_FOLDER = "CLI"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/")
def index():
    """
    Render the main web page.
    """
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """
    Handle Dockerfile generation request.
    """
    repo_url = request.form.get("repo_url")
    app.logger.info(f"Received request to generate Dockerfile for: {repo_url}")

    if not repo_url:
        app.logger.error("No GitHub repository URL provided.")
        return jsonify({"error": "GitHub repository URL is required."}), 400

    try:
        app.logger.info(f"Processing repository: {repo_url}")

        # Step 1: Clone the repository
        dest_folder = os.path.join(CLI_FOLDER, "temp_repo")
        clone_repo(repo_url, dest_folder)

        # Step 2: Process files in the repository
        create_prompt_files_folder(repo_url, dest_folder, CLI_FOLDER)

        # Step 3: Generate Dockerfile
        prompt_files_dir = os.path.join(CLI_FOLDER, "prompt_files")
        output_dir = CLI_FOLDER
        generate_dockerfile(prompt_files_dir, output_dir)

        # Read the generated Dockerfile
        dockerfile_path = os.path.join(CLI_FOLDER, "Dockerfile")
        if not os.path.exists(dockerfile_path):
            app.logger.error("Dockerfile was not generated.")
            return jsonify({"error": "Dockerfile was not generated. Please check the repository and try again."}), 500

        with open(dockerfile_path, "r") as file:
            dockerfile_content = file.read()
        app.logger.info(f"Dockerfile generated successfully for: {repo_url}")

        return jsonify({"dockerfile": dockerfile_content})

    except DependencyNotFoundError as e:
        app.logger.error(f"Dependency files missing: {e}")
        return jsonify({"error": str(e)}), 400
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Git clone failed: {e}")
        return jsonify({"error": "Failed to find the repository. Please check the GitHub URL."}), 500
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure the CLI folder exists
    os.makedirs(CLI_FOLDER, exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
