import React, { useState } from 'react';
import './DocumentUploader.css';

function DocumentUploader() {
    const [documentData, setDocumentData] = useState(null); // Holds the extracted document data
    const [loading, setLoading] = useState(false); // Indicates if the file is being uploaded
    const [error, setError] = useState(null); // Holds any error message
    const [imagePreview, setImagePreview] = useState(null); // Holds the image preview URL
    const [uploadProgress, setUploadProgress] = useState(0); // Holds the upload progress percentage

    // This function is triggered when a new file is selected for upload
    const handleFileUpload = async (event) => {
        // Reset all the states before uploading a new file
        setDocumentData(null); // Reset extracted data
        setImagePreview(null); // Reset image preview
        setLoading(true); // Set loading to true while uploading
        setError(null); // Clear previous error
        setUploadProgress(0); // Reset upload progress

        const file = event.target.files[0];

        // If no file is selected, show an error and exit
        if (!file) {
            setError('Please select a file first.');
            setLoading(false);
            return;
        }

        // Check if the file is an image to display a preview
        if (file.type.startsWith('image/')) {
            const previewUrl = URL.createObjectURL(file);
            setImagePreview(previewUrl);
        } else {
            setImagePreview(null); // If not an image, clear the preview
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://localhost:5000/extract-data', true);

            // Track upload progress
            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const progress = Math.round((event.loaded / event.total) * 100);
                    setUploadProgress(progress);
                }
            };

            // Handle successful response from the backend
            xhr.onload = () => {
                if (xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText);
                    setDocumentData(data); // Set the extracted data
                    setLoading(false); // Set loading to false once the upload is done
                } else {
                    setError('Failed to upload file. Please try again.');
                    setLoading(false);
                }
            };

            // Handle error response
            xhr.onerror = () => {
                setError('An error occurred during the upload. Please try again.');
                setLoading(false);
            };

            // Send the form data to the server
            xhr.send(formData);

        } catch (err) {
            setError('An error occurred while uploading. Please try again.');
            setLoading(false);
        }
    };

    return (
        <div className="uploader-container">
            <h2 className="title">Upload Your Passport</h2>

            {/* File input for uploading the image */}
            <input
                type="file"
                onChange={handleFileUpload} // Trigger handleFileUpload when a file is selected
                className="file-input"
                aria-label="Upload Passport Image"
            />

            {/* Display image preview if available */}
            {imagePreview && (
                <div className="image-preview-container">
                    <h3 className="preview-title">Image Preview:</h3>
                    <img src={imagePreview} alt="Preview" className="image-preview" />
                </div>
            )}

            {/* Show loading state if the file is being uploaded */}
            {loading && (
                <div className="loading-container">
                    <div className="loading-message">Processing your file...</div>
                    <div className="progress-bar-container">
                        <div
                            className="progress-bar"
                            style={{ width: `${uploadProgress}%` }}
                        ></div>
                    </div>
                    <div className="progress-percentage">{uploadProgress}%</div>
                </div>
            )}

            {/* Display error message if there's any error */}
            {error && <div className="error-message">{error}</div>}

            {/* Show extracted data if available */}
            {documentData && (
                <div className="data-container">
                    <h3 className="data-title">Extracted Data:</h3>
                    <table className="data-table">
                        <tbody>
                            <tr>
                                <td><strong>Name:</strong></td>
                                <td>{documentData.name}</td>
                            </tr>
                            <tr>
                                <td><strong>Passport Number:</strong></td>
                                <td>{documentData.passport_number}</td>
                            </tr>
                            <tr>
                                <td><strong>Expiration Date:</strong></td>
                                <td>{documentData.expiration_date}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default DocumentUploader;