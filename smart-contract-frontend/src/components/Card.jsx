import React from 'react'

const Card = ({ imgSrc, cardTitle, cardContent }) => {
    return (
        <div class="flex flex-col xl:flex-row shadow bg-base-200 hover:shadow-md w-full rounded-lg overflow-hidden cursor-pointer">
            <img
                class="object-cover w-full h-48"
                src={imgSrc}
                alt="Flower and sky"
            />

            <div class="relative p-4">
                <h3 class="text-base md:text-xl font-medium text-base-content">
                    {cardTitle}
                </h3>

                <p class="mt-4 text-base md:text-lg text-base-300">
                    {cardContent}
                </p>
            </div>
        </div>
    )
}

export default Card