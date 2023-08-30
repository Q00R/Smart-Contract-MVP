import React, { useState } from 'react';
import logo from "../Assets/logo.png";
import userIcon from "../Assets/user.png";
import UserProfileModal from './UserProfileModal';
import Cookies from 'js-cookie';

const Navbar = () => {

    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };


    const handleUser = () => {
        console.log(Cookies.get('token'));
        // If there is a user logged in, open the user profile modal
        if (Cookies.get('token')) {
            console.log("User is logged in");
            console.log();
            setIsModalOpen(true);
        } else {
            // Redirect to login page
            window.location.href = '/login';
        }
    };

    const handleLogo = () => {
        // If there is a user logged in, show the user's dashboard
        if (Cookies.get('token')) {
            window.location.href = '/dashboard';
        } else {
            // Redirect to home page
            window.location.href = '/';
        }
    };

    const closeUserProfileModal = () => {
        setIsModalOpen(false);
    };

    return (
        <div
            className="z-50 flex items-center px-2 duration-300 navbar bg-base-100 sticky top-0 h-auto"
        >
            <div className="navbar bg-base-100">
                <div className="navbar-start">
                    <button onClick={handleLogo} className="normal-case text-xl">
                        <img src={logo} className='w-16 h-16' alt="Logo" />
                    </button>
                </div>
            </div>
            <div className="navbar-end">
                <button onClick={handleUser}>
                    <img src={userIcon} className='w-14 h-14 mx-5' alt="User" />
                </button>
            </div>

            <UserProfileModal isOpen={isModalOpen} onRequestClose={handleCloseModal} />

        </div>
    );
};

export default Navbar;
