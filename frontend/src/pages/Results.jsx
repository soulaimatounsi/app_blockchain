function Results({ data }) {
    if (!data) return null;

    // ✅ Statut final basé sur les résultats ML
    const finalStatus =
        data.all_results &&
            Object.values(data.all_results).some((res) => res?.prediction === 1)
            ? "Vulnerable"
            : "Safe";

    // ✅ Parser et nettoyer le texte LLM
    let llmDisplay = "No LLM result yet";
    if (data.llm_result) {
        try {
            // Si c'est un JSON valide
            const parsed = typeof data.llm_result === "string"
                ? JSON.parse(data.llm_result)
                : data.llm_result;
            llmDisplay = JSON.stringify(parsed, null, 2); // joli formatage
        } catch {
            // Sinon nettoyer les backticks et \n
            llmDisplay = data.llm_result
                .replace(/\\n/g, "\n")
                .replace(/```json/g, "")
                .replace(/```/g, "")
                .trim();
        }
    }

    // ✅ Gestion sécurisée du meilleur score
    const bestScore =
        typeof data.best_score === "number" ? data.best_score.toFixed(2) : "N/A";

    return (
        <div className="card">
            <h3>📊 Analysis Results</h3>

            {/* Best model */}
            <p><strong>Best Model:</strong> {data.best_model || "N/A"}</p>
            <p><strong>Best Score:</strong> {bestScore}</p>

            {/* Status ML */}
            <p>
                <strong>Status:</strong>{" "}
                <span
                    className="badge"
                    style={{
                        padding: "4px 8px",
                        borderRadius: "4px",
                        color: "white",
                        backgroundColor: finalStatus === "Safe" ? "green" : "red",
                    }}
                >
                    {finalStatus}
                </span>
            </p>

            {/* All models results */}
            <h4>Models Comparison</h4>
            <div className="score-grid">
                {data.all_results
                    ? Object.entries(data.all_results).map(([model, res]) => (
                        <div className="score-item" key={model}>
                            <strong>{model}</strong><br />
                            Prediction: {res?.prediction === 1 ? "Vulnerable" : "Safe"}<br />
                            Score: {typeof res?.score === "number" ? res.score.toFixed(2) : "N/A"}
                        </div>
                    ))
                    : "No ML results available."}
            </div>

            {/* LLM report */}
            <h4>LLM Security Analysis</h4>
            <pre
                style={{
                    background: "#f5f5f5",
                    padding: "8px",
                    whiteSpace: "pre-wrap",
                    wordWrap: "break-word",
                }}
            >
                {llmDisplay}
            </pre>

            {/* Blockchain */}
            <h4>Blockchain Trace</h4>
            <p>
                <a href={data.blockchain_link || "#"} target="_blank" rel="noreferrer">
                    View transaction
                </a>
            </p>

            {/* Contract code */}
            <h4>Smart Contract Code</h4>
            <div className="code-box">
                <pre>{data.contract_code || "No contract code."}</pre>
            </div>
        </div>
    );
}

export default Results;
