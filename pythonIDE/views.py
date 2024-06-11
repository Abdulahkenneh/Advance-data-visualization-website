from django.shortcuts import render, redirect
import docker
from .forms import IDE_form,CodeSnippetForm,CodeSnippet
import logging
import io
import sys
from django.contrib.auth.decorators import login_required

# Configure logging to output debug messages
# logging.basicConfig(level=logging.DEBUG)

# def ide_content_execute_view(request):
#     result = None
#     error = None

#     if request.method == 'POST':
#         form = IDE_form(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             client = docker.from_env()
#             try:
#                 logging.debug("Before running the code in the container")
#                 # Run the code in the container
#                 container = client.containers.run(
#                     "python-sandbox",
#                     f"python -c \"{code}\"",
#                     detach=True,
#                     stdin_open=True,
#                     stdout=True,
#                     stderr=True,
#                     auto_remove=True
#                 )
#                 logging.debug("After running the code in the container")
#                 # Wait for the container to finish executing
#                 exit_status = container.wait()
#                 # Capture the logs
#                 result = container.logs(stdout=True, stderr=False).decode('utf-8')
#                 error = container.logs(stdout=False, stderr=True).decode('utf-8')

#             except docker.errors.ContainerError as e:
#                 error = str(e)
#             except docker.errors.ImageNotFound as e:
#                 error = "Docker image not found. Please ensure the image is built and available."
#             except docker.errors.APIError as e:
#                 error = "Docker API error occurred."
#             except Exception as e:
#                 error = str(e)
#                 logging.error(f"An error occurred: {error}")
                
#             # After processing the form, redirect to a success page
#             return redirect('python-ide:execute-ide')  # Replace 'success_page' with the name of your success page URL pattern
#     else:
#         form = IDE_form()

#     logging.debug("Before rendering the template")
#     return render(request, 'pythonIDE/ide.html', {'form': form, 'result': result, 'error': error})


# Configure logging to output debug messages
logging.basicConfig(level=logging.DEBUG)



def execute_code(code):
    try:
        logging.debug("Before executing the code")

        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        exec_globals = {}
        exec(code, exec_globals)

        # Reset stdout
        sys.stdout = old_stdout

        # Capture printed output
        printed_output = redirected_output.getvalue()

        # Capture result variable if it exists
        result = exec_globals.get('result', None)

        # Combine printed output and result variable
        if result:
            combined_result = printed_output + "\n" + str(result)
        else:
            combined_result = printed_output

        # Handle case where there is no output
        if not combined_result.strip():
            combined_result = 'Code executed successfully but no result to display.'

        logging.debug(f"Execution result: {combined_result}")
        return combined_result, None
    except Exception as e:
        error = str(e)
        logging.error(f"An error occurred: {error}")
        return None, error
@login_required(login_url="/login/")
def ide_view(request):
    result = None  # Define result variable with a default value
    error = None   # Define error variable with a default value

    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            result, error = execute_code(code)
            if error is None:
                # Save code snippet to database
                form.save()
        else:
            logging.debug("Form is not valid")
    else:
        form = CodeSnippetForm()
    
    logging.debug(f"Before rendering the template - Result: {result}, Error: {error}")
    return render(request, 'pythonIDE/ide.html', {'form': form, 'result': result, 'error': error})





# def restricted_exec(code):
#     allowed_builtins = {
#         'print': print,
#         'str': str,
#         'int': int,
#         'float': float,
#         'bool': bool,
#         'len': len,
#         'range': range,
#         'abs': abs,
#         'sum': sum,
#         'min': min,
#         'max': max,
#         # Add other allowed built-ins as needed
#     }

#     exec_globals = {
#         '__builtins__': allowed_builtins,
#     }

#     exec_locals = {}

#     # Redirect stdout to capture print statements
#     old_stdout = sys.stdout
#     redirected_output = sys.stdout = io.StringIO()

#     try:
#         exec(code, exec_globals, exec_locals)
#         result = redirected_output.getvalue()
#         sys.stdout = old_stdout

#         if not result.strip():
#             result = 'Code executed successfully but no result to display.'

#         return result, None
#     except Exception as e:
#         sys.stdout = old_stdout
#         error = ''.join(traceback.format_exception(None, e, e.__traceback__))
#         return None, error

# def ide_view(request):
#     result = None  # Define result variable with a default value
#     error = None   # Define error variable with a default value

#     if request.method == 'POST':
#         form = CodeSnippetForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             result, error = restricted_exec(code)
#             if error is None:
#                 # Save code snippet to database
#                 form.save()
#         else:
#             logging.debug("Form is not valid")
#     else:
#         form = CodeSnippetForm()
    
#     logging.debug(f"Before rendering the template - Result: {result}, Error: {error}")
#     return render(request, 'pythonIDE/ide.html', {'form': form, 'result': result, 'error': error})

# # Add security headers to the response
# def add_security_headers(response):
#     response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net;"
#     response['X-Content-Type-Options'] = 'nosniff'
#     response['X-Frame-Options'] = 'DENY'
#     response['X-XSS-Protection'] = '1; mode=block'
#     return response