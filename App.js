import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

function App() {
  const [selectedCompany, setSelectedCompany] = useState('');
  const [predictionData, setPredictionData] = useState(null);

  const niftyCompanies = [
    "ADANIENT", "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV",
    "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT",
    "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR",
    "ICICIBANK", "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI",
    "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", "SBIN", "SUNPHARMA",
    "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "UPL", "ULTRACEMCO", "WIPRO"
  ];
  
  const handleDownloadPDF = () => {
    const downloadButton = document.getElementById('download-button');
    if (downloadButton) {
      downloadButton.style.display = 'none';
    }
  
    const input = document.getElementById('report-section');
    html2canvas(input, {
      useCORS: true,
      scale: 2,
    }).then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
  
      const margin = 10; // 10 mm margin
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const contentWidth = pdfWidth - 2 * margin;
      const contentHeight = pdfHeight - 2 * margin;
  
      const imgWidth = contentWidth;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
  
      const totalPages = Math.ceil(imgHeight / contentHeight);
  
      for (let page = 0; page < totalPages; page++) {
        
        const sourceY = (page * contentHeight * canvas.width) / contentWidth + 23; 
  
        const pageCanvas = document.createElement('canvas');
        pageCanvas.width = canvas.width;
        pageCanvas.height = (contentHeight * canvas.width) / contentWidth;
  
        const ctx = pageCanvas.getContext('2d');
        ctx.drawImage(
          canvas,
          0,
          sourceY,
          canvas.width,
          pageCanvas.height,
          0,
          0,
          canvas.width,
          pageCanvas.height
        );
  
        const pageImgData = pageCanvas.toDataURL('image/png');
  
        if (page > 0) pdf.addPage();
        pdf.addImage(pageImgData, 'PNG', margin, margin, imgWidth, contentHeight);
      }
  
      pdf.save('report.pdf');
  
      if (downloadButton) {
        downloadButton.style.display = 'inline-block';
      }
    });
  };
  

  const handlePredict = () => {
    if (!selectedCompany) {
      alert("Please select a company!");
      return;
    }

    axios.post("http://localhost:5000/predict", { company: selectedCompany })
      .then((response) => {
        setPredictionData(response.data);
      })
      .catch((error) => {
        console.error("Prediction error:", error);
      });
  };

  return (
    <div className="App">
      <h1>📊 Stock Price Predictor (LSTM Model)</h1>

      <label>Select Company: </label>
      <select value={selectedCompany} onChange={(e) => setSelectedCompany(e.target.value)}>
        <option value="">-- Choose --</option>
        {niftyCompanies.map((company) => (
          <option key={company} value={company}>{company}</option>
        ))}
      </select>

      <button onClick={handlePredict}>Predict</button>

      {predictionData && (
        <>
          <div className="result-container" id="report-section">
            <h2>Prediction Report for {predictionData.company}</h2>

            <h3>Stock Price Trend (Next 30 Days)</h3>
            <img
              src={`http://localhost:5000/${predictionData.lineGraph}`}
              alt="Line Graph"
              className="chart"
              crossOrigin="anonymous"
            />

            <h3>Week-wise Price Summary</h3>
            <img
              src={`http://localhost:5000/${predictionData.barGraph}`}
              alt="Bar Graph"
              className="chart"
              crossOrigin="anonymous"
            />

            <h3>Summary of the Report: </h3>
            <pre className="report-text">
              {predictionData.report}
            </pre>

            <h3>Daily Predicted Prices (Next 30 Days)</h3>
            <table className="prediction-table">
              <thead>
                <tr>
                   <th>Day</th>
                  <th>Date</th>
                  <th>Predicted Price (₹)</th>
                </tr>
              </thead>
              <tbody>
                {predictionData.predictions.map((item, index) => {
                  const numericPrice = Number(item.price);
                  const formattedPrice = !isNaN(numericPrice) ? numericPrice.toFixed(2) : 'N/A';
                  const formattedDate = new Date(item.date).toLocaleDateString();

                  return (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{formattedDate}</td>
                      <td>₹{formattedPrice}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

          </div>

          <button id="download-button" onClick={handleDownloadPDF}>Download Report as PDF</button>
        </>
      )}
    </div>
  );
}

export default App;
