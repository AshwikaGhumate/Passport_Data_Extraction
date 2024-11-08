import React from 'react';  
import './App.css';  
import DocumentUploader from './DocumentUploader';  

import passportImage from './assets/passport-icon.png'; 

function App() {
    return (
        <div className="app-container">  
            
            {/* Header section */}
            <header className="app-header">  
                <div className="header-content">  
                    
                    {/* Passport Image */}
                    <img 
                        src={passportImage}  // Source path for the passport image icon
                        alt="Passport Icon"  // Alt text for the image 
                        className="passport-image"  // CSS class to apply styles to the image
                    />

                    {/* Title and Description */}
                    <div className="title-container">  
                        <h1 className="app-title">Passport Data Extraction</h1>  
                        <p className="app-description">
                            Upload a passport image and extract details with just a click!
                        </p>  
                    </div>

                </div>
            </header>

            {/* DocumentUploader component - where the user can upload their passport image */}
            <DocumentUploader />

        </div>
    );
}

export default App;  
