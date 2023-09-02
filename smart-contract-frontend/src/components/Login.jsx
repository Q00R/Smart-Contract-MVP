import React, { useState } from 'react';
import Cookies from 'js-cookie';

import { loginFields } from "../constants/formFields";
import FormAction from "./FormAction";
import FormExtra from "./FormExtra";
import Input from "./Input";
import OTPVerificationModal from './OTPVerificationModal';

const fields = loginFields;
let fieldsState = {};
fields.forEach(field => fieldsState[field.id] = '');

export default function Login() {


    const [loginState, setLoginState] = useState(fieldsState);

    const handleChange = (e) => {
        setLoginState({ ...loginState, [e.target.id]: e.target.value });
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        await authenticateUser();
    }

    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const authenticateUser = async () => {
        try {
            const input = {
                "email": loginState['email-address'],
                "password": loginState['password'],
            };

            const response = await fetch('http://localhost:8000/api/users/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(input),
            });

            const data = await response.json();
            console.log(data);

            // save user info in local storage
            localStorage.setItem('user', JSON.stringify(data.user));

            //set cookie expiration to 1 hour
            Cookies.set('token', data.token['token'], { expires: 1 / 24 });

            if (!data.is_activated) {
                console.log("user is not active");
                await sendOTP();
            } else {
                console.log("user is active");
                window.location.href = "/dashboard";
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const sendOTP = async () => {
        try {
            console.log("Sending OTP");

            console.log(Cookies.get('token'));

            const response = await fetch('http://localhost:8000/api/users/activate/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    "SID": Cookies.get('token'), // Include the token in the custom "SID" header
                },
            });

            const data = await response.json();
            console.log(JSON.stringify(data));
            console.log(data);

            // Show OTP verification modal
            setIsModalOpen(true);


        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <form className="flex flex-col mt-8 space-y-6 p-12 m-10">
            <div className="-sspace-y-px self-center w-full">
                {
                    fields.map(field =>
                        <Input
                            key={field.id}
                            handleChange={handleChange}
                            value={loginState[field.id]}
                            labelText={field.labelText}
                            labelFor={field.labelFor}
                            id={field.id}
                            name={field.name}
                            type={field.type}
                            isRequired={field.isRequired}
                            placeholder={field.placeholder}
                        />

                    )
                }
                <FormExtra />
                <FormAction handleSubmit={handleSubmit} text="Login" />
                <OTPVerificationModal isOpen={isModalOpen} onRequestClose={handleCloseModal} userEmail={loginState['email-address']} />
            </div>
        </form>
    )
}
