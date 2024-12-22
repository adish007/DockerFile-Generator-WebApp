import os
import shutil
from glob import glob
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FILES_TO_CHECK = [
    "requirements.txt", "Pipfile", "Pipfile.lock", "pyproject.toml", "environment.yml",
    "package.json", "package-lock.json", "yarn.lock",
    "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts",
    "Gemfile", "Gemfile.lock",
    "composer.json", "composer.lock",
    "go.mod", "go.sum",
    "Cargo.toml", "Cargo.lock",
    "CMakeLists.txt", "Makefile", "vcpkg.json",
    "*.csproj", "*.fsproj", "*.vbproj", "packages.config", "global.json",
    "DESCRIPTION", "renv.lock",
    "mix.exs",
    "stack.yaml", "cabal.project",
    "Dockerfile",
    "build.sh", "start.sh", "install.sh", "setup.sh",
    "configure.ac", "meson.build", "SConstruct",
    ".env"
]

class DependencyNotFoundError(Exception):
    """Custom exception raised when no dependency files are found."""
    pass

def create_prompt_files_folder(repo_url, repo_path, cli_folder="CLI"):
    """
    Creates the 'prompt_files' directory inside the CLI folder, writes the GitHub link to a file,
    and collects dependency files. Raises an error if no dependency files are found.
    """
    output_dir = os.path.join(cli_folder, "prompt_files")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        logging.info(f"Removed existing directory: {output_dir}")
    os.makedirs(output_dir)
    logging.info(f"Created directory: {output_dir}")

    # Add the GitHub link to a file
    github_link_file = os.path.join(output_dir, "github_link")
    with open(github_link_file, "w") as f:
        f.write(repo_url)
    logging.info(f"GitHub link added to {github_link_file}")

    # Collect dependency files
    found_files = []
    for pattern in FILES_TO_CHECK:
        files = glob(os.path.join(repo_path, "**", pattern), recursive=True)
        found_files.extend(files)

    if not found_files:
        logging.warning(f"No dependency files found in {repo_path}.")
        raise DependencyNotFoundError("No dependency files found in the repository.")

    logging.info(f"Found dependency files: {found_files}")
    for file in found_files:
        try:
            shutil.copy(file, output_dir)
            logging.info(f"Copied: {file}")
        except Exception as e:
            logging.error(f"Failed to copy {file}: {e}")

    logging.info(f"All dependency files collected in {output_dir}")
