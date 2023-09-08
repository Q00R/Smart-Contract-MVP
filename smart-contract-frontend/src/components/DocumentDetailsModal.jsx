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
            <div class="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div class="relative px-6 pt-10 pb-9 shadow-xl mx-auto rounded-2xl">
                    <div class="flex flex-col space-y-16">
                        <div className="flex flex-col items-center justify-center">
                            <div className="bg-base-200 shadow-xl rounded-lg py-3 h-fit">
                                <button onClick={onRequestClose} className="ml-3 btn btn-accent btn-sm">
                                    back
                                </button>

                                <h3 className="text-center text-2xl text-base-content font-medium leading-8">
                                    Document Details
                                </h3>
                                <table className="text-2xl my-10 mx-5">
                                    <tbody>
                                        <tr>
                                            <td class="px-2 py-2 text-base-content font-semibold">
                                                {renderDocumentDetails()}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Modal >
    );
};

export default DocumentDetailsModal;
