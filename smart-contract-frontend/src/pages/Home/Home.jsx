import React, { useEffect, useState } from 'react';


const HomePage = () => {

    const [message, setMessage] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/api/example/')  // Update with your Django API endpoint
            .then(response => response.json())
            .then(data => setMessage(data.message))
            .catch(error => console.error('Error:', error));
    }, []);


    return (
        <div className="flex flex-col">

            <h1 className="text-2xl self-center">Home content here</h1>
            <div>
                <p>Response from Django: {message}</p>
            </div>
        </div>
    );
};

export default HomePage;
