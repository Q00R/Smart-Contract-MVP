import React, { useState } from 'react';

const FileInput = ({ onFileChange }) => {
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        onFileChange(selectedFile);
    };

    return (

        <div className="form-control w-full">
            <label className="label">
                <span className="label-text">Pick a file</span>
                <span className="label-text-alt">Alt label</span>
            </label>
            <input onChange={handleFileChange} type="file" className="file-input file-input-bordered w-full" />
            <label className="label">
                <span className="label-text-alt">Alt label</span>
                <span className="label-text-alt">Alt label</span>
            </label>
        </div>

    );
};

export default FileInput;
