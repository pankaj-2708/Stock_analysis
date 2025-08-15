
# 📈 Stock Analysis

A Python-based tool for collecting, analyzing, and visualizing stock market data. This project provides insights into stock performance using historical and live market data.

## 🛠 Tools and Technologies Used

- **Python 3.10+**
- **Libraries**: `pandas`, `numpy`, `matplotlib`, `requests`, `plotly`, `selenium`, `bs4` 
- **Visualization**: Matplotlib and Plotly for plotting stock trends and metrics  
- **Data Handling**: CSV, JSON, and HTML data formats  
- **Web Scraping**: Selenium for fetching dynamic web data  
- **Development Tools**: Streamlit

## 🚀 Features

- Fetch live and historical stock data  
- Visualize stock trends, returns, and comparisons using 65+ plots 
- Save data locally in CSV/HTML formats  
- Simple interface to analyze multiple stocks  
- **Preview Mode**: View sample stock data without fetching live data

> ⚠️ **Warning:** The data displayed in preview mode is **not up to date** and is for demonstration purposes only.
> 🔗 **[Click here to open Preview](https://pankaj-2708.github.io/Stock_analysis/demo/demo.html)** 
## 📂 Project Structure

```
Stock_analysis/
│
├─ main.py             # Main script to run stock analysis
├─ collect_data.py     # Module for fetching stock data
├─ data.html           # Example output of collected data
├─ profile.json        # Configuration or profile settings
├─ com.txt             # List of companies or symbols
├─ requirements.txt    # Python dependencies
├─ Dockerfile          # Optional: containerize the app
└─ README.md           # Project documentation
```

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/pankaj-2708/Stock_analysis.git
cd Stock_analysis
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🧪 Usage

Run the main script to fetch and analyze stock data:

```bash
streamlit run main.py
```

- Ensure `profile.json` and `com.txt` are properly configured.  
- Use **preview mode** to view sample data without connecting to live sources.  
- The results can be visualized directly in Python or saved as HTML/CSV.

## 🤝 Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.
