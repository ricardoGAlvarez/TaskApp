"use client";
import { useRouter } from "next/navigation";

function TaskCard({ task }) {
  const router = useRouter();

  return (
    <div
      className="bg-slate-800 p-3 hover:bg-slate-600 cursor-pointer 
      rounded-xl border border-gray-300 "
      onClick={() => {
        router.push("/task/edit/" + task.id);
      }}
    >
      <h3 className="font-bold text-center text-2xl text-gray-50">{task.title}</h3>
      <span className="text-gray-200">{task.description}</span>
      <div className="flex justify-end ">
      <span className="text-gray-200">{new Date(task.createdAt).toLocaleDateString()}</span>
      </div>
    </div>
  );
}

export default TaskCard;
