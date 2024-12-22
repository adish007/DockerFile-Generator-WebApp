import os
from openai import OpenAI
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Init OpenAI API client
client = OpenAI()

def read_file(file_path):
    """
    Reads the content of a file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_dockerfile(prompt_files_dir="CLI/prompt_files", output_dir="CLI"):
    """
    Reads the dependency files and GitHub link from 'prompt_files' in the CLI folder,
    sends them to the OpenAI API to generate a Dockerfile, and saves the result.
    """
    if not os.path.exists(prompt_files_dir):
        logging.error(f"Directory '{prompt_files_dir}' not found!")
        return

    # Read dependency files and GitHub link
    dependency_files = [os.path.join(prompt_files_dir, f) for f in os.listdir(prompt_files_dir) if f != "github_link"]
    github_link_file = os.path.join(prompt_files_dir, "github_link")
    if not dependency_files:
        logging.error("No dependency files found in 'prompt_files'.")
        return
    if not os.path.exists(github_link_file):
        logging.error("GitHub link file 'github_link' not found in 'prompt_files'.")
        return

    logging.info(f"Dependency files to process: {dependency_files}")

    dependency_content = ""
    for file_path in dependency_files:
        file_name = os.path.basename(file_path)
        try:
            content = read_file(file_path)
            dependency_content += f"\n### {file_name} ###\n{content}\n"
            logging.info(f"Read content from {file_path}")
        except Exception as e:
            logging.error(f"Failed to read {file_path}: {e}")

    try:
        github_link = read_file(github_link_file).strip()
        logging.info(f"Read GitHub link: {github_link}")
    except Exception as e:
        logging.error(f"Failed to read GitHub link file: {e}")
        return

    # Prepare API request
    messages = [
        {
            "role": "system",
            "content": "You are an expert in creating Dockerfiles based on dependency files and the structure of the repository. Your goal is to analyze the dependency file(s), and generate a complete, functional Dockerfile. Follow best practices for Dockerfile creation. Output only the Dockerfile content without any explanations or additional text."
        },
        {"role": "user", "content": f"Here is the dependency file(s):\n\n\"\"\"\n{dependency_content}\"\"\""},
        {"role": "user", "content": f"Here is the GitHub link:\n\n\"\"\"\n{github_link}\n\"\"\""}
    ]

    try:
        logging.info("Sending request to OpenAI API to generate Dockerfile.")
        completion = client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:personal::AXNdq8xI",
            messages=messages,
            temperature=0
        )
        assistant_reply = completion.choices[0].message.content
        logging.info("Received response from OpenAI API.")

        # Clean output of dockerfile
        if assistant_reply.startswith("```Dockerfile") and assistant_reply.endswith("```"):
            assistant_reply = assistant_reply[13:-3].strip()
            logging.info("Removed Dockerfile code block markers.")

        if assistant_reply.startswith("\"\"\"") and assistant_reply.endswith("\"\"\""):
            assistant_reply = assistant_reply[3:-3].strip()
            logging.info("Removed triple quotes.")

        # Saving Dockerfile
        os.makedirs(output_dir, exist_ok=True)
        dockerfile_path = os.path.join(output_dir, "Dockerfile")
        with open(dockerfile_path, 'w', encoding='utf-8') as output_file:
            output_file.write(assistant_reply)
        logging.info(f"Dockerfile saved to {dockerfile_path}")

    except Exception as e:
        logging.error(f"Error generating Dockerfile: {e}")
