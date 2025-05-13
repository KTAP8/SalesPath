import React, { useState, ChangeEvent } from "react";
import { Text } from "react-native";
import { Colors } from "@/constants/Colors";

interface NoteBoxProps {
  title?: string; //Optional prop
  textAreawidth?: string; // height and width to define the textbox size
  textAreaheight?: string;
  placeholder?: string;
  note: string;
  setNote: (val: string) => void;
}

const NoteBox: React.FC<NoteBoxProps> = ({
  title = "Problem Notes",
  textAreawidth = "100%",
  textAreaheight = "120px",
  placeholder,
  note,
  setNote,
}) => {
  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setNote(e.target.value);
  };

  return (
    <div style={styles.container}>
      <p style={styles.heading}>{title}</p>
      <textarea
        value={note}
        onChange={handleChange}
        placeholder={placeholder}
        style={{
          ...styles.textarea,
          width: textAreawidth,
          height: textAreaheight,
        }}
      />
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    maxWidth: "500px",
    marginTop: "10px",
    paddingTop: "12px",
  },
  heading: {
    marginBottom: "10px",
    fontFamily: "Lexend",
    fontSize: "14px",
    fontWeight: "600",
    color: Colors.primaryBlue,
  },
  textarea: {
    width: "100%",
    height: "120px",
    padding: "13px",
    fontSize: "14px",
    borderRadius: "8px",
    border: "1px solid #9D9D9D",
    resize: "vertical",
    fontFamily: "Lexend",
  },
};

export default NoteBox;
