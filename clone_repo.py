import os
import shutil
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clone_repo(repo_url, dest_folder="WebApp/temp_repo"):
    """
    Clones the repository to the specified destination folder.
    """
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
        logging.info(f"Removed existing directory: {dest_folder}")

    try:
        logging.info(f"Cloning repository from {repo_url} to {dest_folder}")
        subprocess.run(["git", "clone", repo_url, dest_folder], check=True)
        logging.info(f"Repository cloned to {dest_folder}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Git clone failed: {e}")
        raise
