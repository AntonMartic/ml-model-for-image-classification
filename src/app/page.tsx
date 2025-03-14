"use client"

import { useEffect, useState } from "react"

function page() {
  const [message, setMessage] = useState("Loading");

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json()
      ).then((data) => setMessage(data));
  }, [])

  return (
    <div>{message}</div>
  )
}

export default page