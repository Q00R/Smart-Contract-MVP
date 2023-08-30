import React, { useState } from 'react';
import FileInput from './FileInput';
import FormAction from './FormAction';
import Cookies from 'js-cookie';


const UploadPDF = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (file) => {
        setSelectedFile(file);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedFile) {
            console.log('No file selected.');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('document_file', selectedFile);
            console.log(Cookies.get('token'));


            // Perform the file upload here
            const response = await fetch('http://localhost:8000/api/documents/upload/', {
                method: 'POST',
                headers: {
                    'SID': Cookies.get('token'),
                },
                body: formData,
            });

            const data = await response.json();
            console.log(data);

        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <div>
            <FileInput onFileChange={handleFileChange} />
            <FormAction handleSubmit={handleSubmit} text="Upload" />
        </div>
    );
};

export default UploadPDF;
