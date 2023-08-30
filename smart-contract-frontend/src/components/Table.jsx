import React, { useEffect, useState } from 'react';
import TableRow from './TableRow';
import Cookies from 'js-cookie';

const Table = (props) => {
    const [selectAll, setSelectAll] = useState(false);
    const [rows, setRows] = useState([
        {
            isChecked: false,
            colOneContent: props.colOneContent,
            colTwoContent: props.colTwoContent,
            colThreeContent: props.colThreeContent,
            actionButton: props.actionButton,
        },
    ]);

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
            actionButton: props.actionButton,
        };

        const updatedRows = [...rows, newRow];
        setRows(updatedRows);
    };


    const loadRows = async () => {

        try {

            fetch('http://localhost:8000/api/users/documents/', {
                method: 'GET',
                headers: {
                    'SID': Cookies.get('token'),
                },
            }).then(response => response.json())
                .then(data => {
                    console.log(data);
                    setRowData(data);
                });
        } catch (error) {
            console.error('Error Loading files:', error);
        }
    };

    useEffect(() => {
        loadRows();
    }, []);

    const setRowData = async (data) => {

        const updatedRows = [...rows];

        for (let i = 0; i < data.length; i++) {
            const newRow = {
                isChecked: false,
                colOneContent: data[i].name,
                colTwoContent: data[i].email,
                colThreeContent: data[i].status,
                actionButton: props.actionButton,
            };
            updatedRows.push(newRow);
        }

        setRows(updatedRows);
    };



    return (
        <div className="overflow-x-auto m-5" onLoad={loadRows}>
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
                <tbody>
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
            {/* TODO just for testing, remove */}
            <button onClick={addRow}>Add Row</button>
        </div>
    );
};

export default Table;
