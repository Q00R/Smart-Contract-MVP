import React from 'react';
import Cookies from 'js-cookie';

const DownloadButton = ({ documentDownloadId, documentDownloadName, buttonClass }) => {

    const fixedButtonClass = "btn btn-outline btn-ghost "

    const handleDownload = async () => {
        console.log('documentDownloadId', documentDownloadId);
        console.log('documentDownloadName', documentDownloadName);

        try {
            const response = await fetch(`http://localhost:8000/api/documents/${documentDownloadId}/retrieve/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'SID': Cookies.get('token')
                }
            });

            if (response.ok) {
                // Create a blob from the response data
                const blob = await response.blob();

                // Create a temporary URL for the blob
                const url = window.URL.createObjectURL(blob);

                // Create an anchor element to trigger the download
                const a = document.createElement('a');
                a.href = url;
                a.download = documentDownloadName; // Set the desired file name here
                document.body.appendChild(a);
                a.click();

                // Clean up the temporary URL and anchor element
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                console.log('Downloaded', documentDownloadId);
            } else {
                console.error('Failed to download. Status:', response.status);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <button onClick={handleDownload} className={fixedButtonClass + buttonClass}>Download</button>
    )
}

export default DownloadButton;
