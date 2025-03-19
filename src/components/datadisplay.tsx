import { DocumentData } from "firebase/firestore";

type DataDisplay = {
    data: DocumentData | undefined;
}

export default function DataDisplay({ data }: DataDisplay) {
    return (
        <div className="grid grid-cols-2 gap-4">
            <p className="text-left font-semibold text-neutral-950">Katter:</p>
            <p className="text-right font-semibold text-neutral-950">{data ? data.cat : 0}</p>

            <p className="text-left font-semibold text-neutral-950">Hundar:</p>
            <p className="text-right font-semibold text-neutral-950">{data ? data.dog : 0}</p>

            <p className="text-left font-semibold text-neutral-950">Korrekta klassifikationer:</p>
            <p className="text-right font-semibold text-green-700">{data ? data.correctClassifications : 0}</p>

            <p className="text-left font-semibold">Felaktiga klassifikationer:</p>
            <p className="text-right font-semibold text-red-700">{data ? data.wrongClassifications : 0}</p>
        </div>
    )
}