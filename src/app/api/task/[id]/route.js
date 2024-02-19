import { NextResponse } from "next/server";
import { prisma } from '@/libs/prisma';


export async function GET(request,{params}){
    const task = await prisma.task.findUnique({
        where:{
            id: Number(params.id)
        }
    })
    return NextResponse.json(task)
}

export async function PUT(request,{params}){
    const data = await request.json()
    const taksUpdated = await prisma.task.update({
        where:{
            id: Number(params.id)
        },
        data:data
    })
    return NextResponse.json(taksUpdated)
}

export async function DELETE(request,{params}){
    try {
        const taksRemoved = await prisma.task.delete({
            where:{
                id: Number(params.id),
            },
        });
        return NextResponse.json(taksRemoved)
    } catch (error) {
        return NextResponse.json(error.message);
    }
}

