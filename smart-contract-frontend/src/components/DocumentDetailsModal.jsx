import React, { useState } from 'react'
import Modal from 'react-modal'

const DocumentDetailsModal = ({ isOpen, onRequestClose, documentDetails }) => {
    return (
        <Modal className={'overflow-hidden'} isOpen={isOpen}>
            <div class="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div class="relative px-6 pt-10 pb-9 shadow-xl mx-auto rounded-2xl">
                    <div class="flex flex-col space-y-16">
                        <button onClick={onRequestClose} className="ml-3 btn btn-accent btn-sm">
                            back
                        </button>

                        {documentDetails}
                    </div>
                </div>
            </div>
        </Modal>
    )
}

export default DocumentDetailsModal