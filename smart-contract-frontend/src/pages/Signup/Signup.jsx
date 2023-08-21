import React from "react";
import Header from "../../components/Header";
import Signup from "../../components/Signup";
import logo from '../../Assets/logo.png';


export default function SignupPage() {
    return (
        <>
            <Header
                imgSrc={logo}
                heading="Sign up to create an account"
                paragraph="Already have an account? "
                linkName="Login"
                linkUrl="/login"
            />
            <Signup />
        </>
    )
}