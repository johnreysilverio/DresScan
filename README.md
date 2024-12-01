# **DresScan**

## **License**
[MIT License](LICENSE)
## **To Train the program:**

## **To Run the program:**

### **Step 1: Check Python Version**

 1.  Open your terminal or command prompt.
 2.  Check your Python version to make sure it's version 3.12.4:
    
    python --version
   or

    python3 --version
    
 3.  If the version is not 3.12.4, you may need to install or upgrade Python to version 3.12.4.

  To download Python 3.12.4, visit the official Python website:
  https://www.python.org/downloads/release/python-3124/
  
### **Step 2: Create a Virtual Environment**
1. Navigate to the directory where your project is located using the cd command. For example:

       cd path/to/your/project
 
2. Create a virtual environment using venv. Replace myenv with the name you want to give your virtual environment:

       python3 -m venv myenv
   
or

       python -m venv myenv

### **Step 3: Activate the Virtual Environment**

  Activate the virtual environment:

  On Windows: 
  
  ```myenv\Scripts\activate```

  On macOS/Linux: 
  
  ```source myenv/bin/activate```
  
  Once activated, you should see (myenv) at the beginning of your terminal prompt, indicating that the virtual environment is active.
  
### **Step 4: Install Dependencies**

  1. Ensure you have your requirements.txt file in the project directory.
  2. Install the required dependencies listed in requirements.txt by running: pip install -r requirements.txt
  This will automatically install all the libraries and packages needed for your project, such as cv2, pyttsx3, ultralytics, etc.

### **Step 5: Run Your Program**

  1. Run your program (e.g., app.py) after installing all dependencies: python app.py
  This will start the program, and you should see the GUI running along with the object detection.

### **Step 6: Deactivate the Virtual Environment (When Done)**

  1. After you finish working, you can deactivate the virtual environment by running: deactivate
  Now, you have a clear set of steps to get your program running! Let me know if you need more details or run into any issues.

