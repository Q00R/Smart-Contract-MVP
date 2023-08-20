import React from 'react'
import Header from '../../components/header'
import Login from '../../components/login'

import logo from '../../Assets/logo.jpeg'

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