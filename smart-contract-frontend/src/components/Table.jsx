import React, { useEffect, useState } from 'react';
import TableRow from './TableRow';
import Cookies from 'js-cookie';
import DownloadButton from './DownloadButton';
import GetDocumentDetailsButton from './GetDocumentDetailsButton';

const Table = (props) => {
    const [selectAll, setSelectAll] = useState(false);
    const [rows, setRows] = useState([]);
    const [isLoading, setIsLoading] = useState(true); // Add loading state

    //store the documents that come from the get all user documents request
    const [ownedDocuments, setOwnedDocuments] = useState([]);
    const [sharedDocuments, setSharedDocuments] = useState([]);

    const [actionButton_1, setActionButton_1] = useState();
    const [actionButton_2, setActionButton_2] = useState();


    const toggleSelectAll = () => {
        const updatedRows = rows.map((row) => ({ ...row, isChecked: !selectAll }));
        setSelectAll(!selectAll);
        setRows(updatedRows);
    };

    const toggleCheckbox = (index) => {
        const updatedRows = [...rows];
        updatedRows[index].isChecked = !updatedRows[index].isChecked;
        setRows(updatedRows);
    };

    // Function to add a new row
    const addRow = () => {
        const newRow = {
            isChecked: false,
            colOneContent: props.colOneNewContent, // Modify with your data
            colTwoContent: props.colTwoNewContent,
            colThreeContent: props.colThreeNewContent,
            actionButton_1: props.actionButton_1,
            actionButton_2: props.actionButton_2,
        };

        const updatedRows = [...rows, newRow];
        setRows(updatedRows);
    };


    //gets all the user documents
    const getDocuments = async () => {

        try {
            await fetch('http://localhost:8000/api/users/documents/', {
                method: 'GET',
                headers: {
                    'SID': Cookies.get('token'),
                },
            }).then(response => response.json())
                .then(data => {
                    // Assuming data is an array and contains ownedDocuments and sharedDocuments
                    console.log(data);
                    setOwnedDocuments(data['user_documents']);
                    setSharedDocuments(data['shared_documents']);
                    console.log('owned documents: ', ownedDocuments);
                    console.log('shared documents: ', sharedDocuments);
                    setRowData();
                });
        } catch (error) {
            console.error('Error Loading files:', error);
        }
    };

    //gets the details of a specific document
    const getDocumentDetails = async (documentId) => {

        try {
            fetch('http://localhost:8000/api/documents/' + documentId + '/retrieve_details/', {
                method: 'GET',
                headers: {
                    'SID': Cookies.get('token'),
                },
            }).then(response => response.json())
                .then(data => {
                    console.log(data);
                    return data;
                });
        }
        catch (error) {
            console.error('Error Loading files:', error);
        }
    };

    useEffect(() => {
        getDocuments();
    }, []);

    const setRowData = async () => {
        if (props.isOwnedDocumentsTable) {
            console.log('owned documents: ', ownedDocuments);

            // Create rows from the documents
            const newRows = ownedDocuments.map((document, index) => {

                const actionButton1 = (
                    <GetDocumentDetailsButton
                        documentDetails={document}
                        buttonClass="btn btn-outline btn-ghost"
                    />
                );

                const actionButton2 = (
                    <DownloadButton
                        documentDownloadId={document.document_id}
                        documentDownloadName={document.document_name}
                        buttonClass="btn btn-outline btn-ghost"
                    />
                );

                // sharedEmails = getSharedEmails(document.document_id);

                return {
                    isChecked: false,
                    colOneContent: document.document_name,
                    actionButton_1: actionButton1,
                    actionButton_2: actionButton2,
                    // Add other properties as needed
                };
            });

            setRows(newRows);
        } else {
            // Create rows from the documents
            const newRows = sharedDocuments.map((document, index) => ({
                isChecked: false,
                // colOneContent: document.someProperty,
                // actionButton_1: actionButton_1,
                // Add other properties as needed
            }));

            setRows(newRows);
        }

        setIsLoading(false); // Data loading is complete
    };


    return (
        <div className="overflow-auto m-5" onLoad={getDocuments}>
            {isLoading ? ( // Display loading content if isLoading is true
                <p>Loading...</p>
            ) : (
                <table className="table w-full h-full">
                    {/* head */}
                    <thead>
                        <tr>
                            <th>
                                <label>
                                    <input
                                        type="checkbox"
                                        className="checkbox"
                                        checked={selectAll}
                                        onChange={toggleSelectAll}
                                    />
                                </label>
                            </th>
                            <th>{props.colOneHeader}</th>
                            <th>{props.colTwoHeader}</th>
                            <th>{props.colThreeHeader}</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody className='overflow-y-auto '>
                        {rows.map((rowData, index) => (
                            <TableRow
                                key={index}
                                rowData={rowData}
                                index={index}
                                toggleCheckbox={toggleCheckbox}
                            />
                        ))}
                    </tbody>
                    {/* foot */}
                    <tfoot>
                        <tr>
                            <th></th>
                            <th>{props.colOneHeader}</th>
                            <th>{props.colTwoHeader}</th>
                            <th>{props.colThreeHeader}</th>
                            <th></th>
                        </tr>
                    </tfoot>
                </table>
            )}
        </div>
    );
};

export default Table;