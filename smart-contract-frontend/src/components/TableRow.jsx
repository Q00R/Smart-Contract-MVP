import React from "react";

const TableRow = ({ rowData, index, toggleCheckbox }) => {
    return (
        <tr>
            <th>
                <label>
                    <input
                        type="checkbox"
                        className="checkbox"
                        checked={rowData.isChecked}
                        onChange={() => toggleCheckbox(index)}
                    />
                </label>
            </th>
            <td>
                <div className="flex items-center space-x-3">
                    {rowData.colOneContent}
                </div>
            </td>
            <td>{rowData.colTwoContent}</td>
            <td>{rowData.colThreeContent}</td>
            <th>{rowData.actionButton}</th>
        </tr>
    );
};

export default TableRow;