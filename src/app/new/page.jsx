"use client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

function NewPage({ params }) {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (params.id) {
      fetch(`/api/task/${params.id}`)
        .then((res) => res.json())
        .then((data) => {
          setTitle(data.title);
          setDescription(data.description);
        });
    }
  }, []);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (params.id) {
      const res = await fetch(`/api/task/${params.id}`, {
        method: "PUT",
        body: JSON.stringify({ title, description }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
    } else {
      const res = await fetch("/api/task", {
        method: "POST",
        body: JSON.stringify({ title, description }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
    }
    router.push("/");
    router.refresh();

  };
  return (
    <div className="h-screen flex justify-center items-center  ">
      <form
        action=""
        className="bg-slate-700 p-10 w-2/4 border-gray-400 border rounded-xl"
        onSubmit={onSubmit}
      >
        <label htmlFor="title" className="font-bold text-sm">
          Titulo de la tarea
        </label>
        <input
          id="title"
          type="text"
          className="border border-gray-400 p-2 mb-4 w-full rounded-xl text-black"
          placeholder="Titulo"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <label htmlFor="description" className="font-bold text-sm">
          Descipcion de la tarea
        </label>
        <textarea
          name=""
          id="description"
          rows="3"
          value={description}
          className="border border-gray-400 p-2 mb-4 w-full rounded-xl text-black"
          placeholder="Describe la tarea"
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
        <div className="flex justify-between">
          <button
            type="submit"
            className="bg-blue-600  p-3 text-white rounded-xl mx-2"
          >
            Create
          </button>

          {params.id && (
            <button
              type="button"
              className="bg-red-500  p-3 text-white rounded-xl mx-2"
              onClick={async () => {
                const res = await fetch(`/api/task/${params.id}`, {
                  method: "DELETE",
                });
                const data = await res.json();
                router.push("/");
                router.refresh()
              }}
            >
              Delete
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default NewPage;
