const API_BASE_URL = CONFIG.API_BASE_URL;

const dynamicForm = document.getElementById("dynamicForm");
const resultBox = document.getElementById("resultBox");
const explanationList = document.getElementById("explanationList");
const modelInfoBox = document.getElementById("modelInfoBox");
const backendStatus = document.getElementById("backendStatus");
const modeButtons = document.querySelectorAll(".mode-btn");
const publicCompareSection = document.getElementById("publicCompareSection");
const tickerInput = document.getElementById("tickerInput");
const compareBtn = document.getElementById("compareBtn");
const comparisonBox = document.getElementById("comparisonBox");

let currentMode = "public";
let valuationChart = null;

const sectorOptions = [
  "Technology",
  "Financial Services",
  "Healthcare",
  "Energy",
  "Consumer Defensive",
  "Consumer Cyclical",
  "Industrials",
  "Communication Services",
  "Utilities",
  "Real Estate",
  "Unknown"
];

const publicSampleData = {
  sector: "Technology",
  industry: "Software - Infrastructure",
  total_revenue: 42000000000,
  ebitda: 15000000000,
  net_income: 11000000000,
  total_cash: 9000000000,
  total_debt: 4000000000,
  current_ratio: 1.8,
  debt_to_equity: 35,
  gross_margins: 0.72,
  operating_margins: 0.31,
  profit_margins: 0.26,
  revenue_growth: 0.18,
  earnings_growth: 0.21,
  shares_outstanding: 750000000,
  return_on_assets: 0.12,
  return_on_equity: 0.24,
  trailing_pe: 32,
  forward_pe: 28,
  price_to_book: 8,
  beta: 1.05,
  enterprise_value: 180000000000,
  book_value: 22
};

const privateSampleData = {
  sector: "Industrials",
  industry: "Business Services",
  country: "India",
  annual_revenue: 85000000,
  ebitda: 12000000,
  net_income: 7000000,
  total_cash: 6000000,
  total_debt: 10000000,
  total_assets: 55000000,
  total_liabilities: 20000000,
  shareholders_equity: 35000000,
  gross_margin: 0.42,
  operating_margin: 0.18,
  net_margin: 0.08,
  revenue_growth: 0.14,
  employee_count: 320,
  company_age_years: 11,
  free_cash_flow: 5000000,
  operating_cash_flow: 6500000,
  capex: 1200000,
  customer_count: 180,
  recurring_revenue_ratio: 0.35
};

const startupSampleData = {
  sector: "Technology",
  business_model: "B2B SaaS",
  funding_stage: "Series A",
  country: "India",
  arr: 3200000,
  mrr: 266667,
  revenue_growth: 0.95,
  gross_margin: 0.78,
  burn_rate_monthly: 180000,
  runway_months: 16,
  customer_count: 210,
  churn_rate: 0.035,
  net_revenue_retention: 1.18,
  employee_count: 38,
  cac: 4200,
  ltv: 38000,
  logo_retention: 0.92,
  active_users: 12500,
  arpu: 1280
};

