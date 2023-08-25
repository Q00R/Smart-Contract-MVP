import React, { useEffect, useState } from 'react'
import { signupFields } from "../constants/formFields"
import FormAction from "./FormAction";
import Input from "./Input";
import OTPVerificationModal from './OTP';


const fields = signupFields;
let fieldsState = {};

fields.forEach(field => fieldsState[field.id] = '');

export default function Signup() {

    //set the initial state of the form
    const [signupState, setSignupState] = useState(fieldsState);


    //set the initial state of the modal
    const [isModalOpen, setIsModalOpen] = useState(false);

    //handle input change
    const handleChange = (e) => setSignupState({ ...signupState, [e.target.id]: e.target.value });


    //handle form submission
    const handleSubmit = (e) => {



        //prevent the default form behaviour
        e.preventDefault();

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
        //talk to the django backend, create a user account

        //if successful, redirect to login page
        //if not, display error message

        //get the data from the form
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
                // After successful signup, open the OTP modal
                setIsModalOpen(true);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    return (
        <form className="flex flex-col mt-8 space-y-6">
            <div className="-sspace-y-px self-center w-1/6">
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
                <FormAction handleSubmit={handleSubmit} text="Signup" />

                <OTPVerificationModal isOpen={isModalOpen} onRequestClose={handleCloseModal} />
            </div>
        </form>
    )
}