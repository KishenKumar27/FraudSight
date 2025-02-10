# FraudSight

## About the Project
An advanced AI-driven web application designed to detect, prevent, and mitigate fraudulent activities in real-time. The system leverages LLM to identify suspicious patterns and anomalies, enhancing fraud detection accuracy. It also incorporates reinforcement learning capabilities, allowing the platform to continuously learn and adapt to emerging fraud tactics, thereby improving detection over time.


## Project Structure

- **`chatbot/`**: Contains components and logic for chatbot integration.
- **`fraud-chatbot/`**: Merges chatbot features with fraud detection functionality.
- **`.DS_Store`**: MacOS directory metadata (should be ignored).
- **`.gitignore`**: Specifies intentionally untracked files to ignore.
- **`FraudSight.pdf`**: Documentation related to the fraud detection system.
- **`README.md`**: This file, providing details about the project setup and usage.
- **`data_migration.py`**: Script to manage data migration between systems.
- **`docker-compose.yaml`**: Defines the MySQL database service for the project, including persistent storage and user credentials.
- **`fraud_detection.py`**: Main fraud detection logic and rules implementation.
- **`fraud_parameters.json`**: Contains the parameters and rules for identifying suspicious transactions.
- **`fraud_parameters.py`**: Supporting script for managing fraud detection parameters.
- **`mysql_native_func.py`**: Provides a comprehensive list of MySQL operators and functions for reference.
- **`package-lock.json`**: Dependency lock file for npm.
- **`requirements.txt`**: Lists the Python dependencies for the project.


## Features

- **Fraud Detection Rules:**
  - Transaction Amount Threshold
  - Transaction Frequency
  - IP Address Consistency
  - Transaction Time Patterns
  - Unusual Currency Patterns
  - Account Age and Activity Level
- **Database Management:** Utilizes MySQL with structured and persistent data storage.
- **Containerization:** Simplified deployment using Docker.
- **Extensibility:** The system supports adding new fraud parameters dynamically.


## Prerequisites
1. To set up the project for development, first install the necessary dependencies and activate your virtual environment.
```zsh
pip install -r requirements.txt
```

2. Install all the required packages listed in the package.json file which is inside fraud-chatbot foler.
```zsh
npm install
```


## Installation

1. Run the MySQL Container
In the directory where you saved your docker-compose.yml file, run:
```zsh
docker-compose up -d
```
2. Migrate the data into the MySQL Container
```zsh
python3 data-migration.py
```

3. Run the python files in the following order:
```zsh
python3 fraud_detection.py
python3 fraud_parameters.py
```

4. Locate to the chatbot folder
```zsh
cd chatbot
```

5. Run the following python file in the chatbot folder
```zsh
python3 bot.py
```

6. To start the front-end React application, run:
```zsh
cd fraud-chatbot/
npm install
npm start
```

### Configuration

#### Environment Variables
Sensitive configurations are defined in the `docker-compose.yaml` file. Update these variables as needed:
- `MYSQL_ROOT_PASSWORD`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

#### Fraud Parameters
Modify or add new detection rules in the `fraud_parameters.json` file. Each rule includes:
- **ID:** A unique identifier.
- **Parameter:** Name of the rule.
- **Description:** Details of what the rule monitors.
- **Example:** A practical example illustrating the rule.

Example rule:
```json
{
    "id": 1,
    "parameter": "Transaction Amount Threshold",
    "description": "Flag transactions that exceed a specified amount or fall within an unusual range.",
    "example": "Transactions above $10,000 or below $1 may be flagged."
}
```


## Reference

### MySQL Functions and Operators
A detailed list of MySQL operators and functions is available in `mysql_native_func.py`.


## Contribution
Contributions are welcome! Please fork the repository and submit a pull request with your changes.


## License
This project is not under any license yet.
