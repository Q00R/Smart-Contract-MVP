import React from 'react'
import logo from "../Assets/logo.png"
import userIcon from "../Assets/user.png"



const navbar = () => {
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
                    <a href="/" className="normal-case text-xl">
                        <img src={logo} className='w-16 h-16' />
                    </a>
                </div>
            </div>
            <div className="navbar-end">
                <a id="loginIcon" href='/login'>
                    <img src={userIcon} className='w-14 h-14 mx-5' />
                </a>
            </div>
        </div>
    );
}

export default navbar