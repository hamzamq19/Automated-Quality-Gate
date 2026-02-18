# SauceDemo Automation Framework

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![Python](https://img.shields.io/badge/python-3.10+-blue) ![Selenium](https://img.shields.io/badge/selenium-4.x-green)

A modular test automation framework built with **Python**, **Selenium WebDriver**, and **Pytest**. Designed to validate critical workflows on the SauceDemo e-commerce sandbox, demonstrating hybrid API/UI testing patterns and robust error handling.

## Features:

* **Hybrid Execution:** Performs a backend API status check (`HTTP 200`) before initializing the WebDriver to save resources.
* **Smart Waiting:** Utilizes a mix of explicit and implicit waits to handle dynamic elements without hardcoded sleeps.
* **Failure Capture:** Automatically captures and timestamps screenshots upon any test failure for debugging.
* **Data Validation:** Verifies cart calculations and tax logic dynamically rather than just checking for static text.

## Project Structure:

```text
├── tests/
│   ├── test_ticket.py          # Main E2E workflow
├── reports/                    # HTML reports and screenshot artifacts
├── utils/                      # Helper modules
├── requirements.txt            # Project dependencies
└── pytest.ini                  # Pytest configuration

```
## Setup & Usage:

### 1. Installation
Requires Python 3.10+ and Chrome.

```bash
pip install -r requirements.txt
```
### 2. Execution
Run the full test suite:
```bash
pytest
```
To generate the HTML Report:
```bash
pytest --html=reports/report.html --self-contained-html
```
### 3. Reporting
##### Screenshots: Automatically saved to reports/ on failure.
##### HTML Report: Open reports/report.html in your browser to view execution details.

## Author: Hamza Mustafa
