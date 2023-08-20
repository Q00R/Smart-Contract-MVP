import React from 'react'
import ToggleDarkImage from "../Assets/ToggleDark.png";
import ToggleLightImage from "../Assets/ToggleLight.png"
import logo from "../Assets/logo.jpeg"

function toggleMode() {
    //toggle dark mode and light mode
    document.documentElement.setAttribute(
        "data-theme",
        document.documentElement.getAttribute("data-theme") === "dark"
            ? "light"
            : "dark"
    );
    document.getElementById("toggleModeIcon").src =
        document.documentElement.getAttribute("data-theme") === "dark"
            ? ToggleLightImage
            : ToggleDarkImage;

    localStorage.setItem(
        "theme",
        document.documentElement.getAttribute("data-theme")
    );
}

const navbar = () => {
    return (
        <div
            onLoad={() => {
                document.documentElement.setAttribute(
                    "data-theme",
                    localStorage.getItem("theme")
                );

                if (localStorage.getItem("theme") === "dark") {
                    document.getElementById("toggleModeIcon").src = ToggleLightImage;
                } else {
                    document.getElementById("toggleModeIcon").src = ToggleDarkImage;
                }
            }}
            className="z-50 flex items-center px-2 duration-300 navbar bg-base-100 sticky top-0 h-auto"
        >

            <div className="navbar bg-base-100">
                <div className="navbar-start">
                    <a href="/" className="btn btn-ghost normal-case text-xl">
                        <img src={logo} className='w-14 h-14' />
                    </a>
                </div>
            </div>
            <div className="navbar-end">
                <a className="btn mx-2" href='/login'>Login</a>
                <button
                    id="toggleMode"
                    onClick={toggleMode}
                    className="mx-2 btn btn-primary"
                >
                    <img
                        id="toggleModeIcon"
                        src={ToggleLightImage}
                        alt="moon"
                        className="w-6 h-6"
                    />
                </button>
            </div>
        </div>
    );
}

export default navbar