"use client"

import { useEffect, useState } from "react"

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
        <p className="text-black text-4xl font-bold">{message}</p>
      </div>
    </>
  )
}