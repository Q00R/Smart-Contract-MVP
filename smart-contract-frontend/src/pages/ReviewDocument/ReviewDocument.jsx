import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Cookies from 'js-cookie';
import DownloadButton from '../../components/DownloadButton';
import GetDocumentDetailsButton from '../../components/GetDocumentDetailsButton';
import ReviewDocumentIcon from '../../Assets/ReviewDocument.png';
import Header from '../../components/Header';

const ReviewDocument = () => {
    const { sharedDocumentId } = useParams();
    const [documentTitle, setDocumentTitle] = useState('');
    const [documentID, setDocumentID] = useState('');
    const [documentOwner, setDocumentOwner] = useState('');
    const [documentDetails, setDocumentDetails] = useState({});

    useEffect(() => {
        const handleGetDocument = async () => {
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
                setDocumentTitle(data['doc'].document_name);
                setDocumentOwner(data['sender_email']);
                setDocumentDetails({
                    'Document Name': data['doc'].document_name,
                    'Document ID': data['doc'].document_id,
                    'Document Owner': data['sender_email'],
                    'Document is Complete': data['doc'].document_is_complete ? 'Yes' : 'No',
                    'Document Hash': data['doc'].document_hash,
                    'Document Timestamp': data['doc'].timestamp,

                });
                console.log('documentDetails', documentDetails);


            } catch (error) {
                console.error('Error:', error);
            }
        };

        handleGetDocument();
    }, [sharedDocumentId]);

    const handleAccept = async () => {
        try {
            const response = await fetch(`http://localhost:8000/api/confirm_document/${documentID}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'SID': Cookies.get('token')
                }
            });

            console.log(response);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleReject = async () => {

        try {
            const response = await fetch(`http://localhost:8000/api/reject_document/${documentID}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'SID': Cookies.get('token')
                }
            });
            console.log(response);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="flex flex-col">
            <div className="container rounded-lg shadow-xl border-2 self-center w-1/2 min-h-fit min-w-fit my-8 p-12">
                <Header
                    imgSrc={ReviewDocumentIcon}
                    heading="Review Document"
                />

                <h1 className='font-semibold text-2xl self-center text-center m-4'>{documentTitle}</h1>
                <h1 className='text-xl self-center text-center m-4 my-6'>From: <br /> {documentOwner}</h1>


                <div className='flex flex-row mx-36 space-x-3'>
                    <GetDocumentDetailsButton buttonClass="w-1/2" documentDetails={documentDetails} />
                    <DownloadButton buttonClass="w-1/2" documentDownloadId={documentID} documentDownloadName={documentTitle} />
                </div>

                {/* accept/reject button */}
                <button onClick={handleAccept} className="w-full my-4 btn btn-outline btn-success">Accept</button>

                <button onClick={handleReject} className="w-full my-4 btn btn-outline btn-error">Reject</button>


            </div>
        </div>
    );
}

export default ReviewDocument;
