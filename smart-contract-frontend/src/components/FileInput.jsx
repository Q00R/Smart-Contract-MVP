import React, { useState } from 'react';

const FileInput = ({ onFileChange }) => {
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        onFileChange(selectedFile);
    };

    return (

        <input type="file" onChange={handleFileChange} className="file-input file-input-bordered file-input-primary w-full" />
    );
};

export default FileInput;
