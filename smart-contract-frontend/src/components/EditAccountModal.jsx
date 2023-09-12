import React, { useState } from 'react';
import Modal from 'react-modal';
import Cookies from 'js-cookie';

const EditAccountModal = ({ isOpen, onRequestClose }) => {
    const user = JSON.parse(localStorage.getItem('user'));
    const [nameArray, setNameArray] = useState([user.firstname, user.lastname]);
    const [phone, setPhone] = useState(user.phone_number);



    const handleEditAccount = async () => {
        // Update the user object with the new first name and last name
        const updatedUser = {
            firstname: nameArray[0],
            lastname: nameArray[1],
            phone_number: phone,
        };

        console.log(updatedUser);

        try {
            const response = await fetch('http://localhost:8000/api/users/Edit/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    "SID": Cookies.get('token'), // Include the token in the custom "SID" header
                },
                body: JSON.stringify(updatedUser),
            });
            const data = await response.json();
            console.log(data)
            //wait for data to be returned
            user.firstname = updatedUser.firstname;
            user.lastname = updatedUser.lastname;
            user.phone_number = updatedUser.phone_number;
            localStorage.setItem('user', JSON.stringify(user));
            onRequestClose();
        } catch (error) {
            console.error('Error updating user', error);
        }
    };

    const handleNameChange = (event) => {
        const newName = event.target.value;
        // Split the new name into first name and last name based on the space character
        const nameParts = newName.split(' ');
        // Ensure we have at least two parts (first name and last name)
        if (nameParts.length >= 2) {
            setNameArray(nameParts);
        } else {
            // Handle the case when there are not enough name parts
            setNameArray([newName, '']);
        }
    };

    return (

        <Modal className={'overflow-hidden'} isOpen={isOpen} onRequestClose={onRequestClose}>
            <div className="relative flex min-h-screen flex-col justify-center overflow-hidden bg-base-100 py-12">
                <div className="relative px-6 pt-10 pb-9 shadow-xl mx-auto w-full max-w-lg rounded-2xl">
                    <button onClick={onRequestClose} className="btn btn-accent btn-sm">
                        back
                    </button>
                    <div className="mx-auto flex w-full max-w-md flex-col space-y-16">
                        <div className="flex flex-col items-center justify-center text-center space-y-2">
                            <div className="font-semibold text-3xl">
                                <p>Edit Account</p>
                            </div>
                            <div className="flex flex-row text-sm font-medium text-base-content">
                                <p>Please enter your <span className='font-bold'>new</span> account information</p>
                            </div>
                        </div>

                        <table className="text-2xl my-10 mx-5">
                            <tbody>
                                <tr>
                                    <td className="px-2 py-2 text-base-content font-semibold">
                                        Name: <input
                                            type="text"
                                            placeholder="Enter Name"
                                            className="my-3 input input-bordered input-info w-full max-w-xs"
                                            value={nameArray.join(' ')} // Join first name and last name with a space
                                            onChange={handleNameChange} // Handle changes in the name input
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="px-2 py-2 text-base-content font-semibold">
                                        Phone: <input
                                            type="text"
                                            placeholder="Enter Phone Number"
                                            className="my-3 input input-bordered input-info w-full max-w-xs"
                                            value={phone}
                                            onChange={(e) => setPhone(e.target.value)} // Handle changes in the phone input
                                        />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div className="flex flex-col space-y-5">
                            <button className="btn btn-primary" onClick={handleEditAccount}>
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
    )
}

export default EditAccountModal