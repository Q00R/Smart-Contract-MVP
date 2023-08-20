import React from 'react'

const navbar = () => {
    return (

        <div className="navbar bg-base-100">
            <div className="navbar-start">
                <a className="btn btn-ghost normal-case text-xl">daisyUI</a>
            </div>
            <div className="navbar-end">
                <a className="btn" href='/login'>Button</a>
            </div>
        </div>

    );
}

export default navbar