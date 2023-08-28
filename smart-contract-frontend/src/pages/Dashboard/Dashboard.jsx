import React, { useEffect, useState } from 'react';
import GeneralBanner from '../../components/GeneralBanner';
import UploadPDF from '../../components/UploadPDF';
import logo from '../../Assets/DocumentImage.jpg';


const Dashboard = () => {



    return (
        <div className='flex flex-col'>


            <div className="container mx-auto px-4 sm:px-8 max-w-3xl">
                <UploadPDF />
            </div>


            <GeneralBanner
                postionOfBanner="lg:order-first"

                propsImage={logo}

                propsImagePref="object-cover"

                propsTitle="Hello Eyadfafasaasfsfsf"

                propsContent="Hello Eyad"



            />


        </div>
    );
};

export default Dashboard;