const publicFields = [
  { name: "sector", label: "Sector", type: "select", options: sectorOptions, required: true },
  { name: "industry", label: "Industry", type: "text", required: true },
  { name: "total_revenue", label: "Total Revenue", type: "number", required: true },
  { name: "ebitda", label: "EBITDA", type: "number", required: true },
  { name: "net_income", label: "Net Income", type: "number", required: true },
  { name: "total_cash", label: "Total Cash", type: "number", required: true },
  { name: "total_debt", label: "Total Debt", type: "number", required: true },
  { name: "current_ratio", label: "Current Ratio", type: "number", required: true },
  { name: "debt_to_equity", label: "Debt to Equity", type: "number", required: true },
  { name: "gross_margins", label: "Gross Margins", type: "number", required: true },
  { name: "operating_margins", label: "Operating Margins", type: "number", required: true },
  { name: "profit_margins", label: "Profit Margins", type: "number", required: true },
  { name: "revenue_growth", label: "Revenue Growth", type: "number", required: true },
  { name: "earnings_growth", label: "Earnings Growth", type: "number", required: true },
  { name: "shares_outstanding", label: "Shares Outstanding", type: "number", required: true },
  { name: "return_on_assets", label: "Return on Assets", type: "number", required: false },
  { name: "return_on_equity", label: "Return on Equity", type: "number", required: false },
  { name: "trailing_pe", label: "Trailing P/E", type: "number", required: false },
  { name: "forward_pe", label: "Forward P/E", type: "number", required: false },
  { name: "price_to_book", label: "Price to Book", type: "number", required: false },
  { name: "beta", label: "Beta", type: "number", required: false },
  { name: "enterprise_value", label: "Enterprise Value", type: "number", required: false },
  { name: "book_value", label: "Book Value", type: "number", required: false }
];

const privateFields = [
  { name: "sector", label: "Sector", type: "select", options: sectorOptions, required: true },
  { name: "industry", label: "Industry", type: "text", required: true },
  { name: "country", label: "Country", type: "text", required: true },
  { name: "annual_revenue", label: "Annual Revenue", type: "number", required: true },
  { name: "ebitda", label: "EBITDA", type: "number", required: true },
  { name: "net_income", label: "Net Income", type: "number", required: true },
  { name: "total_cash", label: "Total Cash", type: "number", required: true },
  { name: "total_debt", label: "Total Debt", type: "number", required: true },
  { name: "total_assets", label: "Total Assets", type: "number", required: true },
  { name: "total_liabilities", label: "Total Liabilities", type: "number", required: true },
  { name: "shareholders_equity", label: "Shareholders Equity", type: "number", required: true },
  { name: "gross_margin", label: "Gross Margin", type: "number", required: true },
  { name: "operating_margin", label: "Operating Margin", type: "number", required: true },
  { name: "net_margin", label: "Net Margin", type: "number", required: true },
  { name: "revenue_growth", label: "Revenue Growth", type: "number", required: true },
  { name: "employee_count", label: "Employee Count", type: "number", required: true },
  { name: "company_age_years", label: "Company Age (Years)", type: "number", required: true },
  { name: "free_cash_flow", label: "Free Cash Flow", type: "number", required: false },
  { name: "operating_cash_flow", label: "Operating Cash Flow", type: "number", required: false },
  { name: "capex", label: "CAPEX", type: "number", required: false },
  { name: "customer_count", label: "Customer Count", type: "number", required: false },
  { name: "recurring_revenue_ratio", label: "Recurring Revenue Ratio", type: "number", required: false }
];

const startupFields = [
  { name: "sector", label: "Sector", type: "select", options: sectorOptions, required: true },
  { name: "business_model", label: "Business Model", type: "text", required: true },
  { name: "funding_stage", label: "Funding Stage", type: "text", required: true },
  { name: "country", label: "Country", type: "text", required: true },
  { name: "arr", label: "ARR", type: "number", required: true },
  { name: "mrr", label: "MRR", type: "number", required: true },
  { name: "revenue_growth", label: "Revenue Growth", type: "number", required: true },
  { name: "gross_margin", label: "Gross Margin", type: "number", required: true },
  { name: "burn_rate_monthly", label: "Monthly Burn Rate", type: "number", required: true },
  { name: "runway_months", label: "Runway (Months)", type: "number", required: true },
  { name: "customer_count", label: "Customer Count", type: "number", required: true },
  { name: "churn_rate", label: "Churn Rate", type: "number", required: true },
  { name: "net_revenue_retention", label: "Net Revenue Retention", type: "number", required: true },
  { name: "employee_count", label: "Employee Count", type: "number", required: true },
  { name: "cac", label: "CAC", type: "number", required: false },
  { name: "ltv", label: "LTV", type: "number", required: false },
  { name: "logo_retention", label: "Logo Retention", type: "number", required: false },
  { name: "active_users", label: "Active Users", type: "number", required: false },
  { name: "arpu", label: "ARPU", type: "number", required: false }
];

