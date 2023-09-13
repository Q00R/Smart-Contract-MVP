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

            // Perform the file upload here
            const response = await fetch('http://localhost:8000/api/documents/upload/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${Cookies.get('token')}`
                },
                body: formData, // Use the FormData object
            });

            const data = await response.json();

            //handle if user is not activated
            if (data['message'] === 'User is not activated') {
                console.log('User is not activated');

                //show some error message fel frontend


                return;
            }

            console.log(data);

            await handleAddEmails(data['Doc_id']);

        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };



    const handleAddEmails = async (doc_id) => {

        console.log('doc_id', doc_id);
        console.log('emailList', emailList.email);

        console.log('emailList tany', JSON.stringify(emailList.email));
        try {
            const response = await fetch(`http://localhost:8000/api/documents/EmailAdd/${doc_id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}`
                },
                body: JSON.stringify({ email_list: emailList.email }), // Correct the JSON structure here
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
