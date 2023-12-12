import React, { useState, useRef } from 'react';
import '../styles/admin_premake.css'; // Import the external CSS file

const AdminPremake = () => {
    const logo_2 = '/images/background_image.png';
    const logo = '/images/Import Pdf.png'

    const [file, setFile] = useState(null);
    const fileInputRef = useRef(null);
  
    const handleUpload = (e) => {
      setFile(URL.createObjectURL(e.target.files[0]));
    };
  
    const openFileInput = () => {
      fileInputRef.current.click();
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        // Handle form submission logic here
        // Access the bio and LinkedIn profile input values using formRef.current
        // For example: console.log(formRef.current.bio.value, formRef.current.linkedin.value);
    };

    return (
        <div className="mainContainer">
            <div className="back-container">
                <img src={logo_2} alt="back Logo" className="back-image" />
            </div>
            <form onSubmit={handleSubmit} className="formContainer">
                <div>
                    <label htmlFor="premake" className="premakeText">
                        Admin, Premake Accounts by uploading the CSV file </label>
                </div>
                <div className="preview-premake-box">
        {/* Add the text inside the preview box as a link */}
        <a href="#!" className="upload-premake-text" onClick={openFileInput}>
          Upload a writing sample
        </a>
        {file && <img src={file} alt="Profile" />}
        <img src={logo} alt="pdfLogo" className="pdf-premake-image" />
      </div>
      <div className="upload-section">
        {/* Hidden file input */}
        <input
          type="file"
          id="fileInput"
          onChange={handleUpload}
          className="upload-input visually-hidden"
          ref={fileInputRef}
        />
        {/* Button to trigger file input */}
        <button className="upload-premake-button">
          Add a CSV File
        </button>
      </div>
            </form>
        </div>
    );
};

export default AdminPremake;
