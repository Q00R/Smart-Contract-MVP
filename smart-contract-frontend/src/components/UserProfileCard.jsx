import React from 'react'
import editIcon from '../Assets/EditIcon.png'

const UserprofileCard = () => {
    return (
        <div class="flex flex-col items-center h-screen w-full justify-center">
            <div class="bg-base-200 shadow-xl rounded-lg py-3">
                <h3 class="text-center text-2xl text-base-content font-medium leading-8">John Doe</h3>
                <table class="text-xl my-3 mx-5">
                    <tbody>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">Phone</td>
                            <td class="px-2 py-2">+977 9955221114</td>
                        </tr>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">Email</td>
                            <td class="px-2 py-2">john@exmaple.com</td>
                        </tr>
                        <tr>
                            <td class="px-2 py-2 text-base-content font-semibold">National ID</td>
                            <td class="px-2 py-2">3123131313</td>
                        </tr>
                        <tr>
                            <td>
                                <button className='mt-12 btn-sm btn btn-outline btn-info'>Edit Account</button>
                            </td>
                            <td>
                                <button className='mx-6 mt-12 btn-sm btn btn-outline btn-warning'>Reset Password</button>
                            </td>
                            <td>
                                <button className='mt-12 btn-sm btn btn-outline btn-error'>Deactivate</button>
                            </td>
                        </tr>
                    </tbody></table>
            </div>

        </div >
    )
}

export default UserprofileCard