import React, { useState } from 'react';
import Input from './Input';
import Chips from './Chips';

const EmailInput = ({ emailList, setEmailList }) => {
    const [newEmail, setNewEmail] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewEmail(value); // Update the newEmail state only

        // You can also update the email list state here if needed,
        // but it won't add emails immediately on input change.
        console.log(emailList);
    };

    const addEmail = () => {
        if (newEmail.trim() === '') {
            return;
        }

        setEmailList((prev) => ({
            ...prev,
            email: [...prev.email, newEmail],
        }));

        setNewEmail('');

        console.log(emailList);
    };

    const handleRemoveEmail = (index) => {
        // Create a copy of the email list and remove the email at the specified index
        const updatedEmailList = [...emailList.email];
        updatedEmailList.splice(index, 0);

        // Update the email list state
        setEmailList((prev) => ({
            ...prev,
            email: updatedEmailList,
        }));
    };

    return (
        <div>
            <Chips emailList={emailList.email} onRemoveEmail={handleRemoveEmail} />
            <Input
                key={"email"}
                handleChange={handleChange}
                value={newEmail}
                labelText={"Email Address"}
                labelFor={"email-address"}
                id={"email"}
                name={"email"}
                type={"email"}
                isRequired={false}
                placeholder={"Enter email address to share the document with"}
            />
            <div className="flex justify-center">
                <button onClick={addEmail} className="my-3 self-center btn btn-primary">
                    Add
                </button>
            </div>
        </div>
    );
};

export default EmailInput;
