import os
import string as st
import easyocr
import cv2
import warnings
import matplotlib.image as mpimg
from dateutil import parser
from passporteye import read_mrz
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importing the CORS package for cross-origin requests

# Suppressing warnings to avoid cluttering the console
warnings.filterwarnings('ignore')

# Initializing EasyOCR Reader for text extraction (English language and no GPU)
reader = easyocr.Reader(lang_list=['en'], gpu=False)

# Initializing Flask app and enable CORS for cross-origin resource sharing
app = Flask(__name__)
CORS(app)

# Path to store uploaded files temporarily
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Creates the uploads folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def parse_date(date_string, iob=True):
    """
    Parse and format date from passport MRZ data.
    Args:
        date_string (str): Raw date string from MRZ.
        iob (bool): Flag to handle input/output behavior (default is True).
    Returns:
        str: Formatted date in DD/MM/YYYY format.
    """
    date = parser.parse(date_string, yearfirst=True).date()  # Parsing the date string
    return date.strftime('%d/%m/%Y')  # Returning the formatted date


def clean(string):
    """
    Clean the string to only include alphanumeric characters and convert to uppercase.
    Args:
        string (str): Raw string.
    Returns:
        str: Cleaned string.
    """
    return ''.join(i for i in string if i.isalnum()).upper()  # Removing non-alphanumeric characters


def get_data_from_mrz(img_path):
    """
    Extract personal information from the Machine Readable Zone (MRZ) of a passport.
    Args:
        img_path (str): Path to the passport image file.
    Returns:
        dict: Extracted user information like name, passport number, and expiration date.
    """
    user_info = {}
    
    # Temporary file path to save the region of interest (ROI) extracted from the MRZ
    new_im_path = 'temporary.png'
    
    # Reading MRZ from the image
    mrz = read_mrz(img_path, save_roi=True)
    
    if mrz:
        # Saving and reading the extracted ROI (region containing MRZ)
        mpimg.imsave(new_im_path, mrz.aux['roi'], cmap='gray')
        img = cv2.imread(new_im_path)
        
        # Resizing the image to a consistent size for text extraction
        img = cv2.resize(img, (1110, 140))
        
        # Defining allowed characters for OCR (letters, digits, and special characters)
        allowlist = st.ascii_letters + st.digits + '< '
        
        # Performing OCR to extract text from the MRZ region
        code = reader.readtext(img, paragraph=False, detail=0, allowlist=allowlist)
        
        if len(code) >= 2:
            a, b = code[0].upper(), code[1].upper()
            
            # Ensuring MRZ fields are padded to the correct length
            a = a + '<' * (44 - len(a)) if len(a) < 44 else a
            b = b + '<' * (44 - len(b)) if len(b) < 44 else b

            # Extracting surname and names from the MRZ
            surname_names = a[5:44].split('<<', 1)
            if len(surname_names) < 2:
                surname_names += ['']
            surname, names = surname_names
            
            # Storing extracted data in a dictionary
            user_info['name'] = names.replace('<', ' ').strip().upper()
            user_info['passport_number'] = clean(b[0:9])  # Cleaning passport number
            user_info['expiration_date'] = parse_date(b[21:27])  # Parsing expiration date

        # Cleaning up the temporary image file after extraction
        os.remove(new_im_path)
    else:
        return None
    
    return user_info


@app.route('/extract-data', methods=['POST'])
def upload_file():
    """
    Handle the file upload and data extraction from the uploaded passport image.
    Args:
        None (handled via HTTP POST request).
    Returns:
        JSON: Extracted user data or an error message.
    """
    # Checking if a file is provided in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400  # Returning an error if no file is provided
    
    # Get the uploaded file from the request
    file = request.files['file']
    
    # Checking if the file is empty (no file selected)
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Saving the uploaded image to a temporary file in the server's uploads directory
    temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(temp_file_path)
    
    try:
        # Processing the uploaded file and extract data from the MRZ
        user_info = get_data_from_mrz(temp_file_path)
        
        if user_info:
            # If MRZ data extraction is successful, return the extracted info
            return jsonify(user_info), 200
        else:
            # If MRZ data extraction fails, return an error message
            return jsonify({'error': 'Unable to read image. Please try again later.'}), 400
    finally:
        # Cleaning up the uploaded temporary file from the server
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == '__main__':
    """
    Start the Flask web application.
    This will run the web server locally and enable file upload functionality.
    """
    app.run(debug=True)  # Running the app in debug mode for development purposes
