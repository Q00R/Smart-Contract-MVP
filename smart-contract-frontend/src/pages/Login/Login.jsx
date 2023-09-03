import React from 'react'
import Header from '../../components/Header'
import Login from '../../components/Login'
import logo from '../../Assets/logo.png'

const LoginPage = () => {
    return (
        <div className='flex flex-col'>
            <div className="container rounded-lg shadow-xl border-2 self-center w-fit h-fit my-5 py-5">
                <Header
                    imgSrc={logo}
                    heading="Login to your account"
                    paragraph="Don't have an account yet? "
                    linkName="Signup"
                    linkUrl="/signup"
                />
                <Login
                />
            </div>
        </div>
    )
}

export default LoginPage;