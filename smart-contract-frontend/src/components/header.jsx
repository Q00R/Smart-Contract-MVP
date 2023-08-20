import { Link } from 'react-router-dom';

export default function Header({
    imgSrc,
    heading,
    paragraph,
    linkName,
    linkUrl = "#"
}) {
    return (
        <div className="mb-10">
            <div className="flex justify-center">
                <img
                    alt=""
                    className="h-14 w-14"
                    src={imgSrc} />
            </div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-primary">
                {heading}
            </h2>
            <p className="mt-5 text-center text-sm text-base-content">
                {paragraph} {' '}
                <Link to={linkUrl} className="font-medium text-secondary hover:text-secondary-focus">
                    {linkName}
                </Link>
            </p>
        </div>
    )
}