import axios from "axios";
import "./App.css";
import { useState } from "react";

function App() {
  const [selectedFile, setSelectedFile] = useState();
  const [preData, setPreData]= useState();

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async(event) => {
    event.preventDefault();

    if (!selectedFile) {
      // Handle case when no file is selected
      return;
    }

    let formData = new FormData();
    formData.append("file", selectedFile);

    let res = await axios({
      method: "post",
      url: "http://localhost:8000/predict",
      data: formData,
    });
    if (res.status === 200) {
      setPreData(res.data);
      console.log(res.data);

    }

    
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form> 
      </div>

      <div style={{
        margin:'100px'
      }}>
        {
          preData && <div>
            <p>CLass: {preData.class}</p>
            <p>Confidence: {preData.confidence}</p>
          </div>
        }
      </div>
    </div>
  );
}

export default App;