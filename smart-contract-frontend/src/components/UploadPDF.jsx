import React, { useState } from 'react';
import FileInput from './FileInput';
import EmailInput from './EmailInput';
import FormAction from './FormAction';
import Cookies from 'js-cookie';


const UploadPDF = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [emailList, setEmailList] = useState({ email: [] });


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

            handleAddEmails()

            window.location.reload();

        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const handleAddEmails = async () => {

        try {
            const response = await fetch('http://localhost:8000/api/documents/upload/<str:doc_id>/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'SID': Cookies.get('token'),
                },
                body: JSON.stringify(emailList),
            });

            const data = await response.json();
            console.log(data);

        } catch (error) {
            console.error('Error adding emails:', error);
        }

    };


    return (
        <div>

            <EmailInput emailList={emailList} setEmailList={setEmailList} />

            <FileInput onFileChange={handleFileChange} />

            <FormAction handleSubmit={handleSubmit} text="Upload" />
        </div>
    );
};

export default UploadPDF;
