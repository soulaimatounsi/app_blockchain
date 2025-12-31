function Results({ data }) {
    if (!data || !data.all_results) {
        return null;
    }

    // Déterminer le statut final selon les résultats des modèles
    // Exemple simple : si au moins un modèle prédit "Vulnerable" (1), on considère le contrat vulnérable
    const finalStatus = Object.values(data.all_results).some(
        res => res.prediction === 1
    )
        ? "Vulnerable"
        : "Safe";

    return (
        <div className="card">
            <h3>📊 Analysis Results</h3>

            {/* Best model */}
            <p>
                <strong>Best Model:</strong> {data.best_model}
            </p>
            <p>
                <strong>Best Score:</strong> {data.best_score.toFixed(2)}
            </p>

            {/* Status basé sur les résultats des modèles */}
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
                {Object.entries(data.all_results).map(([model, res]) => (
                    <div className="score-item" key={model}>
                        <strong>{model}</strong>
                        <br />
                        Prediction: {res.prediction === 1 ? "Vulnerable" : "Safe"}
                        <br />
                        Score: {res.score.toFixed(2)}
                    </div>
                ))}
            </div>

            {/* Blockchain */}
            <h4>Blockchain Trace</h4>
            <p>
                <a href={data.blockchain_link} target="_blank" rel="noreferrer">
                    View transaction
                </a>
            </p>

            {/* Contract code */}
            <h4>Smart Contract Code</h4>
            <div className="code-box">
                <pre>{data.contract_code}</pre>
            </div>
        </div>
    );
}

export default Results;
