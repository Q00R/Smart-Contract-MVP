import React, { useEffect, useState } from 'react'
import { signupFields } from "../constants/formFields"
import FormAction from "./FormAction";
import Input from "./Input";
import OTPVerificationModal from './OTPVerificationModal';
import Cookies from 'js-cookie';


const fields = signupFields;
let fieldsState = {};

fields.forEach(field => fieldsState[field.id] = '');

export default function Signup() {

    //set the initial state of the form
    const [signupState, setSignupState] = useState(fieldsState);

    const [error, setError] = useState(''); // Added error state

    //set the initial state of the modal
    const [isModalOpen, setIsModalOpen] = useState(false);

    //handle input change
    const handleChange = (e) => setSignupState({ ...signupState, [e.target.id]: e.target.value });


    //handle form submission
    const handleSubmit = (e) => {



        //prevent the default form behaviour
        e.preventDefault();

        // Check for missing inputs
        const missingInputs = fields.filter(
            (field) => field.isRequired && !signupState[field.id]
        );

        if (missingInputs.length > 0) {
            // Display an error message for missing inputs
            setError('Please fill in all required fields.');
            return; // Prevent further processing
        }

        // Clear any previous errors
        setError('');

        //log the form data
        console.log(signupState)

        //call the createAccount function
        createAccount()
    }

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    //handle Signup API Integration here
    const createAccount = () => {
        const data = {
            "firstname": signupState['first-name'],
            "lastname": signupState['last-name'],
            "email": signupState['email-address'],
            "password": signupState['password'],
            "nid": signupState['national-id'],
            "phone number": signupState['phone-number'],
        }

        //if password and confirm password do not match, display error message
        if (signupState['password'] !== signupState['confirm-password']) {
            console.log('Passwords do not match')
            return
        }

        console.log(data)

        //make a post request to the backend
        fetch('http://localhost:8000/api/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) //convert the data to a JSON string
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                if (data['error']) {
                    setError(data['error']);
                    return;
                }
                login();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const login = async () => {
        //login the user and redirect to the dashboard
        await fetch('http://localhost:8000/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "email": signupState['email-address'], "password": signupState['password'] }) //convert the data to a JSON string
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                let user = {
                    "user_id": data.user.user_id,
                    "email": data.user.email,
                    "firstname": data.user.firstname,
                    "lastname": data.user.lastname,
                    "nid": data.user.nid,
                    "phone_number": data.user.phone_number,
                    "is_activated": data.is_activated,
                }
                localStorage.setItem('user', JSON.stringify(user));
                Cookies.set('token', data.token.access, { expires: 1 / 24 });
                sendOTP();
            }
            )
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const sendOTP = async () => {
        try {
            console.log("Sending OTP");

            console.log(Cookies.get('token'));

            const response = await fetch('http://localhost:8000/api/users/activate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}`,
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

        <form className="flex flex-col space-y-10 px-20 m-12 h-fit">
            <div className="self-center w-full">
                {
                    fields.map(field =>
                        <Input
                            key={field.id}
                            handleChange={handleChange}
                            value={signupState[field.id]}
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
                <FormAction handleSubmit={handleSubmit} text="Sign up" />
                {error && <div className="text-red-500">{error}</div>} {/* Display error message */}
                <OTPVerificationModal isOpen={isModalOpen} onRequestClose={handleCloseModal} userEmail={signupState['email-address']} />
            </div>
        </form>
    )
}