import React from "react";

import ToggleDarkImage from "../Assets/ToggleDark.png";
import ToggleLightImage from "../Assets/ToggleLight.png"


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

const footer = () => {
    return (
        <div className="flex flex-col mt-32">
            <button
                id="toggleMode"
                onClick={toggleMode}
                className="m-5 w-fit h-fit btn btn-primary self-end"
            >
                <img
                    id="toggleModeIcon"
                    src={ToggleLightImage}
                    alt="moon"
                    className="w-6 h-6"
                />
            </button>
            <footer className="bg-gray-100 dark:bg-base-200">
                <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
                    <p className="mx-auto mt-6 max-w-md text-center leading-relaxed text-gray-500 dark:text-gray-400">
                        <a className="content-center">
                            © 2023 Valify All rights reserved. <br /> Terms · Privacy Policy
                        </a>
                    </p>
                </div>
            </footer>
        </div>
    );
};

export default footer;
