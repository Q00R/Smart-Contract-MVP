import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Cookies from 'js-cookie';

const ReviewDocument = () => {
    const { doc_id } = useParams();
    const [documentTitle, setDocumentTitle] = useState('');
    const [documentID, setDocumentID] = useState('');

    useEffect(() => {
        const handleGetDocument = async () => {
            console.log('doc_id', doc_id);

            try {
                const response = await fetch(`http://localhost:8000/review-share-doc/${doc_id}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'SID': Cookies.get('token')
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                console.log('data', data);
                console.log('Success:', data);
                setDocumentID(data['doc_id']);
                setDocumentTitle(data['doc']['document_name']);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        handleGetDocument();
    }, [doc_id]);

    return (
        <div>
            <h1>Review Document Page</h1>
            <p>Doc share ID: {doc_id}</p>
            <p>Doc ID: {documentID}</p>
            <p>Doc Title: {documentTitle}</p>
            {/* Rest of your ReviewDocument component */}
        </div>
    );
}

export default ReviewDocument;
