import { useState } from 'react';
import { loginFields } from "../constants/formFields";
import FormAction from "./FormAction";
import FormExtra from "./FormExtra";
import Input from "./Input";

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
    const authenticateUser = () => {

        //get user details from loginState
        const data = {
            "email": loginState['email-address'],
            "password": loginState['password'],
        }

        // console.log(data)

        //call login API
        fetch('http://localhost:8000/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                console.log(JSON.stringify(data) + " success ")
                console.log(data)
                if (data.token) {
                    console.log(data.token)
                    localStorage.setItem('token', data.token)
                    window.location.href = '/user#dashboard'
                }
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
            </div>
        </form>
    )
}