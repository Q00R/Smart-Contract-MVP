import React from 'react'

export default function FormExtra() {
    return (
        <div className="flex flex-col justify-between ">
            <div className="flex">
                <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    className="h-4 w-4 text-primary focus:ring-primary-focus border-gray-300 rounded"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-base-content">
                    Remember me
                </label>
            </div>
            <div className="text-sm">
                <a href="#" className="font-medium text-secondary hover:text-secondary-focus">
                    Forgot your password?
                </a>
            </div>
        </div >

    )
}