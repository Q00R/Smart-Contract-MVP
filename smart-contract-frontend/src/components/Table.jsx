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

    //gets all the user documents
    const getDocuments = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/users/documents/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${Cookies.get('token')}`
                },

            });
            const data = await response.json();
            console.log(data);

            // wait for the data to be set before setting the rows
            setOwnedDocuments((prevOwnedDocuments) => [...prevOwnedDocuments, ...data['user_documents']]);
            setSharedDocuments((prevSharedDocuments) => [...prevSharedDocuments, ...data['shared_documents']]);
            setRowData(); // Call setRowData after data is set
            setIsLoading(false); // Set loading to false here
        } catch (error) {
            console.error('Error Loading files:', error);
        }
    };

    //gets the details of a specific document
    const getDocumentDetails = (documentId) => {

        try {
            fetch('http://localhost:8000/api/documents/' + documentId + '/retrieve_details/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${Cookies.get('token')}`,
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

    const getSharedEmails = (documentId) => {

        try {
            fetch(`http://localhost:8000/api/get-shared/${documentId}/`, {
                method: 'GET',
                headers: {
                    // 'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('token')}`,
                },
            }).then(response => response.json())

                .then(data => {
                    console.log("Shared Emails: ", data);
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

    const setRowData = () => {
        if (props.isOwnedDocumentsTable) {
            console.log('owned documents: ', ownedDocuments);

            // Create rows from the documents
            const newRows = ownedDocuments.map((document, index) => ({
                // 
                isChecked: false,
                colOneContent: document.document_name,
                colTwoContent: 2,
                colThreeContent: 3,
                actionButton_1: (
                    <GetDocumentDetailsButton
                        documentDetails={document}
                        buttonClass="btn btn-outline btn-ghost"
                    />
                ),
                actionButton_2: (
                    <DownloadButton
                        documentDownloadId={document.document_id}
                        documentDownloadName={document.document_name}
                        buttonClass="btn btn-outline btn-ghost"
                    />
                ),
                // Add other properties as needed
            }));

            console.log('new rows: ', newRows);

            setRows(newRows);
        } else {
            // Create rows from the documents
            const newRows = sharedDocuments.map((document, index) => ({
                isChecked: false,
                colOneContent: 1,
                // actionButton_1: actionButton_1,
                // Add other properties as needed
            }));

            setRows(newRows);
        }

        console.log('rows: ', rows);

        setIsLoading(false); // Data loading is complete
    };


    return (
        <div className="flex flex-col overflow-auto m-5">
            {isLoading ? ( // Display loading content if isLoading is true
                <span className="self-center loading loading-spinner text-primary"></span>
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