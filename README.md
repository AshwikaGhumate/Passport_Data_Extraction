### Passport Data Extraction Web Application


## Overview

This full-stack web application, built with React and Flask, allows users to upload a passport image to extract essential information, such as name, passport number, and expiration date. The backend uses Optical Character Recognition (OCR) technology for text extraction, while the frontend provides an intuitive interface for users to interact with.


## Key Features

**Image Upload**: Users can upload an image of their passport.
**Data Extraction**: The backend uses MRZ (Machine Readable Zone) processing to extract key details.
**Responsive UI**: Developed with React for a clean, user-friendly experience.
**Backend Processing**: Built with Flask, integrating EasyOCR and PassportEye for image processing.


## Tech Stack

**Frontend**: React, JavaScript, HTML, CSS
**Backend**: Python Flask, Flask-CORS, EasyOCR, PassportEye
**Image Processing**: OpenCV, EasyOCR for MRZ data extraction


## Installation

**Prerequisites**
Node.js: Required for React frontend
Python 3.x: Required for Flask backend and dependencies

**Steps**
1. Clone the Repository
git clone https://github.com/AshwikaGhumate/Passport_Data_Extraction.git
cd passport-data-extraction

2. Backend Setup
   
   a. Navigate to the backend directory
     
         cd backend

   b. Set up and activate virtual environment

        python -m venv venv
   
        venv\Scripts\activate

  c. Install the required Python packages
    pip install -r requirements.txt

3. Frontend Setup
  a. Navigate to the frontend directory
      cd frontend 

4. Run the Application
  a. Start Backend: In the backend folder:
      python app.py
   
  b. Start Frontend: In the frontend folder:
      npm start
      
  c. The application should now be accessible at http://localhost:3000
  
## API Endpoints

1. POST /extract-data
  a. Description: Uploads a passport image for data extraction.
  b. Request: Expects an image file (multipart/form-data).
  c. Response: JSON object with extracted fields (name, passport_number, and expiration_date).
