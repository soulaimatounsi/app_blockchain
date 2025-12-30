function Results({ data }) {
    if (!data) return null;

    return (
        <div className="card">
            <h3>📊 Analysis Results</h3>

            <p>
                <strong>Model:</strong> {data.modelUsed}
            </p>

            <p>
                <strong>Status:</strong>{" "}
                <span
                    className={`badge ${data.prediction === "Safe" ? "safe" : "vulnerable"
                        }`}
                >
                    {data.prediction}
                </span>
            </p>

            <h4>Model Score</h4>
            <div className="score-grid">
                {Object.entries(data.score).map(([k, v]) => (
                    <div className="score-item" key={k}>
                        {k}
                        <br />
                        {v}
                    </div>
                ))}
            </div>

            <h4>Detected Vulnerabilities</h4>
            <ul className="list">
                {data.detectedVulnerabilities.map((v, i) => (
                    <li key={i}>{v}</li>
                ))}
            </ul>

            <h4>Blockchain Trace</h4>
            <p>
                <strong>Hash:</strong> {data.blockchainTrace.hash}
            </p>
            <p>
                <strong>Transaction:</strong> {data.blockchainTrace.txLink}
            </p>

            <h4>Smart Contract Code</h4>
            <div className="code-box">
                <pre>{data.sourceCode}</pre>
            </div>
        </div>
    );
}

export default Results;
