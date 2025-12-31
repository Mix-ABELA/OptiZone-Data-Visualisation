# ⚽ OptiZone – Workload Data Visualization

This repository contains a Python-based analytics pipeline for **computing and visualizing player workload in soccer** using **GPS and Heart Rate wearable data**.

The project focuses on transforming raw wearable data into **meaningful workload metrics and visual reports** that can support coaches, performance staff, and analysts in **training monitoring, performance optimization, and injury prevention**.

---

## 📌 Project Context

This project was developed by **Michel Abela** as part of a **Semester Project at EPFL**, in collaboration with the startup **OptiZone**.

The work combines **sports science principles** with **data processing and visualization tools**, aiming to build a modular and deployable workload analysis framework.

📧 Contact: **michel.abela@epfl.ch**

---

## 🎯 Project Objectives

- Compute **external load metrics** from GPS data (distance, speed, accelerations, high-speed running, etc.)
- Compute **internal load metrics** from Heart Rate data (HR zones, TRIMP, recovery indicators)
- Synchronize, clean, and preprocess wearable datasets
- Generate **clear and interpretable visualizations** for training and match analysis
- Design a **modular code architecture** suitable for future deployment on a server or dashboard

---

## 🧠 Sports Science Background

The folder `useful_documents/` contains PDF files summarizing **key sports science concepts** related to workload monitoring, including:
- External vs internal load
- GPS-based performance metrics
- Heart-rate-based workload indicators
- Practical interpretation of training and match demands

These documents provide the scientific foundation behind the metrics implemented in this project.

---

## 🗂 Repository Structure

```
OptiZone-Data-Visualisation/
│
├── requirements.txt           # Python dependencies
|
├── data_samples/              # Dataset storage
│   └── sample_data.csv
│
├── src/                       # source code directory
│   └── optizone_report.py     # Main execution script
│   └── config_params.ini      # Main configuration file (user-defined parameters)
│   └── __init.py__     
│   └── config_handler         # Module: Configuration Library
│   └── csv_handler            # Module: CSV Library
│   └── metrics_handler        # Module: Workload Metrics Library
│   └── plot_handler           # Module: Plotter Library
│
├── useful_documents/          # Sports science reference PDFs
|   └── scientific_researches.pdf
|
└── README.md
```

The codebase is intentionally **modular**, making it:
- Easy to maintain and extend
- Suitable for future integration into a server-based or dashboard application
- Adaptable to new datasets or additional workload metrics

---

## ⚙️ Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/Mix-ABELA/OptiZone-Data-Visualisation.git
cd OptiZone-Data-Visualisation
```

### 2. Install dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Add your dataset
- Place your CSV dataset in the `data_samples/` folder
- The dataset **must contain the same column structure** as the example CSV provided in the repository

---

## 🛠 Configuration

All user-defined parameters are centralized in the file:

```
config_params.ini
```

This file allows users to:
- Select the input dataset
- Adjust speed, acceleration, and HR zone thresholds
- Configure visualization and analysis options

➡️ **No code modification is required** for basic usage — users only need to edit this configuration file.

---

## 📊 Data Requirements

For the pipeline to work correctly, input datasets **must be provided as CSV files** and include the following columns **in the exact order shown below**:

1. Time  
2. Latitude  
3. Longitude  
4. Speed (m/s)  
5. Heart Rate (BPM)  
6. Hacc  
7. Hdop  
8. Quality of Signal  
9. Number of Satellites  
10. Instantaneous Acceleration Impulse  
11. Accl X  
12. Accl Y  
13. Accl Z  
14. Gyro X  
15. Gyro Y  
16. Gyro Z  

⚠️ Column names, order, and units must match the example dataset provided in the repository for the code to function properly.

---

## 🚀 Future Extensions

Possible future developments include:
- Automated session reports (PDF / dashboard)
- Multi-player and multi-session comparison
- Match vs training workload comparison tools
- Integration with web-based visualization platforms
- Injury risk indicators based on workload history

---

## 📄 License & Academic Use

This project was developed for **academic and research purposes** in collaboration with OptiZone.
