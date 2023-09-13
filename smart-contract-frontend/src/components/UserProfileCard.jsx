import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import OTPVerificationModal from './OTPVerificationModal';
import EditAccountModal from './EditAccountModal';
import ResetPasswordModal from './ResetPasswordModal';

const UserprofileCard = ({ isOpen, onRequestClose }) => {
    const [isActivated, setIsActivated] = useState(localStorage.getItem('user').is_activated); // Initialize the state

    const isActivatedClassName = 'mr-5 mt-12 w-auto btn-sm btn btn-outline btn-success';
    const isActivatedText = 'Activate';
    const isDeactivatedClassName = 'mr-5 mt-12 w-auto btn-sm btn btn-outline btn-error';
    const isDeactivatedText = 'Deactivate';

    const [isVerifyModalOpen, setisVerifyModalOpen] = useState(false);
    const [isEditAccountModalOpen, setisEditAccountModalOpen] = useState(false);
    const [isResetPasswordModalOpen, setisResetPasswordModalOpen] = useState(false);

    const handleCloseVerifyModal = () => {
        setisVerifyModalOpen(false);
    };

    const handleCloseResetPasswordModal = () => {
        setisResetPasswordModalOpen(false);
    };

    const handleOpenResetPasswordModal = () => {
        setisResetPasswordModalOpen(true);
    };

    const handleCloseEditAccountModal = () => {
        setisEditAccountModalOpen(false);
    };

    const handleOpenEditAccountModal = () => {
        setisEditAccountModalOpen(true);
    };

    const handleDeactivate = async () => {

        console.log(localStorage.getItem('user'));

        try {
            const response = await fetch('http://localhost:8000/api/users/deactivate/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}`, // Include the token in the custom "Authorization" header
                },
            });
            const data = await response.json();
            console.log(data);

            if (data['message'] === 'Account is deacivated') {
                setIsActivated(false); // Update the state when deactivated

                //save the updated user info in local storage
                const user = JSON.parse(localStorage.getItem('user'));
                user.is_activated = false;
                localStorage.setItem('user', JSON.stringify(user));

                //redirect to dashboard
                window.location.href = "/dashboard";
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleActivate = async () => {

        try {
            console.log("Sending OTP");

            console.log(Cookies.get('token'));

            const response = await fetch('http://localhost:8000/api/users/activate/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}`, // Include the token in the custom "Authorization" header
                },
            });

            const data = await response.json();
            console.log(JSON.stringify(data));
            console.log(data);

            //save the updated user info in local storage
            const user = JSON.parse(localStorage.getItem('user'));
            user.is_activated = true;
            localStorage.setItem('user', JSON.stringify(user));


            // Show OTP verification modal
            setisVerifyModalOpen(true);

        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleSendResetPassword = async () => {
        try {
            console.log("Sending OTP");

            console.log(Cookies.get('token'));

            const response = await fetch('http://localhost:8000/api/users/email_reset/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}`, // Include the token in the custom "Authorization" header
                },
            });
            const data = await response.json();
            setisResetPasswordModalOpen(true);

        } catch (error) {
            console.error('Error:', error);
        }
    }

    const user = JSON.parse(localStorage.getItem('user'));
    useEffect(() => {
        // Check the user's activation status from localStorage when the component mounts
        setIsActivated(user.is_activated);
    }, []);

    return (
        <div className="flex flex-col items-center justify-center">
            <div className="bg-base-200 shadow-xl rounded-lg py-3">
                <button onClick={onRequestClose} className="ml-3 btn btn-accent btn-sm">
                    back
                </button>
                <h3 className="text-center text-2xl text-base-content font-medium leading-8">
                    {user.firstname + " " + user.lastname}
                </h3>
                <table className="text-2xl my-10 mx-5">
                    <tbody>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">Email:</td>
                            <td class="px-2 py-2">{user.email}</td>
                        </tr>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">Phone:</td>
                            <td class="px-2 py-2">{user.phone_number}</td>
                        </tr>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">National ID:</td>
                            <td class="px-2 py-2">{user.nid}</td>
                        </tr>
                        <tr>
                            <td>
                                <button onClick={handleOpenEditAccountModal} className='mr-5 mt-12 w-auto btn-sm btn btn-outline btn-info'>Edit Account</button>
                            </td>
                            <td>
                                <button onClick={handleSendResetPassword} className='mr-5 mt-12 w-auto btn-sm btn btn-outline btn-warning'>Reset Password</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <button
                                    onClick={isActivated ? handleDeactivate : handleActivate}
                                    className={isActivated ? isDeactivatedClassName : isActivatedClassName}
                                >
                                    {isActivated ? isDeactivatedText : isActivatedText}

                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <OTPVerificationModal isOpen={isVerifyModalOpen} onRequestClose={handleCloseVerifyModal} userEmail={user.email} />
                <EditAccountModal isOpen={isEditAccountModalOpen} onRequestClose={handleCloseEditAccountModal} />
                <ResetPasswordModal isOpen={isResetPasswordModalOpen} onRequestClose={handleCloseResetPasswordModal} userEmail={user.email} />
            </div>
        </div>
    );
};

export default UserprofileCard;
