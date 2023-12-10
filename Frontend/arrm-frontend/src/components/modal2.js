import React from 'react';
import '../styles/modal2.css'; // Import the external CSS file

const Modal2 = () => {
    const logo_2 = '/images/background_image.png';

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
                    <label htmlFor="bio" className="bioText">
                        Bio<span className="requiredAsterisk">*</span>:
                    </label>
                    <input
                        type="text"
                        id="bio"
                        name="bio"
                        placeholder="Enter your bio"
                        className="bioTextField"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="linkedin" className='linkedInProfileText'>LinkedIn Profile:</label>
                    <input
                        type="text"
                        id="linkedin"
                        name="linkedin"
                        placeholder="https://www.linkedin.com/in/bright-sithole/"
                        className="linkedInProfileBox"
                    />
                </div>
                <button type="submit" className="modal2Button">Add Bio</button>
            </form>
        </div>
    );
};

export default Modal2;
