import React from 'react'

const UserprofileCard = () => {
    return (
        <div class="flex items-center h-screen w-full justify-center">

            <div class="max-w-xl">
                <div class="bg-base-200 shadow-xl rounded-lg py-3">
                    <div class="p-2">
                        <h3 class="text-center text-2xl text-neutral font-medium leading-8">John Doe</h3>
                        <div class="text-center text-base-content text-lg font-semibold">
                            <p>Web Developer</p>
                        </div>
                        <table class="text-xl my-3">
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
                            </tbody></table>

                        <div class="text-center my-3">
                            <a class="text-xl text-primary italic hover:text-primary-focus font-medium" href="#">View Profile</a>
                        </div>

                    </div>
                </div>
            </div>

        </div>
    )
}

export default UserprofileCard