import os
import re
import subprocess
import tempfile
from pathlib import Path

# Function to clone GitHub repository with only the most recent version
def clone_github_repo(repo_url, clone_dir):
    try:
        # Add --depth 1 to clone only the latest version
        subprocess.run(['git', 'clone', '--depth', '1', repo_url, clone_dir], check=True)
        print(f"Cloned repository to {clone_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        exit(1)

# Function to extract relevant text from different file types
def extract_text_from_file(file_path):
    text = ""
    file_extension = file_path.suffix.lower()
    
    if file_extension in ['.md', '.txt']:
        # Read text from markdown or text files
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    elif file_extension in ['.py', '.js', '.cpp', '.c', '.java']:
        # Extract comments from code files (basic implementation)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line in lines:
                # Extract lines that start with comments
                if re.match(r'^\s*#', line) or re.match(r'^\s*//', line) or re.match(r'^\s*/\*', line):
                    text += line

    # Formatting the text output
    if text:
        header = f"\n{'='*40}\n{file_path.name}\n{'='*40}\n"
        return header + text + "\n\n"
    return ""

# Main function to generate a single .txt file from all extracted content
def generate_text_from_repo(repo_url, output_file=None):
    # Create a temporary directory to clone the repo
    with tempfile.TemporaryDirectory() as tempdir:
        clone_github_repo(repo_url, tempdir)
        
        # Collect all text from relevant files in the repository
        extracted_text = ""
        for root, _, files in os.walk(tempdir):
            for file in files:
                file_path = Path(root) / file
                extracted_text += extract_text_from_file(file_path)
        
        # If no output file name is provided, use the repository name from the URL
        if not output_file:
            match = re.search(r'github\.com[/:]([^/]+)/([^/]+)', repo_url)
            if match:
                repo_name = f"{match.group(1)}_{match.group(2)}.txt"
                output_file = repo_name
        
        # Write the collected text into a single .txt file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        print(f"All content written to {output_file}")

# Usage Example
if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ")
    output_file = None  # Default to automatic naming based on repository name
    generate_text_from_repo(repo_url, output_file)
    print(f"Formatted text file created: {output_file}")
