"use client"

import { useEffect, useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function page() {
  const [message, setMessage] = useState("Loading");

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json()
      ).then((data) => setMessage(data.message));
  }, [])

  return (
    <>
      <div className="bg-gray-50 w-dvw h-dvh flex justify-center items-center flex-col gap-8">
        <h1 className="text-black font-extrabold text-7xl">Dog and cat classifier</h1>
        <form className="w-8/12 h-1/4 bg-gray-200 rounded-3xl flex justify-center items-center">
          <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="picture">Picture</Label>
            <Input id="picture" type="file" accept="image/*" />
          </div>
        </form>
        <p className="text-black text-4xl font-bold">{message}</p>
      </div>
    </>
  )
}