import { MouseEvent, useState } from "react";
import { ClassificationProps, DBDocumentProps } from "./types"
import { doc, updateDoc } from "firebase/firestore";
import { db } from "./firebase";
import DataDisplay from "./datadisplay";
import { MainButton } from "./mainbutton";

export function ClassificationResult({ appState, results, dbData, setAppState, setResults, setFile, setPreview }: ClassificationProps) {
    const [hasAnswered, setHasAnswered] = useState(false);

    async function Reset() {
        setFile(null);
        setPreview(null);
        setResults({
            result: null,
            hogVisualization: null,
            heatmap: null,
        });
        setAppState({
            ...appState,
            error: null,
        })
        setHasAnswered(true);
    }

    async function AnswerForm(e: MouseEvent<HTMLButtonElement>) {
        e.preventDefault();

        if (!results.result) {
            return
        }

        const value = (e.currentTarget as HTMLButtonElement).value;

        let writeRes: DBDocumentProps = {
            cat: 0,
            dog: 0,
            classifications: 0,
            wrongClassifications: 0,
            correctClassifications: 0,
        }

        if (results.result === "Dog") writeRes.dog += 1;
        else writeRes.cat += 1;

        if (value === "true") {
            writeRes.correctClassifications += 1;
        } else {
            writeRes.wrongClassifications += 1;
        }

        writeRes.classifications += 1;

        const docRef = doc(db, "classifications", "information");
        await updateDoc(docRef, {
            cat: dbData?.cat + writeRes.cat,
            dog: dbData?.dog + writeRes.dog,
            classifications: dbData?.classifications + writeRes.classifications,
            wrongClassifications: dbData?.wrongClassifications + writeRes.wrongClassifications,
            correctClassifications: dbData?.correctClassifications + writeRes.correctClassifications,
        })

        setHasAnswered(true);
    }

    return (
        <>
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
                <DataDisplay data={dbData}
                />
                <MainButton text="Classify another image" onClick={Reset} />
            </div>
        </>
    )
}