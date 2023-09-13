import React, { useEffect, useState } from 'react';
import Card from '../../components/Card';


const HomePage = () => {


    useEffect(() => {

    }, []);


    return (
        <div className="flex flex-col">

            <div className="hero max-h-full bg-base-200">
                <div className="hero-content text-center">
                    <div className="max-w-md">
                        <h1 className="text-3xl font-semibold">Say hello to efficient, secure agreements!</h1>
                        <p className="py-6">Streamline Agreements with Blockchain! Our self-executing smart contracts remove intermediaries, guarantee transparency, and automate transactions.</p>
                        <a href='/signup'><button className="btn btn-primary">Get Started</button></a>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-6 w-full mx-3 my-3">
                <Card />
                <Card />

                <Card />
                <Card />
            </div>
        </div >
    );
};

export default HomePage;
