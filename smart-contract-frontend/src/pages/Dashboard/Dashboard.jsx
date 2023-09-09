import React, { useEffect, useState } from 'react';
import UploadPDF from '../../components/UploadPDF';
import Table from '../../components/Table';
import Header from '../../components/Header';
import documentsImage from '../../Assets/documentsImage.png'
import uploadImage from '../../Assets/UploadImage.png'
import sharedDocumentsImage from '../../Assets/sharedDocumentIWithMeIcon.png'
import DownloadButton from '../../components/DownloadButton';
import GetDocumentDetailsButton from '../../components/GetDocumentDetailsButton';
import DocumentDetailsModal from '../../components/DocumentDetailsModal';
import Cookies from 'js-cookie';


const Dashboard = () => {
    return (
        <div className="flex flex-col">


            <div className="container rounded-lg shadow-xl border-2 self-center w-1/2 my-5 p-10">
                <Header
                    imgSrc={uploadImage}
                    heading="Upload Documents"
                />
                <UploadPDF />
            </div>

            <div className="container rounded-lg shadow-xl border-2 self-center w-full h-full my-10 p-5">
                <Header
                    imgSrc={documentsImage}
                    heading="My Documents"
                />

                <Table
                    className="overflow-x-auto"

                    colOneHeader="Name"
                    colTwoHeader="Email"
                    colThreeHeader="Document Status"

                    colOneContent="Document Name"
                    colTwoContent="Shared Email" // Shared Group Emails
                    colThreeContent={<div className="badge badge-success badge-xs"></div>} // Pending, Approved, Rejected

                // actionButton_1={<DownloadButton />}
                // actionButton_2={<GetDocumentDetailsButton />}

                />
            </div>



            <div className="container rounded-lg shadow-xl border-2 self-center w-full h-full my-10 p-5">
                <Header
                    imgSrc={sharedDocumentsImage}
                    heading="Documents Shared With Me"
                />

                <Table
                    className="overflow-x-auto"

                    colOneHeader="Name"
                    colTwoHeader="Email"
                    colThreeHeader="Document Status"

                    colOneContent="Document Name"
                    colTwoContent="Shared Email" // Shared Group Emails
                    colThreeContent={<div className="badge badge-success badge-xs"></div>} // Pending, Approved, Rejected

                // actionButton_1={<DownloadButton />}
                // actionButton_2={<GetDocumentDetailsButton />}

                />
            </div>

        </div>



    );
};

export default Dashboard;
