import React, { useEffect, useState } from 'react';
import UploadPDF from '../../components/UploadPDF';


const Dashboard = () => {



    return (
        <div className="flex flex-col">

            <div className="self-center">
                <UploadPDF />
            </div>

        </div>
    );
};

export default Dashboard;
