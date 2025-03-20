import { Dispatch, SetStateAction } from "react";
import { AppStateProps } from "./types";

export const ProcessFile = (
  selectedFile: File,
  setFile: Dispatch<SetStateAction<File | null>>,
  appState: AppStateProps,
  setAppState: Dispatch<SetStateAction<AppStateProps>>,
  setPreview: Dispatch<SetStateAction<string | null>>
) => {
  setFile(selectedFile);
  setAppState({
    ...appState,
    error: null,
  });

  const reader = new FileReader();
  reader.onloadend = () => {
    if (typeof reader.result === "string") {
      setPreview(reader.result);
    }
  };
  reader.readAsDataURL(selectedFile);
};
