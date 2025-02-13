import React, { useState } from "react";
import axios from "axios";

export default function ResumeScanner() {
    const [file, setFile] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [skills, setSkills] = useState([]);
    const [matchScore, setMatchScore] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please upload a file.");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);
        
        try {
            const response = await axios.post("http://localhost:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            setSkills(response.data.skills);
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    const handleMatch = async () => {
        if (!jobDescription) {
            alert("Please enter a job description.");
            return;
        }
        
        try {
            const response = await axios.post("http://localhost:5000/match", {
                job_description: jobDescription,
                skills: skills,
            });
            setMatchScore(response.data.match_scores);
        } catch (error) {
            console.error("Error matching resume:", error);
        }
    };

    return (
        <div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
            <h1 className="text-2xl font-bold mb-4">AI-Powered Resume Scanner</h1>
            
            <input type="file" onChange={handleFileChange} className="mb-2" />
            <button onClick={handleUpload} className="px-4 py-2 bg-blue-500 text-white rounded">Upload Resume</button>
            
            {skills.length > 0 && (
                <div className="mt-4 p-4 bg-white shadow-md rounded">
                    <h2 className="text-lg font-semibold">Extracted Skills:</h2>
                    <p className="text-gray-700">{skills.join(", ")}</p>
                </div>
            )}
            
            <textarea
                placeholder="Enter Job Description"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                className="mt-4 w-2/3 p-2 border rounded"
            />
            
            <button onClick={handleMatch} className="mt-2 px-4 py-2 bg-green-500 text-white rounded">Match Resume</button>
            
            {matchScore && (
                <div className="mt-4 p-4 bg-white shadow-md rounded">
                    <h2 className="text-lg font-semibold">Match Scores:</h2>
                    <pre className="text-gray-700">{JSON.stringify(matchScore, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}
