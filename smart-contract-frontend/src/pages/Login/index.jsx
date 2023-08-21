import React from 'react'
import Header from '../../components/Header'
import Login from '../../components/Login'
import logo from '../../Assets/logo.png'

const index = () => {
    return (
        <>
            <Header
                imgSrc={logo}
                heading="Login to your account"
                paragraph="Don't have an account yet? "
                linkName="Signup"
                linkUrl="/signup"
            />
            <Login />
        </>
    )
}

export default index