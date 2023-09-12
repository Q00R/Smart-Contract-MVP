import React from 'react';

const Chips = ({ emailList, onRemoveEmail }) => {
    return (
        <div>
            {emailList.map((email, index) => (
                <span key={index} className="inline-flex items-center px-2 py-1 mr-2 mb-3 text-sm font-medium bg-primary text-neutral-focus rounded-2xl">
                    {email}
                    <button
                        type="button"
                        className="inline-flex items-center p-1 ml-2 text-sm text-neutral-focus bg-transparent rounded-sm hover:bg-primary-content hover:text-primary-focus"
                        aria-label="Remove"
                        onClick={() => onRemoveEmail(index)} // Call the onRemoveEmail function with the index
                    >
                        <svg className="w-2 h-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                        </svg>
                        <span className="sr-only">Remove badge</span>
                    </button>
                </span>
            ))}
        </div>
    );
};

export default Chips;
