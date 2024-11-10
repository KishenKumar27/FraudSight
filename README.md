# FraudSight

## About the Project
An advanced AI-driven web application designed to detect, prevent, and mitigate fraudulent activities in real-time. The system leverages LLM to identify suspicious patterns and anomalies, enhancing fraud detection accuracy. It also incorporates reinforcement learning capabilities, allowing the platform to continuously learn and adapt to emerging fraud tactics, thereby improving detection over time.

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

6. To start the application, run:
```zsh
npm start
```