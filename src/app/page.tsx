"use client"

import { ChangeEvent, useEffect, useState } from "react"
import { Image, X } from "lucide-react";

export default function page() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const [message, setMessage] = useState("Loading");

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json()
      ).then((data) => setMessage(data.message));
  }, [])

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) {
      setError("Någonting gick fel")
      return
    }

    const selectedFile = e.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();

      reader.onloadend = () => {
        if (typeof reader.result === 'string') {
          setPreview(reader.result);
        }
      };

      // Läs in filen som en URL
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch('http://localhost:8080/classify-image', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data.result);
        setError(null);
      } else {
        setResult(null);
        setError(data.error || "An error occurred");
      }
    } catch (error) {
      setError("Error uploading the file.");
    }
  };

  return (
    <>
      <div className="flex flex-col items-center justify-center w-full gap-8 h-svh bg-gray-50">
        <h1 className="font-extrabold text-black text-7xl">Dog and cat classifier</h1>
        <p className="text-4xl font-bold text-black">{message}</p>
        {result
          ? <p>Result: {result}</p>
          : <form className="flex flex-col items-center justify-center w-full gap-6 h-6/12" onSubmit={handleUpload}>
            <label className={`flex flex-col items-center justify-center w-6/12 gap-2 text-xl font-medium text-center text-blue-400 transition duration-300 ease-in-out bg-blue-100 h-10/12 rounded-3xl 
            ${preview ? '' : 'hover:bg-blue-200 cursor-pointer'}`}
              htmlFor="file-upload">
              {preview
                ?
                <>
                  <img src={preview} alt="Preview" className="rounded-md h-9/12 opacity-80" />
                  <button type="button" className="px-8 py-1 text-sm font-medium transition duration-300 ease-in-out bg-red-500 cursor-pointer rounded-xl text-gray-50 hover:bg-red-700"
                    onClick={() => setPreview(null)}>Välj en annan bild</button>
                </>
                :
                <>
                  <Image className="text-blue-400 w-14 h-14" />
                  Klicka eller dra in en bild för att ladda upp
                </>
              }
            </label>
            {!preview && (
              <input type="file" id="file-upload" className="hidden appearance-none" accept="image/png, image/jpeg" onChange={handleFileChange} />
            )}
            <button className="py-4 text-xl transition duration-300 ease-in-out bg-blue-400 cursor-pointer px-14 rounded-xl text-gray-50 hover:bg-blue-500"
              type="submit">Ladda upp</button>
          </form>}
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      </div>
    </>
  )
}