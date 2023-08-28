import React, { useState } from 'react';
import Modal from 'react-modal';

function OTPVerificationModal({ isOpen, onRequestClose }) {
    const [otp, setOTP] = useState('');
    const [verificationStatus, setVerificationStatus] = useState('');

    const handleOTPChange = (event) => {
        setOTP(event.target.value);
    };

    const handleVerify = async () => {
        try {
            // Send the entered OTP to the server for validation
            const response = await fetch('http://localhost:8000/api/users/verifyOTP/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ otp }),
            });

            const data = await response.json();

            if (data.success) {
                setVerificationStatus('OTP verified successfully!');
                // Proceed with token-based authentication or other actions
            } else {
                setVerificationStatus('Invalid OTP. Please try again.');
            }
        } catch (error) {
            console.error('Error verifying OTP', error);
        }
    };

    return (
        <Modal isOpen={isOpen} onRequestClose={onRequestClose}>
            <h2>OTP Verification</h2>
            <input type="text" value={otp} onChange={handleOTPChange} />
            <button onClick={handleVerify}>Verify OTP</button>
            <p>{verificationStatus}</p>
            <button onClick={onRequestClose}>Close</button>
        </Modal>
    );
}

export default OTPVerificationModal;
