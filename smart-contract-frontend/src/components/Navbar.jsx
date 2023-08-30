import React from 'react'
import logo from "../Assets/logo.png"
import userIcon from "../Assets/user.png"
import Cookies from 'js-cookie'



const navbar = () => {

    const handleUser = () => {
        //if there is a user logged in, show the user's profile page
        //else show the login page
        if (Cookies.get('token')) {
            window.location.href = '/profile'
        } else {
            window.location.href = '/login'

        }
    }

    const handleLogo = () => {
        //if there is a user logged in, show the user's dashboard
        //else show the home page
        if (Cookies.get('token')) {
            window.location.href = '/dashboard'
        } else {
            window.location.href = '/'
        }
    }



    return (
        <div
            onLoad={() => {
                document.documentElement.setAttribute(
                    "data-theme",
                    localStorage.getItem("theme")
                );
            }}
            className="z-50 flex items-center px-2 duration-300 navbar bg-base-100 sticky top-0 h-auto"
        >
            <div className="navbar bg-base-100">
                <div className="navbar-start">
                    <a onClick={handleLogo} className="normal-case text-xl">
                        <img src={logo} className='w-16 h-16' />
                    </a>
                </div>
            </div>
            <div className="navbar-end">
                <a onClick={handleUser}>
                    <img src={userIcon} className='w-14 h-14 mx-5' />
                </a>
            </div>
        </div>
    );
}

export default navbar