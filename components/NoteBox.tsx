import React, { useState, ChangeEvent } from 'react';
import {Text} from 'react-native'

interface NoteBoxProps{
  title?:string; //Optional prop 
  textAreawidth?:string;// height and width to define the textbox size
  textAreaheight?:string;
  placeholder?:string;
  note:string;
  setNote: (val: string) => void;
}

const NoteBox: React.FC<NoteBoxProps> = ({
  title= "Problem Notes",
  textAreawidth="100%",
  textAreaheight="120px",
  placeholder,
  note,
  setNote,

}) => {

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setNote(e.target.value);
  };

  return (
    <div style={styles.container}>
      <h5 style ={styles.heading}>{title}</h5>
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
    maxWidth: '500px',
    margin: '10px',
  },
  heading: {
    marginBottom: '10px',
    fontFamily: 'Lexend',
  },
  textarea: {
    width: '100%',
    height: '120px',
    padding: '10px',
    fontSize: '13px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    resize: 'vertical',
  },
};

export default NoteBox;