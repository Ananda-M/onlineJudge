from django.shortcuts import render
from django.http import HttpResponse
from submit.forms import CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path

import html
import re

def sanitize_code(code: str) -> str:
    # Escape HTML special characters to prevent HTML injection
    sanitized_code = html.escape(code)

    # Optional: Remove potential harmful content, e.g., <script> tags
    sanitized_code = re.sub(r'<script.*?>.*?</script>', '', sanitized_code, flags=re.S)

    # Optional: Prevent SQL-like patterns (if applicable)
    sanitized_code = re.sub(r'(--|;|/\*|\*/)', '', sanitized_code)

    return sanitized_code


import logging

logger = logging.getLogger(__name__)

def submit(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.code = sanitize_code(submission.code)
            logger.debug(f"Language: {submission.language}")
            logger.debug(f"Code: {submission.code}")

            output, error = run_code(
                submission.language, submission.code, submission.input_data
            )
            submission.output_data = output
            submission.error_data = error
            submission.save()

            return render(request, "result.html", {"submission": submission})
    else:
        form = CodeSubmissionForm()

    return render(request, "index.html", {"form": form})


def run_code(language, code, input_data):
    project_path = os.path.join(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    # Create directories if they don't exist
    for directory in directories:
        dir_path = os.path.join(project_path, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    codes_dir = os.path.join(project_path, "codes")
    inputs_dir = os.path.join(project_path, "inputs")
    outputs_dir = os.path.join(project_path, "outputs")

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"input_{unique}.txt"
    output_file_name = f"output_{unique}.txt"
    error_file_name = f"error_{unique}.txt"

    code_file_path = os.path.join(codes_dir, code_file_name)
    input_file_path = os.path.join(inputs_dir, input_file_name)
    output_file_path = os.path.join(outputs_dir, output_file_name)
    error_file_path = os.path.join(outputs_dir, error_file_name)

    # Write the code and input to their respective files
    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    # Create empty output and error files
    open(output_file_path, 'w').close()
    open(error_file_path, 'w').close()

    try:
        if language == "cpp":
            executable_path = os.path.join(codes_dir, unique)
            # Compile the C++ code
            compile_result = subprocess.run(
                ["clang++", code_file_path, "-o", executable_path],
                check=True  # Raises an exception if the command fails
            )
            # Run the executable
            with open(input_file_path, "r") as input_file, \
                    open(output_file_path, "w") as output_file, \
                    open(error_file_path, "w") as error_file:
                subprocess.run(
                    [executable_path],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=error_file,
                    check=True,
                    timeout=5
                )
        elif language == "py":
            # Execute the Python script
            with open(input_file_path, "r") as input_file, \
                    open(output_file_path, "w") as output_file, \
                    open(error_file_path, "w") as error_file:
                subprocess.run(
                    ["python3", code_file_path],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=error_file,
                    check=True,
                    timeout=5
                )
    except subprocess.CalledProcessError as e:
        # If there is an error during compilation or execution, return the error data
        with open(error_file_path, "r") as error_file:
            error_data = error_file.read()
        return "", error_data

    # Read the output and error from their respective files
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()
    
    with open(error_file_path, "r") as error_file:
        error_data = error_file.read()

    return output_data, error_data