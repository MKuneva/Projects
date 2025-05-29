# Project Setup and Usage Guide

This guide provides step-by-step instructions to set up the project, install dependencies, and run the application.

## Prerequisites

- Python installed on your system.

## Installation Steps

1. **Create a Virtual Environment**  
   Create a virtual environment to keep your project dependencies isolated.

   python -m venv venv

   ## Activate the virtual environment

   Windows
   .\venv\Scripts\activate

   macOS/Linux
   source venv/bin/activate

2. **Install the dependencies**
   pip install panel pandas folium geopandas

3. **Run the app**
   panel serve app.py
