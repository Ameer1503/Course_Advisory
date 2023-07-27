## Flask Application Virtual Environment Setup

This README file provides a step-by-step guide on how to set up a virtual environment for running a Flask application. A virtual environment ensures that the required dependencies are isolated from the system-wide Python installation, reducing potential conflicts and making your application more portable. This guide assumes you have Python and pip installed on your system.

### Step 1: Clone the Repository

Clone the repository containing the Flask application to your local machine using Git:



Replace `https://github.com/AmeerTechsoft/Course_Advisory` with the URL of your Git repository and `Course_Advisor` with the name of the repository.

### Step 2: Install Virtualenv (if not installed)

If you haven't installed Virtualenv yet, you can do so using pip:

pip install virtualenv

sql


### Step 3: Create a Virtual Environment

In the root directory of your Flask application, create a new virtual environment. You can name it anything you like; here, we'll call it "venv":

virtualenv venv

sql


This command will create a folder named "venv" containing the isolated Python environment.

### Step 4: Activate the Virtual Environment

Activate the virtual environment to start using it. The method for activating depends on your operating system:

**On Windows:**

venv\Scripts\activate



**On macOS and Linux:**

source venv/bin/activate




Once the virtual environment is activated, your command prompt or terminal will show the environment name in the prompt (e.g., `(venv)`).

### Step 5: Install Dependencies

With the virtual environment active, use pip to install the required dependencies for the Flask application. Usually, these dependencies are listed in a "requirements.txt" file in the project directory:

pip install -r requirements.txt



Make sure the "requirements.txt" file is present in the project directory, and it contains the required packages and their versions.

### Step 6: Configure Flask Application (if necessary)

If your Flask application requires any configuration, such as environment variables or database settings, make sure to set them accordingly. These configurations might be stored in a separate file like "config.py" or taken from environment variables.

### Step 7: Run the Flask Application

Now that your virtual environment is set up and the dependencies are installed, you can run the Flask application:

python app.py




Replace "app.py" with the name of your main Flask application file if it's different.

### Step 8: Access the Application

Once the Flask application is running, you can access it in your web browser by visiting the address displayed in the terminal (usually `http://127.0.0.1:5000/`).

### Step 9: Deactivate the Virtual Environment

When you're done working on the Flask application, you can deactivate the virtual environment by running:

deactivate




This will return you to your system's default Python environment.

Congratulations! You've successfully set up a virtual environment and run your Flask application. Remember to activate the virtual environment again whenever you work on the project. Happy coding!
