import { DataDisplayProps } from "./types";

export default function DataDisplay({ data }: DataDisplayProps) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <p className="self-center pl-4 text-left font-semibold text-neutral-950">Katter:</p>
      <p className="self-center pr-4 text-right font-semibold text-neutral-950">
        {data ? data.cat : 0}
      </p>

      <p className="self-center pl-4 text-left font-semibold text-neutral-950">Hundar:</p>
      <p className="self-center pr-4 text-right font-semibold text-neutral-950">
        {data ? data.dog : 0}
      </p>

      <p className="self-center pl-4 text-left font-semibold text-neutral-950">
        Korrekta klassifikationer:
      </p>
      <p className="self-center pr-4 text-right font-semibold text-green-700">
        {data ? data.correctClassifications : 0}
      </p>

      <p className="self-center pl-4 text-left font-semibold">Felaktiga klassifikationer:</p>
      <p className="self-center pr-4 text-right font-semibold text-red-700">
        {data ? data.wrongClassifications : 0}
      </p>
    </div>
  );
}
