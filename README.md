# Binance BTC Balance Monitor

A Python-based GUI application that monitors your Bitcoin (BTC) balance on Binance and automatically converts BTC to USDC when a specified threshold is reached.

## Features

- **Live BTC Balance Monitoring:** Fetches your BTC balance and its equivalent USD value from Binance.
- **Threshold-Based Auto-Conversion:** Converts BTC to USDC when the balance exceeds the set target.
- **User-Friendly Interface:** Built using Tkinter for an easy-to-use GUI.
- **Logging System:** Displays real-time logs of balance checks and conversions.
- **Configurable Settings:** Allows users to set the target balance and trim amount.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python libraries:
  ```sh
  pip install binance requests tkinter
  ```
- A Binance API key with trading permissions.

## Setup

1. Clone this repository:
   ```sh
   git clone https://github.com/Muunsparkss/BinanceBitcoinTrimmer.git
   cd BinanceBitcoinTrimmer
   ```

2. Create a `key.json` file and add your Binance API credentials:
   ```json
   {
       "apikey": "your_binance_api_key",
       "seckey": "your_binance_secret_key"
   }
   ```

3. Run the application:
   ```sh
   python main.py
   ```

## Usage

1. **Enter the Target Balance (USD):** This is the threshold at which BTC will be converted to USDC.
2. **Enter the Trim Amount (USD):** The amount of BTC (in USD) to convert when the threshold is reached.
3. **Click "Start Monitoring":** The app will continuously check your balance and convert BTC if needed.
4. **Click "Stop Monitoring":** Stops the balance check and conversion process.

## How It Works

- The application checks your BTC balance every **2 minutes**.
- If the balance exceeds the target, it **sells BTC for USDC** equivalent to the trim amount.
- The target balance is then **updated dynamically** to reflect the new threshold.

## Troubleshooting

- **Error: Connection timeout**  
  - Ensure you have a stable internet connection.
  - Increase the API request timeout in the script.
  
- **Invalid API Key error**  
  - Double-check your `key.json` file and ensure your API keys have the correct permissions.

## Disclaimer

⚠️ **Use this script at your own risk.** Trading cryptocurrencies involves financial risk. Ensure you understand how the Binance API works before using this tool.

## License

This project is licensed under the **MIT License**.

## Author

Developed by **Muunsparkss** 🚀
