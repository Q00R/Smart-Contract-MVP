import React, { useEffect, useState } from 'react';
import UploadPDF from '../../components/UploadPDF';
import Table from '../../components/Table';

const Dashboard = () => {

    return (
        <div className="flex flex-col">
            <div className="self-center w-1/2 my-10">
                <UploadPDF />
            </div>

            <div className="self-center w-full my-5">
                <Table

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
