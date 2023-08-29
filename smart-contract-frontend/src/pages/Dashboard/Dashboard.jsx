import React, { useEffect, useState } from 'react';
import UploadPDF from '../../components/UploadPDF';
import Table from '../../components/Table';
import Header from '../../components/Header';
import documentsImage from '../../Assets/documentsImage.png'

const Dashboard = () => {

    return (
        <div className="flex flex-col">

            <div className="container rounded-lg shadow-xl border-2 self-center w-1/2 my-5 p-10">
                <Header
                    // imgSrc={documentsImage}
                    heading="Upload Documents"
                />
                <UploadPDF />
            </div>

            <div className="container rounded-lg shadow-xl border-2 self-center w-full h-full my-5 p-5">
                <Header
                    imgSrc={documentsImage}
                    heading="Documents"
                />

                <Table
                    className="overflow-x-auto"

                    colOneHeader="Name"
                    colTwoHeader="Email"
                    colThreeHeader="Document Status"

                    colOneContent="Document Name"
                    colTwoContent="Shared Email" // Shared Group Emails
                    colThreeContent={<div className="badge badge-success badge-xs"></div>} // Pending, Approved, Rejected

                    actionButton={<button className="btn btn-sm btn-outline btn-ghost">Download</button>}

                />
            </div>

        </div>
    );
};

export default Dashboard;
