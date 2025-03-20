"use client"

import { ChangeEvent, DragEvent, FormEvent, MouseEvent, useEffect, useState } from "react"
import { doc, DocumentData, onSnapshot, updateDoc } from "firebase/firestore";
import { Image } from "lucide-react";
import { db } from "@/components/firebase";
import DataDisplay from "@/components/datadisplay";

type DBDocument = {
  cat: number,
  dog: number,
  classifications: number,
  correctClassifications: number,
  wrongClassifications: number,
}

export default function page() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [message, setMessage] = useState("Loading");
  const [data, setData] = useState<DocumentData | undefined>(undefined);
  const [hasAnswered, setHasAnswered] = useState(false);
  const [hogVisualization, setHogVisualization] = useState<string | null>(null);
  const [heatmap, setHeatmap] = useState<string | null>(null);

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
    if (!e.target.files) return setError("Something went wrong");

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
    if (!file) return setError("Please select an image");

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
        setHeatmap(`data:image/png;base64,${data.heatmap}`);
        setHogVisualization(`data:image/png;base64,${data.hog_visualization}`);
      } else {
        setError(data.error || "An error occurred");
      }
    } catch {
      setError("Error when uploading file");
    }
  };

  async function AnswerForm(e: MouseEvent<HTMLButtonElement>) {
    e.preventDefault();

    if (!result) {
      return
    }

    const value = (e.currentTarget as HTMLButtonElement).value;

    let writeRes: DBDocument = {
      cat: 0,
      dog: 0,
      classifications: 0,
      wrongClassifications: 0,
      correctClassifications: 0,
    }

    if (result === "Dog") writeRes.dog += 1;
    else writeRes.cat += 1;

    if (value === "true") {
      writeRes.correctClassifications += 1;
    } else {
      writeRes.wrongClassifications += 1;
    }

    writeRes.classifications += 1;

    const docRef = doc(db, "classifications", "information");
    await updateDoc(docRef, {
      cat: data?.cat + writeRes.cat,
      dog: data?.dog + writeRes.dog,
      classifications: data?.classifications + writeRes.classifications,
      wrongClassifications: data?.wrongClassifications + writeRes.wrongClassifications,
      correctClassifications: data?.correctClassifications + writeRes.correctClassifications,
    })

    setHasAnswered(true);
  }


  return (
    <>
      <div className="flex flex-col items-center justify-center w-full gap-10 h-svh bg-neutral-50">
        <div className="flex flex-col gap-4 justify-center items-center">
          <h1 className="font-extrabold text-neutral-950 text-7xl">Dog and Cat Classifier</h1>
          <p className="text-4xl font-bold text-neutral-950">{message}</p>
          <p className="text-neutral-950">Supported file types: We don't know (Jpeg?, PNG?)</p>
          <p className="text-left font-extrabold">Classifications: {data ? data.classifications : 0}</p>
        </div>
        <div className="flex flex-col items-center justify-center w-full h-fit gap-6">
          <div className={`flex flex-col items-center justify-center w-3xl gap-4 transition duration-300 ${result ? "scale-100 pointer-events-auto" : "scale-0 pointer-events-none h-0"}`}>
            <div className="flex justify-center gap-4">
              <img src={preview ?? undefined} alt="Preview" className="rounded-md h-52" />
              <img src={hogVisualization ?? undefined} alt="HOG Features" className="rounded-md h-52" />
              <img src={heatmap ?? undefined} alt="Heatmap" className="rounded-md h-52" />
            </div>
            <p className="text-3xl font-bold text-neutral-950">Result: {result}</p>
            <div className={`flex flex-col items-center gap-4 transition duration-300 ease-in-out ${hasAnswered ? "scale-0 pointer-events-none h-0 opacity-0" : "scale-100 pointer-events-auto opacity-100"}`}>
              <p>Was this classification correct?</p>
              <div className="grid grid-cols-2 gap-4">
                <button className="py-4 text-xl transition duration-300 ease-in-out bg-neutral-200 cursor-pointer px-14 rounded-xl text-neutral-950 hover:bg-green-500"
                  value={"true"}
                  onClick={AnswerForm}>
                  Yes
                </button>
                <button className="py-4 text-xl transition duration-300 ease-in-out bg-neutral-200 cursor-pointer px-14 rounded-xl text-neutral-950 hover:bg-red-500 hover:text-neutral-50"
                  value={"false"}
                  onClick={AnswerForm}>
                  No
                </button>
              </div>
            </div>
            <div className={`flex flex-col items-center gap-4 transition duration-300 ease-in-out ${hasAnswered ? "scale-100 pointer-events-auto opacity-100" : "scale-0 pointer-events-none h-0 opacity-0"}`}>
              <DataDisplay data={data}
              />
              <button className="py-4 text-xl transition duration-300 ease-in-out bg-neutral-200 cursor-pointer px-14 rounded-xl text-neutral-950 hover:bg-neutral-500"
                onClick={(e) => {
                  setFile(null);
                  setPreview(null);
                  setResult(null);
                  setError(null);
                  setHasAnswered(false);
                }}
              >
                Classify another image
              </button>
            </div>
          </div>
          <div className={`flex flex-col items-center justify-center w-full gap-6 transition duration-100 ease-in-out ${result ? "scale-0 pointer-events-none h-0 opacity-0" : "opacity-100 scale-100 pointer-events-auto h-fit"}`}>
            <label className={`flex flex-col items-center justify-center w-3xl gap-2 font-medium text-center transition duration-300 ease-in-out h-60 rounded-3xl 
                    ${preview ? "text-neutral-100 text-[0rem]" : "hover:bg-neutral-200 cursor-pointer text-neutral-400 text-xl"}
                    ${isDragging ? "!bg-neutral-300" : "bg-neutral-100"}`}
              htmlFor="file-upload"
              onDragEnter={() => setIsDragging(true)}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
            >
              <div className={`flex flex-col gap-2 items-center justify-center transition duration-300 ease-in-out ${preview ? "scale-100 pointer-events-auto h-full" : "scale-0 pointer-events-none h-0"}`}>
                <img
                  src={preview ?? undefined}
                  alt="Preview"
                  className="rounded-md opacity-80 h-9/12"
                />
                <button
                  type="button"
                  className={`px-8 py-1 text-sm font-medium transition duration-100 ease-in-out bg-red-500 cursor-pointer rounded-xl text-neutral-50 hover:bg-red-700 ${preview ? "scale-100 pointer-events-auto" : "scale-0 pointer-events-none h-0 w-0"}`}
                  onClick={() => {
                    setFile(null);
                    setPreview(null);
                    setResult(null);
                  }}
                >
                  Change image
                </button>
              </div>
              <div className={`flex flex-col items-center justify-center gap-2 transition duration-300 ease-in-out ${preview ? "scale-0 pointer-events-none h-0" : "scale-100 pointer-events-auto"}`}>
                <Image className="text-neutral-400 w-14 h-14" />
                Click or drag in an image
              </div>
            </label>

            {!preview && (<input type="file" id="file-upload" className="hidden" accept="image/png, image/jpeg" onChange={handleFileChange} />)}
            <button className="py-4 text-xl transition duration-300 ease-in-out bg-neutral-400 cursor-pointer px-14 rounded-xl text-neutral-50 hover:bg-neutral-500"
              onClick={handleUpload}>
              Classify
            </button>
          </div>
        </div>
        <p className={`text-red-500 transition duration-300 ease-in-out ${error ? "scale-100" : "scale-0"}`}>Error: {error}</p>
      </div>
    </>
  );
}