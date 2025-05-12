import React, { useState, ChangeEvent } from 'react';

interface NoteBoxProps{
  title?:string; //Optional prop 
  textAreawidth?:string;// height and width to define the textbox size
  textAreaheight?:string;
  placeholder?:string;
}

const NoteBox: React.FC<NoteBoxProps> = ({
  title= "Problem Notes",
  textAreawidth="100%",
  textAreaheight="120px",
  placeholder="Write your notes here... "

}) => {
  const [note, setNote] = useState<string>('');

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setNote(e.target.value);
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>{title}</h3>
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
    fontSize: '16px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    resize: 'vertical',
    fontFamily: 'Lexend'
  },
};

export default NoteBox;
