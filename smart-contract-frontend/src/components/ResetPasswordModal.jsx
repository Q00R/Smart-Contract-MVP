import React, { useState } from 'react';
import Modal from 'react-modal'
import Cookies from 'js-cookie';


const ResetPasswordModal = ({ isOpen, onRequestClose, userEmail }) => {

    const [verificationStatus, setVerificationStatus] = useState('');
    const [newPassword, setNewPassword] = useState(''); // Initialize the state
    const [confirmPassword, setConfirmPassword] = useState(''); // Initialize the state

    const handleDigitChange = (event, nextField) => {
        const input = event.target;
        const maxLength = parseInt(input.getAttribute('maxLength'));
        const currentValue = input.value;

        if (currentValue.length >= maxLength) {
            // If the current input is at max length, move focus to the next input
            const nextInput = document.getElementById(nextField);
            if (nextInput) {
                nextInput.focus();
            }
        }
    };

    // Inside the OTPVerificationModal component

    const handleReset = async () => {

        // Collect values from the input fields
        const digit1 = document.getElementById('Digit_1').value;
        const digit2 = document.getElementById('Digit_2').value;
        const digit3 = document.getElementById('Digit_3').value;
        const digit4 = document.getElementById('Digit_4').value;

        // Concatenate the digits into the OTP
        const enteredOTP = digit1 + digit2 + digit3 + digit4 + "";

        console.log(enteredOTP);

        if (newPassword !== confirmPassword) {
            setVerificationStatus('Passwords do not match');
            return;
        }

        try {

            let req = {
                'otp': enteredOTP,
                'password': newPassword
            }

            const response = await fetch('http://localhost:8000/api/users/reset_password/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}`
                },
                body: JSON.stringify(req)
            });
            const data = await response.json();
            console.log(data);
            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
        }

    };

    const sendOTP = async () => {
        try {
            console.log("Sending OTP");

            console.log(Cookies.get('token'));

            const response = await fetch('http://localhost:8000/api/users/email_reset/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}` // Include the token in the custom "Authorization" header
                },
            });
            const data = await response.json();
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <Modal className={'overflow-hidden'} isOpen={isOpen} onRequestClose={onRequestClose}>
            <div className="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div className="relative px-6 pt-10 pb-9 shadow-xl mx-auto w-full max-w-lg rounded-2xl">
                    <div className="mx-auto flex w-full max-w-md flex-col space-y-16">
                        <div className="flex flex-col items-center justify-center text-center space-y-2">
                            <div className="font-semibold text-3xl">
                                <p>Password Reset</p>
                            </div>
                            <div className="flex flex-row text-sm font-medium text-base-content">
                                <p>We have sent a code to your email {userEmail}</p>
                            </div>
                        </div>

                        <div>
                            <form>
                                <div className="flex flex-col space-y-12">
                                    <div className='justify-center space-y-8'>
                                        <div className="space-y-3">
                                            <p className="text-base-content text-xl font-semibold">New Password</p>
                                            <input
                                                className="input input-bordered input-primary w-full max-w-xl"
                                                type="password"
                                                placeholder='Enter new password'
                                                name=""
                                                value={newPassword} // Bind the value to the state
                                                onChange={(event) => setNewPassword(event.target.value)} // Handle change and update the state
                                            />
                                        </div>



                                        <div className="space-y-3">
                                            <p className="text-base-content text-xl font-semibold">Confirm Password</p>
                                            <input
                                                className="input input-bordered input-primary w-full max-w-xl"
                                                type="password"
                                                placeholder='Enter new password'
                                                name=""
                                                value={confirmPassword} // Bind the value to the state
                                                onChange={(event) => setConfirmPassword(event.target.value)} // Handle change and update the state
                                            />
                                        </div>
                                    </div>

                                    <p className="text-base-content self-center text-xl font-semibold">Enter OTP</p>
                                    <div className="flex flex-row items-center justify-between mx-auto w-full max-w-xs">
                                        <div className="w-16 h-16 ">
                                            <input
                                                className="w-full h-full flex flex-col items-center justify-center text-center px-5 outline-none rounded-xl border border-base-300 text-lg bg-base-100 focus:bg-base-200 focus:ring-1 ring-primary-focus"
                                                type="text"
                                                name=""
                                                id="Digit_1"
                                                maxLength="1"
                                                onInput={(event) => handleDigitChange(event, 'Digit_2')}
                                            />
                                        </div>
                                        <div className="w-16 h-16 ">
                                            <input
                                                className="w-full h-full flex flex-col items-center justify-center text-center px-5 outline-none rounded-xl border border-base-300 text-lg bg-base-100 focus:bg-base-200 focus:ring-1 ring-primary-focus"
                                                type="text"
                                                name=""
                                                id="Digit_2"
                                                maxLength="1"
                                                onInput={(event) => handleDigitChange(event, 'Digit_3')}
                                            />
                                        </div>
                                        <div className="w-16 h-16 ">
                                            <input
                                                className="w-full h-full flex flex-col items-center justify-center text-center px-5 outline-none rounded-xl border border-base-300 text-lg bg-base-100 focus:bg-base-200 focus:ring-1 ring-primary-focus"
                                                type="text"
                                                name=""
                                                id="Digit_3"
                                                maxLength="1"
                                                onInput={(event) => handleDigitChange(event, 'Digit_4')}
                                            />
                                        </div>
                                        <div className="w-16 h-16 ">
                                            <input
                                                className="w-full h-full flex flex-col items-center justify-center text-center px-5 outline-none rounded-xl border border-base-300 text-lg bg-base-100 focus:bg-base-200 focus:ring-1 ring-primary-focus"
                                                type="text"
                                                name=""
                                                id="Digit_4"
                                                maxLength="1"
                                            />
                                        </div>
                                    </div>
                                    <div className="flex flex-col space-y-5">
                                        <button onClick={handleReset} className="btn btn-primary w-full max-w-xs self-center">Reset Password</button>
                                        <p className='self-center'>{verificationStatus}</p>
                                        <div className="flex flex-row items-center justify-center text-center text-sm font-medium space-x-1 text-base-content">
                                            <p>Didn't recieve code?</p> <button className="flex flex-row items-center text-primary" onClick={sendOTP}>Resend</button>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
    )
}

export default ResetPasswordModal