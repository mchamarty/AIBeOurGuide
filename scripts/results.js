// Wait until the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // 📑 Fetch and Display Input JSON Snippet
    fetch('../data/data_formatted.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-departments').textContent = data?.department_data ? Object.keys(data.department_data).length : 'N/A';
            const inputSnippet = extractJSONSnippet(data);
            document.getElementById('json-input').textContent = JSON.stringify(inputSnippet, null, 2);
        });

    // 📊 Populate Metrics Table
    fetch('../data/results_data.json')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#metrics-table tbody');
            data.metrics_table.forEach((row, index) => {
                tableBody.innerHTML += `
                    <tr>
                        <td>Department ${index + 1}</td>
                        <td>${row.task_repetition_score}</td>
                        <td>${row.workflow_complexity}</td>
                        <td>${row.data_structure_score}</td>
                        <td>${row.communication_frequency}</td>
                        <td>${row.average_sentiment}</td>
                        <td>${row.stakeholder_dependency}</td>
                        <td>${convertTimeSpread(row.time_spread)}</td>
                    </tr>
                `;
            });
        });

    fetch('../data/unique_content.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('unique-content').innerHTML = formatUniqueContent(data.unique_section);
        });
});

function extractJSONSnippet(jsonData) {
    return jsonData?.department_data ? { snippet: jsonData.department_data } : { message: 'No data available' };
}

function convertTimeSpread(seconds) {
    const days = Math.floor(seconds / 86400);
    return `${days} days`;
}

function formatUniqueContent(content) {
    return content.technical_attributes.map(attr => `
        <h4>${attr.title}</h4>
        <p><strong>Tool:</strong> ${attr.tool}</p>
        <ul>${attr.why_special.map(point => `<li>${point}</li>`).join('')}</ul>
        <p><strong>Impact:</strong> ${attr.impact}</p>
    `).join('');
}
;

// 📑 Function: Extract a Snippet from JSON
function extractJSONSnippet(jsonData) {
    if (jsonData?.department_data) {
        const firstKey = Object.keys(jsonData.department_data)[0];
        return { [firstKey]: jsonData.department_data[firstKey] };
    }
    return { message: 'No data available for preview' };
}

// ⏳ Function: Convert Time Spread to Human-Readable Format
function convertTimeSpread(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${days} days, ${hours} hours, ${minutes} minutes`;
}

// 🛠️ Function: Populate "Why Our Model is Unique" Section
function populateWhyUniqueSection(section) {
    const sectionContainer = document.getElementById('why-unique');
    
    // Title and Introduction
    sectionContainer.innerHTML = `
        <h2>${section.title}</h2>
        <p>${section.introduction}</p>
        <hr>
    `;
    
    // Technical Attributes
    sectionContainer.innerHTML += `<h3>🛠️ Advanced Technical Attributes of Our Model</h3>`;
    section.technical_attributes.forEach(attr => {
        sectionContainer.innerHTML += `
            <h4>${attr.title}</h4>
            <ul>
                <li><strong>Tool:</strong> <code>${attr.tool}</code></li>
                <li><strong>Why It’s Special:</strong>
                    <ul>${attr.why_special.map(point => `<li>${point}</li>`).join('')}</ul>
                </li>
                <li><strong>Impact:</strong> ${attr.impact}</li>
            </ul>
        `;
    });
    
    // Combinational Strengths
    sectionContainer.innerHTML += `<h3>🧠 Combinational Strengths</h3><ul>`;
    section.combinational_strengths.forEach(item => {
        sectionContainer.innerHTML += `<li><strong>${item.title}:</strong> ${item.description}</li>`;
    });
    sectionContainer.innerHTML += `</ul>`;
    
    // Competitive Landscape
    sectionContainer.innerHTML += `<h3>🏆 Competitive Landscape: How Do We Compare?</h3><table>`;
    sectionContainer.innerHTML += `
        <thead>
            <tr>
                <th>Feature/Capability</th>
                <th>Our Model</th>
                <th>Competitors</th>
            </tr>
        </thead>
        <tbody>
            ${section.competitive_landscape.comparison_table.map(item => `
                <tr>
                    <td>${item.feature}</td>
                    <td>${item.our_model}</td>
                    <td>${item.competitors}</td>
                </tr>
            `).join('')}
        </tbody>
    `;
    sectionContainer.innerHTML += `</table><p>${section.competitive_landscape.conclusion}</p>`;
    
    // Why Choose Us
    sectionContainer.innerHTML += `<h3>💎 Why Choose Us?</h3><ul>`;
    section.why_choose_us.forEach(point => {
        sectionContainer.innerHTML += `<li>${point}</li>`;
    });
    sectionContainer.innerHTML += `</ul>`;
}

// 📚 Function: Populate Metric Computation Details
function populateMetricDetails() {
    const metricExplanations = `
        <ul>
            <li><strong>Task Repetition Score:</strong> Number of tasks identified.</li>
            <li><strong>Workflow Complexity:</strong> Derived from task interconnections.</li>
            <li><strong>Data Structure Score:</strong> Number of associated documents.</li>
            <li><strong>Communication Frequency:</strong> Total emails + chats.</li>
            <li><strong>Average Sentiment:</strong> NLP-based positivity/negativity score.</li>
            <li><strong>Stakeholder Dependency:</strong> Graph centrality-based interdependence.</li>
            <li><strong>Time Spread:</strong> Temporal analysis between communication timestamps.</li>
        </ul>
    `;
    document.getElementById('metric-explanations').innerHTML = metricExplanations;
}
