import { DocumentData } from "firebase/firestore";
import { Dispatch, MouseEvent, SetStateAction } from "react";

export type DBDocumentProps = {
    cat: number,
    dog: number,
    classifications: number,
    correctClassifications: number,
    wrongClassifications: number,
}

export type OutputProps = {
    result: string | null;
    hogVisualization: string | null;
    heatmap: string | null;
}

export type AppStateProps = {
    error: string | null,
    isDragging: boolean,
    message: string,
}

export type ClassificationProps = {
    appState: AppStateProps;
    results: OutputProps;
    dbData: DocumentData | undefined;
    setAppState: Dispatch<SetStateAction<AppStateProps>>;
    setResults: Dispatch<SetStateAction<OutputProps>>;
    setFile: Dispatch<SetStateAction<File | null>>;
    setPreview: Dispatch<SetStateAction<string | null>>;
}

export type DataDisplayProps = {
    data: DocumentData | undefined;
}

export type MainButtonProps = {
    onClick: (event: MouseEvent<HTMLButtonElement>) => void;
    text: string;
}