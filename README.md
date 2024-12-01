# **DresScan**

## **License**
[MIT License](LICENSE)
## **To Train the program:**

## **To Run the program:**

### **Step 1: Check Python Version**

 1.  Open your terminal or command prompt.
 2.  Check your Python version to make sure it's version 3.12.4:
     ```type
     python --version
     ```
     or 
     ```type
     python3 --version
     ```  
 3.  If the version is not 3.12.4, you may need to install or upgrade Python to version 3.12.4.

  To download Python 3.12.4, visit the official Python website:
  https://www.python.org/downloads/release/python-3124/
  
### **Step 2: Create a Virtual Environment**
 1. Navigate to the directory where your project is located using the cd command.
    ```type
    cd path/to/your/project
    ```
 2. Create a virtual environment using venv. Replace myvenv with the name you want to give your virtual envrionment:
    ```type
    python3 -m venv myvenv
    ```
    or
    ```type
    python -m venv myvenv
    ```
    

### **Step 3: Activate the Virtual Environment**

  1. Activate the virtual environment:

     On Windows:
     ```type
     myvenv\Scripts\activate
     ```

     On macOS/Linux:
     ```type
     source myvenv/bin/activate
     ```

     Once activated, you should see (myvenv) at the beginning of your terminal prompt, indicating that the virtual environment is active.
  
### **Step 4: Install Dependencies**

  1. Ensure you have your ```requirements.txt``` file in the project directory.
  2. Install the required dependencies listed in requirements.txt by running:
     ```type
     pip install -r requirements.txt
     ```

### **Step 5: Run Your Program**

  1. Run your program after installing all dependencies:
     ```type
     python app.py
     ```

### **Step 6: Deactivate the Virtual Environment (When Done)**

  1. After you finish working, you can deactivate the virtual environment by running:
     ```type
     deactivate
     ```

