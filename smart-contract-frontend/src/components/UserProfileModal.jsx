import React, { useState } from 'react';
import Modal from 'react-modal';

const UserProfileModal = ({ isOpen, onRequestClose }) => {

    return (
        <Modal className={'overflow-hidden'} isOpen={isOpen} onRequestClose={onRequestClose}>
            <div class="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div class="relative px-6 pt-10 pb-9 shadow-xl mx-auto w-full max-w-lg rounded-2xl">
                    <div class="mx-auto flex w-full max-w-md flex-col space-y-16">
                        <div class="flex flex-col items-center justify-center text-center space-y-2">
                            <div class="font-semibold text-3xl">
                                <p>Email Verification</p>
                                <button onClick={onRequestClose} className="bg-white absolute top-0 right-0 m-5">
                                </button>
                            </div>
                            <div class="flex flex-row text-sm font-medium text-base-content">
                                <p>We have sent a code to your email</p>
                            </div>
                        </div>

                        <div>

                        </div>
                    </div>
                </div>
            </div>
        </Modal>
    );
};


export default UserProfileModal;
