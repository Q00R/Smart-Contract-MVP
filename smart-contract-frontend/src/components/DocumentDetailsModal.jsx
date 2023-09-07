import React from 'react';
import Modal from 'react-modal';

const DocumentDetailsModal = ({ isOpen, onRequestClose, documentDetails }) => {
    const renderDocumentDetails = () => {
        return Object.keys(documentDetails).map((key) => (
            <div key={key} className="flex flex-row space-x-2">
                <span className="font-semibold">{key}:</span>
                <span>{documentDetails[key]}</span>
            </div>
        ));
    };

    return (
        <Modal className={'overflow-hidden'} isOpen={isOpen}>
            <div className="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div className="relative px-6 pt-10 pb-9 shadow-xl mx-auto rounded-2xl">
                    <div className="flex flex-col space-y-16">
                        <button onClick={onRequestClose} className="ml-3 btn btn-accent btn-sm">
                            back
                        </button>

                        <div className="flex flex-col space-y-4">
                            {renderDocumentDetails()}
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
    );
};

export default DocumentDetailsModal;
