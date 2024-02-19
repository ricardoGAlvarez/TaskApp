import { prisma } from "@/libs/prisma";
import TaskCard from "@/components/TaskCard"

async function loadTasks() {
  return await prisma.task.findMany();
}


export default async function Home() {
  const tasks = await loadTasks();

  return (
    <section className="container mx-auto items-center flex flex-col md:flex-row">
      <div className="grid gap-3 w-11/12 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 mt-10">
        {tasks.map((task) => (
         <TaskCard task={task} key={task.id}/>
        ))}
      </div>
    </section>
  );
}
