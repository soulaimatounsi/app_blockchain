export default function MetricsTable({ metrics }) {
    return (
        <table border="1" cellPadding="8">
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1-score</th>
                </tr>
            </thead>
            <tbody>
                {Object.entries(metrics).map(([model, values]) => (
                    <tr key={model}>
                        <td>{model}</td>
                        <td>{values.precision}</td>
                        <td>{values.recall}</td>
                        <td>{values.f1}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
