import Link from "next/link";

function Navbar() {
    return (
        <div className="bg-slate-500 h-20 items-center ">
            <div className="p-4 flex justify-end w-full">
                <Link
                href="/new"
                className="bg-blue-600 p-3  rounded-xl"
                >Create Task</Link>
            </div>
        </div>
    );
}

export default Navbar;