function formatCurrency(value) {
  if (value === null || value === undefined) return "N/A";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(value);
}

function formatCompactCurrency(value) {
  if (value === null || value === undefined) return "N/A";
  const abs = Math.abs(value);

  if (abs >= 1_000_000_000_000) return `$${(value / 1_000_000_000_000).toFixed(2)}T`;
  if (abs >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(2)}B`;
  if (abs >= 1_000_000) return `$${(value / 1_000_000).toFixed(2)}M`;

  return formatCurrency(value);
}

function getFieldsForMode(mode) {
  if (mode === "public") return publicFields;
  if (mode === "private") return privateFields;
  return startupFields;
}

function getSampleDataForMode(mode) {
  if (mode === "public") return publicSampleData;
  if (mode === "private") return privateSampleData;
  return startupSampleData;
}

function renderField(field) {
  if (field.type === "select") {
    return `
      <div class="form-group">
        <label for="${field.name}">${field.label}</label>
        <select id="${field.name}" name="${field.name}" ${field.required ? "required" : ""}>
          ${field.options.map(option => `<option value="${option}">${option}</option>`).join("")}
        </select>
      </div>
    `;
  }

  return `
    <div class="form-group">
      <label for="${field.name}">${field.label}</label>
      <input
        type="${field.type}"
        id="${field.name}"
        name="${field.name}"
        step="any"
        ${field.required ? "required" : ""}
      />
    </div>
  `;
}

function renderForm(mode) {
  const fields = getFieldsForMode(mode);
  const requiredFields = fields.filter(field => field.required);
  const optionalFields = fields.filter(field => !field.required);

  dynamicForm.innerHTML = `
    <div class="form-grid">
      <div class="section-title">Required Inputs</div>
      <div class="section-subtitle">These fields are needed for the selected valuation mode.</div>
      ${requiredFields.map(renderField).join("")}

      <div class="section-title">Optional Advanced Inputs</div>
      <div class="section-subtitle">These improve detail but are not required.</div>
      ${optionalFields.map(renderField).join("")}
    </div>

    <div class="action-row">
      <button type="submit" class="primary-btn">Run Valuation</button>
      <button type="button" id="fillSampleBtn" class="secondary-btn">Fill Sample Data</button>
      <button type="button" id="resetBtn" class="ghost-btn">Reset</button>
    </div>

    <p class="helper-text">
      ${mode === "public"
        ? "Use this mode for listed public companies."
        : mode === "private"
        ? "Use this mode for established non-listed businesses."
        : "Use this mode for startup / SaaS companies."
      }
    </p>
  `;

  document.getElementById("resetBtn").addEventListener("click", () => {
    dynamicForm.reset();
    resetOutput();
  });

  document.getElementById("fillSampleBtn").addEventListener("click", () => {
    fillSampleData(mode);
  });
}

function fillSampleData(mode) {
  const sampleData = getSampleDataForMode(mode);

  Object.entries(sampleData).forEach(([key, value]) => {
    const input = dynamicForm.querySelector(`[name="${key}"]`);
    if (input) input.value = value;
  });
}

function resetOutput() {
  resultBox.innerHTML = `<p class="muted-text">Choose a mode and submit the form to see the valuation estimate.</p>`;
  explanationList.innerHTML = `<li class="muted-text">No explanation yet.</li>`;
  modelInfoBox.innerHTML = `<p class="muted-text">Model details will appear here.</p>`;
  comparisonBox.innerHTML = `<p class="muted-text">Enter a ticker and compare actual market cap vs model prediction.</p>`;

  if (valuationChart) {
    valuationChart.destroy();
    valuationChart = null;
  }
}

function getFormData(formElement) {
  const formData = new FormData(formElement);
  const payload = {};

  for (const [key, value] of formData.entries()) {
    const inputElement = formElement.querySelector(`[name="${key}"]`);

    if (inputElement && inputElement.tagName === "SELECT") {
      payload[key] = value;
    } else if (value === "") {
      payload[key] = 0;
    } else if (!Number.isNaN(Number(value))) {
      payload[key] = Number(value);
    } else {
      payload[key] = value;
    }
  }

  return payload;
}

function showLoading() {
  resultBox.innerHTML = `<p class="loading-text">Running valuation...</p>`;
}

function showError(message) {
  resultBox.innerHTML = `<p class="error-text">${message}</p>`;
}

function showComparisonError(message) {
  comparisonBox.innerHTML = `<p class="error-text">${message}</p>`;
}

function renderExplanation(points) {
  if (!points || points.length === 0) {
    explanationList.innerHTML = `<li class="muted-text">No explanation available.</li>`;
    return;
  }

  explanationList.innerHTML = points.map(point => `<li>${point}</li>`).join("");
}

function renderModelInfo(info) {
  modelInfoBox.innerHTML = `
    <div>
      <p><strong>Model:</strong> ${info.model_name}</p>
      <p><strong>Target:</strong> ${info.target_name}</p>
      <p><strong>Transform:</strong> ${info.target_transform}</p>
      <div><strong>Notes:</strong></div>
      <ul class="explanation-list">
        ${info.notes.map(note => `<li>${note}</li>`).join("")}
      </ul>
    </div>
  `;
}

function showPublicResult(data) {
  resultBox.innerHTML = `
    <div class="result-success">
      <div class="result-label">Estimated Public Market Capitalization</div>
      <div class="result-main">${formatCurrency(data.predicted_market_cap)}</div>
      <div class="result-sub">${formatCompactCurrency(data.predicted_market_cap)}</div>
      <div class="result-meta">Model used: ${data.model_used}</div>
    </div>
  `;
}

function showPrivateResult(data) {
  resultBox.innerHTML = `
    <div class="result-success">
      <div class="result-label">Estimated Enterprise Value</div>
      <div class="result-main">${formatCurrency(data.estimated_enterprise_value)}</div>
      <div class="result-sub">${formatCompactCurrency(data.estimated_enterprise_value)}</div>
      <div class="result-meta">Band: ${data.valuation_band}</div>
      <div class="result-meta">Model used: ${data.model_used}</div>
    </div>
  `;
}

function showStartupResult(data) {
  resultBox.innerHTML = `
    <div class="result-success">
      <div class="result-label">Estimated Startup Valuation</div>
      <div class="result-main">${formatCurrency(data.estimated_valuation)}</div>
      <div class="result-sub">${formatCompactCurrency(data.estimated_valuation)}</div>
      <div class="result-meta">Band: ${data.valuation_band}</div>
      <div class="result-meta">Model used: ${data.model_used}</div>
    </div>
  `;
}

function getEndpointForMode(mode) {
  if (mode === "public") return `${API_BASE_URL}/public/predict`;
  if (mode === "private") return `${API_BASE_URL}/private/predict`;
  return `${API_BASE_URL}/startup/predict`;
}

function getModelInfoEndpoint(mode) {
  if (mode === "public") return `${API_BASE_URL}/public/model-info`;
  if (mode === "private") return `${API_BASE_URL}/private/model-info`;
  return `${API_BASE_URL}/startup/model-info`;
}

async function fetchModelInfo(mode) {
  const response = await fetch(getModelInfoEndpoint(mode));
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not load model info");
  }

  return data;
}

async function submitPrediction(mode, payload) {
  const response = await fetch(getEndpointForMode(mode), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Prediction failed");
  }

  return data;
}

async function compareTicker(ticker) {
  const response = await fetch(`${API_BASE_URL}/public/compare/${ticker}`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Comparison failed");
  }

  return data;
}

async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();

    if (!response.ok || data.status !== "healthy") {
      throw new Error("Backend is unavailable");
    }

    backendStatus.textContent = "Backend connected";
    backendStatus.classList.add("ok");
    backendStatus.classList.remove("error");
  } catch (error) {
    backendStatus.textContent = "Backend unavailable";
    backendStatus.classList.add("error");
    backendStatus.classList.remove("ok");
  }
}

function showComparisonResult(data) {
  comparisonBox.innerHTML = `
    <div class="comparison-success">
      <div class="comparison-grid">
        <div><strong>Company:</strong> ${data.company_name || "N/A"} (${data.ticker})</div>
        <div><strong>Actual Market Cap:</strong> ${data.actual_market_cap ? formatCurrency(data.actual_market_cap) : "N/A"}</div>
        <div><strong>Predicted Market Cap:</strong> ${formatCurrency(data.predicted_market_cap)}</div>
        <div><strong>Difference:</strong> ${data.difference !== null ? formatCurrency(data.difference) : "N/A"}</div>
        <div><strong>Status:</strong> ${data.comparison_status}</div>
      </div>
    </div>
  `;
}

function renderChart(predictedBillions, actualBillions = null, ticker = "Company") {
  const canvas = document.getElementById("valuationChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  if (valuationChart) {
    valuationChart.destroy();
  }

  const labels = actualBillions !== null
    ? [`Predicted (${ticker})`, `Actual (${ticker})`]
    : ["Predicted Valuation"];

  const values = actualBillions !== null
    ? [predictedBillions, actualBillions]
    : [predictedBillions];

  valuationChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Value (Billions USD)",
          data: values,
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

function togglePublicExtras(mode) {
  if (mode === "public") {
    publicCompareSection.classList.remove("hidden");
  } else {
    publicCompareSection.classList.add("hidden");
  }
}

async function loadModeInfo(mode) {
  try {
    const info = await fetchModelInfo(mode);
    renderModelInfo(info);
  } catch (error) {
    modelInfoBox.innerHTML = `<p class="error-text">Error: ${error.message}</p>`;
  }
}

function handleModeChange(newMode) {
  currentMode = newMode;

  modeButtons.forEach(button => {
    button.classList.toggle("active", button.dataset.mode === newMode);
  });

  renderForm(newMode);
  togglePublicExtras(newMode);
  resetOutput();
  loadModeInfo(newMode);
}

modeButtons.forEach(button => {
  button.addEventListener("click", () => handleModeChange(button.dataset.mode));
});

dynamicForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    showLoading();

    const payload = getFormData(dynamicForm);
    const result = await submitPrediction(currentMode, payload);

    if (currentMode === "public") {
      showPublicResult(result);
      renderChart(result.predicted_market_cap_billions);
    } else if (currentMode === "private") {
      showPrivateResult(result);
      if (valuationChart) {
        valuationChart.destroy();
        valuationChart = null;
      }
    } else {
      showStartupResult(result);
      if (valuationChart) {
        valuationChart.destroy();
        valuationChart = null;
      }
    }

    renderExplanation(result.explanation_points);
  } catch (error) {
    showError(`Error: ${error.message}`);
  }
});

compareBtn.addEventListener("click", async () => {
  const ticker = tickerInput.value.trim().toUpperCase();

  if (!ticker) {
    showComparisonError("Please enter a valid ticker.");
    return;
  }

  comparisonBox.innerHTML = `<p class="loading-text">Comparing with public company data...</p>`;

  try {
    const data = await compareTicker(ticker);
    showComparisonResult(data);
    renderChart(
      data.predicted_market_cap_billions,
      data.actual_market_cap_billions,
      data.ticker
    );
  } catch (error) {
    showComparisonError(`Error: ${error.message}`);
  }
});

togglePublicExtras(currentMode);
renderForm(currentMode);
loadModeInfo(currentMode);
checkBackendHealth();