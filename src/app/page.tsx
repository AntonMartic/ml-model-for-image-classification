"use client"

import { ChangeEvent, DragEvent, FormEvent, useEffect, useState } from "react"
import { doc, DocumentData, onSnapshot } from "firebase/firestore";
import { Image } from "lucide-react";
import { db } from "@/components/firebase";

export default function page() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [message, setMessage] = useState("Loading");
  const [data, setData] = useState<DocumentData | undefined>(undefined);

  // useEffect(() => {
  //   const unsub = onSnapshot(doc(db, "classifications", "information"), (doc) => {
  //     setData(doc.data());
  //   });

  //   return () => unsub();
  // }, []);

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("API is offline"));
  }, []);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return setError("Någonting gick fel");

    processFile(e.target.files[0]);
  };

  const handleDrop = (e: DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files.length > 0) {
      processFile(e.dataTransfer.files[0]);
      setIsDragging(false);
    }
  };

  const processFile = (selectedFile: File) => {
    setFile(selectedFile);
    setResult(null);
    setError(null);

    const reader = new FileReader();
    reader.onloadend = () => {
      if (typeof reader.result === "string") {
        setPreview(reader.result);
      }
    };
    reader.readAsDataURL(selectedFile);
  };

  const handleUpload = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) return setError("Vänligen välj en fil");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8080/classify-image", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data.result);
      } else {
        setError(data.error || "Ett fel uppstod");
      }
    } catch {
      setError("Fel vid uppladdning av fil");
    }
  };


  return (
    <>
      <div className="flex flex-col items-center justify-center w-full gap-4 h-svh bg-gray-50">
        <div className="flex flex-col gap-4 justify-center items-center">
          <h1 className="font-extrabold text-black text-7xl">Dog and Cat Classifier</h1>
          <p className="text-4xl font-bold text-black">{message}</p>
        </div>

        {result ? (
          <p>Resultat: {result}</p>
        ) : (
          <form className="flex flex-col items-center justify-center w-full gap-6 h-6/12">
            <label
              className={`flex flex-col items-center justify-center w-6/12 gap-2 text-xl font-medium text-center text-blue-400 transition duration-300 ease-in-out bg-blue-100 h-10/12 rounded-3xl 
            ${preview ? "" : "hover:bg-blue-200 cursor-pointer"}
            ${isDragging ? "bg-blue-200" : ""}`}
              htmlFor="file-upload"
              onDragEnter={() => setIsDragging(true)}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
            >
              {preview ? (
                <>
                  <img src={preview} alt="Preview" className="rounded-md h-9/12 opacity-80" />
                  <button
                    type="button"
                    className="px-8 py-1 text-sm font-medium transition duration-300 ease-in-out bg-red-500 cursor-pointer rounded-xl text-gray-50 hover:bg-red-700"
                    onClick={(e) => {
                      setFile(null);
                      setPreview(null);
                      setResult(null);
                    }}
                  >
                    Välj en annan bild
                  </button>
                </>
              ) : (
                <>
                  <Image className="text-blue-400 w-14 h-14" />
                  Klicka eller dra in en bild för att ladda upp
                </>
              )}
            </label>

            {!preview && (
              <input type="file" id="file-upload" className="hidden" accept="image/png, image/jpeg" onChange={handleFileChange} />
            )}

            <button
              className="py-4 text-xl transition duration-300 ease-in-out bg-blue-400 cursor-pointer px-14 rounded-xl text-gray-50 hover:bg-blue-500"
              type="submit"
              onClick={handleUpload}
            >
              Ladda upp
            </button>
          </form>
        )}
        {error && <p className="text-red-500">{error}</p>}
        <div className="grid grid-cols-2 gap-4">
          <p className="text-left">Totalt antal klassifikationer:</p>
          <p className="text-right">{data ? data.classifications : 0}</p>

          <p className="text-left">Katter:</p>
          <p className="text-right">{data ? data.cat : 0}</p>

          <p className="text-left">Hundar:</p>
          <p className="text-right">{data ? data.dog : 0}</p>

          <p className="text-left">Korrekta klassifikationer:</p>
          <p className="text-right">{data ? data.correctClassifications : 0}</p>

          <p className="text-left">Felaktiga klassifikationer:</p>
          <p className="text-right">{data ? data.wrongClassifications : 0}</p>
        </div>
      </div>
    </>
  );
}