import Link from 'next/link';

export default function NotFound() {
    return (
        <>
            404 Page Not Found
            <Link href="/">
                <button>Go back Home</button>
            </Link>
        </>
    );
}
