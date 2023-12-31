import React, { useState } from 'react';
import Modal from 'react-modal';
import Cookies from 'js-cookie';
import goBackIcon from "../Assets/GoBackImage.png";
import UserProfileCard from './UserProfileCard';

const UserProfileModal = ({ isOpen, onRequestClose }) => {

    return (
        <Modal className={'overflow-hidden'} isOpen={isOpen} onRequestClose={onRequestClose}>
            <div class="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div class="relative px-6 pt-10 pb-9 shadow-xl mx-auto rounded-2xl">
                    <div class="flex flex-col space-y-16">
                        <UserProfileCard isOpen={isOpen} onRequestClose={onRequestClose} />
                    </div>
                </div>
            </div>
        </Modal>
    );
};


export default UserProfileModal;
