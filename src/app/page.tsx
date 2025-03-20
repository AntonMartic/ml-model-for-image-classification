"use client"

import { ChangeEvent, DragEvent, FormEvent, useEffect, useState } from "react"
import { doc, DocumentData, onSnapshot } from "firebase/firestore";
import { Image } from "lucide-react";
import { db } from "@/components/firebase";
import { AppStateProps, OutputProps } from "@/components/types";
import { ClassificationResult } from "@/components/classification";
import { MainButton } from "@/components/mainbutton";
import { ProcessFile } from "@/components/fileprocessing";

export default function page() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [appState, setAppState] = useState<AppStateProps>({
    error: null,
    isDragging: false,
    message: "Loading...",
  })
  const [dbData, setDBData] = useState<DocumentData | undefined>(undefined);
  const [results, setResults] = useState<OutputProps>({
    result: null,
    hogVisualization: null,
    heatmap: null,
  })

  // useEffect(() => {
  //   const unsub = onSnapshot(doc(db, "classifications", "information"), (doc) => {
  //     setDBData(doc.data());
  //   });

  //   return () => unsub();
  // }, []);

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json())
      .then((data) => setAppState({
        ...appState,
        message: data.message,
      }))
      .catch(() => setAppState({
        ...appState,
        message: "API is offline",
      }));
  }, []);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return setAppState({
      ...appState,
      error: "Something went wrong",
    });

    ProcessFile(e.target.files[0], setFile, appState, setAppState, setPreview);
  };

  const handleDrop = (e: DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files.length > 0) {
      ProcessFile(e.dataTransfer.files[0], setFile, appState, setAppState, setPreview);
      setAppState({
        ...appState,
        isDragging: false,
      });
    }
  };

  const handleUpload = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) return setAppState({
      ...appState,
      error: "Please select an image",
    });

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8080/classify-image", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setResults({
          result: data.result,
          heatmap: `data:image/png;base64,${data.heatmap}`,
          hogVisualization: `data:image/png;base64,${data.hog_visualization}`,
        })
      } else {
        setAppState({
          ...appState,
          error: data.error || "An error occurred",
        });
      }
    } catch {
      setAppState({
        ...appState,
        error: "Error when uploading file",
      });
    }
  };

  function Reset() {
    setFile(null);
    setPreview(null);
    setResults({
      result: null,
      hogVisualization: null,
      heatmap: null,
    });
    setAppState({
      ...appState,
      isDragging: false,
      error: null,
    })
  }

  return (
    <>
      <div className="flex flex-col items-center justify-center w-full gap-10 h-svh bg-neutral-50">
        <div className="flex flex-col gap-4 justify-center items-center">
          <h1 className="font-extrabold text-neutral-950 text-7xl">Dog and Cat Classifier</h1>
          <p className="text-4xl font-bold text-neutral-950">{appState.message}</p>
          <p className="text-neutral-950">Supported file types: We don't know (Jpeg?, PNG?)</p>
          <p className="text-left font-extrabold">Classifications: {dbData ? dbData.classifications : 0}</p>
        </div>
        <div className="flex flex-col items-center justify-center w-full h-fit gap-6">
          <div className={`flex flex-col items-center justify-center w-3xl gap-4 transition duration-300 ${results.result ? "scale-100 pointer-events-auto" : "scale-0 pointer-events-none h-0"}`}>
            <div className="flex justify-center gap-4">
              <img src={preview ?? undefined} alt="Preview" className="rounded-md h-52" />
              <img src={results.hogVisualization ?? undefined} alt="HOG Features" className="rounded-md h-52" />
              <img src={results.heatmap ?? undefined} alt="Heatmap" className="rounded-md h-52" />
            </div>
            <p className="text-base font-medium text-neutral-950">Dark blue: Less important for the classification, Red: More important for the classification</p>
            <p className="text-3xl font-bold text-neutral-950">Result: {results.result}</p>
            <ClassificationResult appState={appState} results={results} dbData={dbData} setAppState={setAppState} setResults={setResults} setFile={setFile} setPreview={setPreview} />
          </div>
          <div className={`flex flex-col items-center justify-center w-full gap-6 transition duration-100 ease-in-out ${results.result ? "scale-0 pointer-events-none h-0 opacity-0" : "opacity-100 scale-100 pointer-events-auto h-fit"}`}>
            <label className={`flex flex-col items-center justify-center w-3xl gap-2 font-medium text-center transition duration-300 ease-in-out h-60 rounded-3xl 
                    ${preview ? "text-neutral-100 text-[0rem]" : "hover:bg-neutral-200 cursor-pointer text-neutral-400 text-xl"}
                    ${appState.isDragging ? "!bg-neutral-300" : "bg-neutral-100"}`}
              htmlFor="file-upload"
              onDragEnter={() => setAppState({ ...appState, isDragging: true })}
              onDragLeave={() => setAppState({ ...appState, isDragging: false })}
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
                  onClick={Reset}
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
            <MainButton text="Classify" onClick={handleUpload} />
          </div>
        </div>
        <p className={`text-red-500 transition duration-300 ease-in-out ${appState.error ? "scale-100" : "scale-0"}`}>Error: {appState.error}</p>
      </div>
    </>
  );
}