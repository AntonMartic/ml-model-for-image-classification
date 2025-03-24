import { MainButtonProps } from "./types";

export function MainButton({
  onClick,
  text,
  className,
  value,
}: MainButtonProps) {
  return (
    <button
      className={`py-3 px-8  text-xl sm:py-4 sm:text-xl sm:px-10 transition duration-300 ease-in-out bg-neutral-400 cursor-pointer  rounded-xl text-neutral-50 hover:bg-neutral-500 ${className}`}
      onClick={onClick}
      value={value}>
      {text}
    </button>
  );
}
