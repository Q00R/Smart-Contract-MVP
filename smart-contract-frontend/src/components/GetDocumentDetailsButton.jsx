import React, { useState } from 'react'
import DocumentDetailsModal from './DocumentDetailsModal'
import Cookies from 'js-cookie';

const GetDocumentDetailsButton = ({ documentDetails, buttonClass }) => {

    const fixedButtonClass = "btn btn-outline btn-info "

    const [isSetDocumentDetailsModalOpen, setIsDocumentDetailsModalOpen] = useState(false);

    const handleOpenDocumentDetailsModal = () => {
        setIsDocumentDetailsModalOpen(true);
    };

    const handleCloseDocumentDetailsModal = () => {
        setIsDocumentDetailsModalOpen(false);
    };

    return (
        <>
            <button onClick={handleOpenDocumentDetailsModal} className={fixedButtonClass + buttonClass}>Get Details</button>
            <DocumentDetailsModal isOpen={isSetDocumentDetailsModalOpen} onRequestClose={handleCloseDocumentDetailsModal} documentDetails={documentDetails} />
        </>
    )
}

export default GetDocumentDetailsButton