import React from 'react'

export default function FormAction({
    handleSubmit,
    type = 'Button',
    action = 'button',
    text
}) {
    return (
        <>
            {
                type === 'Button' ?
                    <button
                        type={action}
                        className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md btn btn-primary mt-10"
                        onClick={handleSubmit}
                    >

                        {text}
                    </button>
                    :
                    <></>
            }
        </>
    )
}