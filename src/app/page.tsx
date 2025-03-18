"use client"

import { useEffect, useState } from "react"
import { Image } from "lucide-react";

export default function page() {
  const [message, setMessage] = useState("Loading");

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json()
      ).then((data) => setMessage(data.message));
  }, [])

  return (
    <>
      <div className="flex flex-col items-center justify-center gap-8 bg-gray-50 w-dvw h-dvh">
        <h1 className="font-extrabold text-black text-7xl">Dog and cat classifier</h1>
        <form className="flex items-center justify-center w-8/12 bg-blue-100 h-1/4 rounded-3xl">
          <label className="flex flex-col items-center justify-center w-full h-full gap-2 text-xl font-medium text-center text-blue-500 cursor-pointer"
            htmlFor="file-upload">
            <Image className="w-14 h-14" />
            Ladda upp en bild
          </label>
          <input type="file" id="file-upload" className="hidden appearance-none" />
        </form>
        <p className="text-4xl font-bold text-black">{message}</p>
      </div>
    </>
  )
}