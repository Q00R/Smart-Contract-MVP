import React, { useState } from 'react';
import Modal from 'react-modal';
import Cookies from 'js-cookie';
import goBackIcon from "../Assets/GoBackImage.png";

const UserProfileModal = ({ isOpen, onRequestClose }) => {

    return (
        <Modal className={'overflow-hidden'} isOpen={isOpen} onRequestClose={onRequestClose}>
            <div class="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div class="relative px-6 pt-10 pb-9 shadow-xl mx-auto w-full max-w-lg rounded-2xl">
                    <div class="mx-auto flex w-full max-w-md flex-col space-y-16">
                        <div class="flex flex-col items-center justify-center text-center space-y-2">
                            <div class="font-semibold text-3xl">
                                <p>Email Verification</p>
                            </div>
                            <div class="flex flex-row text-sm font-medium text-base-content">
                                <p>We have sent a code to your email</p>

                                <button onClick={onRequestClose} className="absolute top-0 left-0 m-2 w-10 h-10">
                                    <img src={goBackIcon} alt='go back' />

                                </button>
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
