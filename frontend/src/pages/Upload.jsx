import { useState } from "react";
import Results from "./Results";

function Upload() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError("Please select a Solidity (.sol) file.");
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const formData = new FormData();
            formData.append("file", file);

            const res = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                throw new Error("Backend error while analyzing contract");
            }

            const data = await res.json();
            setResult(data);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="card">
                <h2>🔐 Smart Contract Security Analyzer</h2>
                <p>Upload a Solidity (.sol) file to analyze vulnerabilities.</p>

                <form onSubmit={handleSubmit}>
                    <input
                        type="file"
                        accept=".sol"
                        onChange={(e) => setFile(e.target.files[0])}
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? "Analyzing..." : "Analyze"}
                    </button>
                </form>

                {error && <p style={{ color: "red" }}>{error}</p>}
            </div>

            {result && <Results data={result} />}
        </div>
    );
}

export default Upload;
