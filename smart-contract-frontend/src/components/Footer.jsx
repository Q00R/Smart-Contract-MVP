import React from "react";

const footer = () => {
    return (
        <div className="flex flex-col-reverse">
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
