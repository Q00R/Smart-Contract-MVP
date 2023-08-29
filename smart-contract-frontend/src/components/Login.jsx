import { useState } from 'react';
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
        setLoginState({ ...loginState, [e.target.id]: e.target.value })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        authenticateUser();
    }

    //Handle Login API Integration here
    // Handle Login API Integration here
    const authenticateUser = async () => {
        try {
            // Get user details from loginState
            const input = {
                "email": loginState['email-address'],
                "password": loginState['password'],
            };

            // Call login API
            const response = await fetch('http://localhost:8000/api/users/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(input),
            });

            const data = await response.json();
            console.log(data);

            if (!data.is_activated) {
                console.log("user is not active");
                // Send OTP
                await sendOTP();
            } else {
                console.log("user is active");
                // Redirect to dashboard
                window.location.href = "/dashboard";
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Handle OTP Sending API Integration here
    const sendOTP = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/users/activate/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            console.log(JSON.stringify(data));
            console.log(data);

            // Show OTP verification modal
            // document.getElementById('otp-verification-modal').style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <form className="flex flex-col mt-8 space-y-6">
            <div className="-sspace-y-px self-center w-1/6">
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
                {/* TODO Add I am not robot captcha */}
                <FormAction handleSubmit={handleSubmit} text="Login" />
                <OTPVerificationModal />
            </div>
        </form>
    )
}