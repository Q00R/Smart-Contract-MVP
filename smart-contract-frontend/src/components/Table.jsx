import React from 'react'

const Table = (props) => {
    return (
        <div className="overflow-x-auto">
            <table className="table">
                {/* head */}
                <thead>
                    <tr>
                        <th>
                            <label>
                                <input type="checkbox" className="checkbox" />
                            </label>
                        </th>
                        <th>{props.colOneHeader}</th>
                        <th>{props.colTwoHeader}</th>
                        <th>{props.colThreeHeader}</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {/* row 1 */}
                    <tr>
                        <th>
                            <label>
                                <input type="checkbox" className="checkbox" />
                            </label>
                        </th>
                        <td>
                            <div className="flex items-center space-x-3">
                                {props.colOneContent}
                            </div>
                        </td>
                        <td>
                            {props.colTwoContent}
                            <br />
                            <span className="badge badge-ghost badge-sm">Desktop Support Technician</span>
                        </td>
                        <td>{props.colThreeContent}</td>
                        <th>
                            {props.actionButton}
                        </th>
                    </tr>
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
        </div>
    )
}

export default Table