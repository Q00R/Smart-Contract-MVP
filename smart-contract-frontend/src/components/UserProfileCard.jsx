import React from 'react'

const UserprofileCard = () => {

    const user = JSON.parse(localStorage.getItem('user'));
    return (
        <div class="flex flex-col items-center justify-center">
            <div class="bg-base-200 shadow-xl rounded-lg py-3">
                <h3 class="text-center text-2xl text-base-content font-medium leading-8">{
                    user.firstname + " " + user.lastname
                }</h3>
                <table class="text-xl my-10 mx-5">
                    <tbody>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">Phone</td>
                            <td class="px-2 py-2">{user.phone_number}</td>
                        </tr>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">Email</td>
                            <td class="px-2 py-2">{user.email}</td>
                        </tr>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">National ID</td>
                            <td class="px-2 py-2">{user.nid}</td>
                        </tr>
                        <tr>
                            <td>
                                <button className='mr-5 mt-12 w-auto btn-sm btn btn-outline btn-info'>Edit Account</button>
                            </td>
                            <td>
                                <button className='mr-5 mt-12 w-auto btn-sm btn btn-outline btn-warning'>Reset Password</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <button className='mr-5 mt-12 w-auto btn-sm btn btn-outline btn-error'>Deactivate</button>
                            </td>
                        </tr>
                    </tbody></table>
            </div>

        </div >
    )
}

export default UserprofileCard