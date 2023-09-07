import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Cookies from 'js-cookie';
import DownloadButton from '../../components/DownloadButton';
import GetDocumentDetailsButton from '../../components/GetDocumentDetailsButton';

const ReviewDocument = () => {
    const { sharedDocumentId } = useParams();
    const [documentTitle, setDocumentTitle] = useState('');
    const [documentID, setDocumentID] = useState('');
    const [documentOwner, setDocumentOwner] = useState('');

    useEffect(() => {
        const handleGetDocument = async () => {
            console.log('sharedDocumentId', sharedDocumentId);

            try {
                const response = await fetch(`http://localhost:8000/review-share-doc/${sharedDocumentId}/`, {
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

                setDocumentID(data['doc'].document_id);
                setDocumentTitle(data['doc'].document_name);
                setDocumentOwner(data['sender_email']);


            } catch (error) {
                console.error('Error:', error);
            }
        };

        handleGetDocument();
    }, [sharedDocumentId]);

    return (
        <div>
            <h1>Review Document Page</h1>
            <p>Doc Title: {documentTitle}</p>
            <p>Doc Owner email: {documentOwner}</p>
            <p>Doc share ID: {sharedDocumentId}</p>
            <p>Doc ID: {documentID}</p>
            <GetDocumentDetailsButton documentID={documentID} />
            <DownloadButton documentDownloadId={documentID} documentDownloadName={documentTitle} />

            {/* accept/reject button */}

        </div>
    );
}

export default ReviewDocument;
