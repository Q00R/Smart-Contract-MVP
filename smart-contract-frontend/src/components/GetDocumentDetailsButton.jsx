import React, { useState } from 'react'
import DocumentDetailsModal from './DocumentDetailsModal'
import Cookies from 'js-cookie';

const GetDocumentDetailsButton = ({ documentID }) => {

    const [documentDetails, setDocumentDetails] = useState({});
    const [isSetDocumentDetailsModalOpen, setIsDocumentDetailsModalOpen] = useState(false);

    const handleOpenDocumentDetailsModal = () => {
        setIsDocumentDetailsModalOpen(true);
    };

    const handleCloseDocumentDetailsModal = () => {
        setIsDocumentDetailsModalOpen(false);
    };


    const handleGetDetails = async () => {

        try {
            const response = await fetch(`http://localhost:8000/api/documents/${documentID}/retrieve_details/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'SID': Cookies.get('token')
                }
            });
            response.json().then((data) => {
                console.log(data, "data");
                setDocumentDetails(data);
                console.log(documentDetails);
                setIsDocumentDetailsModalOpen(true);
            });
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <button onClick={handleGetDetails} className="btn btn-sm btn-outline btn-info">Get Document Details</button>
            <DocumentDetailsModal isOpen={isSetDocumentDetailsModalOpen} onRequestClose={handleCloseDocumentDetailsModal} documentDetails={documentDetails} />
        </div>
    )
}

export default GetDocumentDetailsButton