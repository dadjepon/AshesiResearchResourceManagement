import React, { useState, useRef } from 'react';
import "./modal3.css";

const Modal3 = (
  // {isOpen, onClose}
  ) => {
    const logo_2 = '/images/background_image.png';
    const logo = '/images/Import Pdf.png'

    const [file, setFile] = useState(null);
    const fileInputRef = useRef(null);
  
    // if (!isOpen) {
    //   return null;
    // }
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
                    <label htmlFor="title" className="titleText">
                        Title<span className="requiredAsterisk">*</span>:
                    </label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        placeholder="Enter your title here"
                        className="titleTextField"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="publication" className='publicationText'>Publication Link:</label>
                    <input
                        type="text"
                        id="publication"
                        name="publication"
                        placeholder="https://www.publication.com/in/bright-sithole/"
                        className="publicationBox"
                    />
                </div>
                <div className="preview-modal3-box">
        {/* Add the text inside the preview box as a link */}
        <a href="#!" className="upload-modal3-text" onClick={openFileInput}>
          Upload a writing sample
        </a>
        {file && <img src={file} alt="Profile" />}
        <img src={logo} alt="pdfLogo" className="pdf-image" />
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
        <button className="upload-modal3-button"
        // onClick={take info to database !}
        >
          Add a Sample
        </button>
      </div>
            </form>
        </div>
    );
};

export default Modal3;
