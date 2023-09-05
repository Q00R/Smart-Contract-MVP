import React from "react";
import Header from "../../components/Header";
import Signup from "../../components/Signup";
import logo from '../../Assets/logo.png';


export default function SignupPage() {
    return (

        <div className='flex flex-col'>
            <div className="container rounded-lg shadow-xl border-2 self-center w-fit h-fit">
                <Header
                    imgSrc={logo}
                    heading="Sign up to create an account"
                    paragraph="Already have an account? "
                    linkName="Login"
                    linkUrl="/login"
                />
                <Signup />
            </div>
        </div>
    )
}