import React from 'react'
import Modal from 'react-modal'

const EditAccountModal = ({ isOpen, onRequestClose }) => {


    const handleEditAccount = async () => {

        //we can edit first name, last name, and phone number

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
                                    <td class="px-2 py-2 text-base-content font-semibold">Phone:</td>
                                    <td class="px-2 py-2">{ }</td>
                                </tr>
                                <tr>
                                    <td class="px-2 py-2 text-base-content font-semibold">Email:</td>
                                    <td class="px-2 py-2">{ }</td>
                                </tr>
                                <tr>
                                    <td class="px-2 py-2 text-base-content font-semibold">National ID:</td>
                                    <td class="px-2 py-2">{ }</td>
                                </tr>
                            </tbody>
                        </table>
                        <div className="flex flex-col space-y-5">
                            <button className='btn btn-primary'>
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