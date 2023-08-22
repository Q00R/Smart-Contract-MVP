import React, { useEffect, useState } from 'react'
import { signupFields } from "../constants/formFields"
import FormAction from "./FormAction";
import Input from "./Input";


const fields = signupFields;
let fieldsState = {};

fields.forEach(field => fieldsState[field.id] = '');

export default function Signup() {

    //set the initial state of the form
    const [signupState, setSignupState] = useState(fieldsState);

    //handle input change
    const handleChange = (e) => setSignupState({ ...signupState, [e.target.id]: e.target.value });


    //handle form submission
    const handleSubmit = (e) => {

        const data = {
            first_name: signupState.firstName,
            last_name: signupState.lastName,
            email: signupState.email,
            phone: signupState.phone,
            national_id: signupState.nationalId,
            password: signupState.password,
        }

        console.log(data)

        //prevent the default form behaviour
        // e.preventDefault();

        //log the form data
        // console.log(signupState)

        //call the createAccount function
        // createAccount()
    }

    //handle Signup API Integration here
    const createAccount = () => {
        //talk to the django backend, create a user account

        //if successful, redirect to login page
        //if not, display error message

        //get the data from the form
        const data = {
            first_name: signupState.firstName,
            last_name: signupState.lastName,
            email: signupState.email,
            phone: signupState.phone,
            national_id: signupState['national-id'],
            password: signupState['password'],
        }

        console.log(data)

        //make a post request to the backend
        // fetch('http://localhost:8000/api/users/', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify(data) //convert the data to a JSON string
        // })
        //     .then(response => response.json())
        //     .then(data => {
        //         console.log('Success:', data);
        //         //redirect to login page
        //         window.location.href = '/login'
        //     })
        //     .catch((error) => {
        //         console.error('Error:', error);
        //     });
    }

    return (
        <form className="flex flex-col mt-8 space-y-6">
            <div className="-sspace-y-px self-center">
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
            </div>
        </form>
    )
}