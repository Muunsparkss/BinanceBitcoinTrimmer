import time
import json
import threading
import tkinter as tk
from tkinter import messagebox
from binance.client import Client
from requests.exceptions import ConnectionError

# Load API credentials from config.json
with open('key.json', 'r') as file:
    config = json.load(file)
    api_key = config['apikey']
    api_secret = config['seckey']

# Initialize Binance client with timeout
client = Client(api_key, api_secret, requests_params={"timeout": 20})

class BTCMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BTC Balance Monitor")
        self.root.geometry("400x400")
        
        self.running = False
        
        # UI Elements
        tk.Label(root, text="Target Balance (USD):").pack()
        self.target_entry = tk.Entry(root)
        self.target_entry.pack()
        self.target_entry.insert(0, "510")
        
        tk.Label(root, text="Trim Amount (USD):").pack()
        self.trim_entry = tk.Entry(root)
        self.trim_entry.pack()
        self.trim_entry.insert(0, "10")
        
        self.balance_label = tk.Label(root, text="Current BTC Balance: Fetching...", font=("Arial", 12))
        self.balance_label.pack()
        
        self.log_box = tk.Text(root, height=10, width=50)
        self.log_box.pack()
        
        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack()
    
    def log_message(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
    
    def get_btc_balance_in_usd(self):
        try:
            btc_balance = float(client.get_asset_balance(asset='BTC')['free'])
            btc_price = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
            return btc_balance * btc_price
        except ConnectionError as e:
            self.log_message(f"Connection error: {e}")
            return None
    
    def convert_btc_to_usdc(self, amount_in_usd):
        try:
            btc_price = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
            btc_amount = amount_in_usd / btc_price
            order = client.order_market_sell(symbol='BTCUSDC', quantity=round(btc_amount, 6))
            self.log_message(f"Converted ${amount_in_usd} of BTC to USDC: {order}")
        except ConnectionError as e:
            self.log_message(f"Connection error during conversion: {e}")
    
    def monitor_balance(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        while self.running:
            target_balance = float(self.target_entry.get())
            trim_amount = float(self.trim_entry.get())
            
            current_balance = self.get_btc_balance_in_usd()
            if current_balance is not None:
                self.balance_label.config(text=f"Current BTC Balance: ${current_balance:.2f}")
                self.log_message(f"Current BTC Balance: ${current_balance:.2f}")
                
                if current_balance >= target_balance:
                    self.log_message("Threshold reached. Converting BTC to USDC...")
                    self.convert_btc_to_usdc(trim_amount)
                    self.target_entry.delete(0, tk.END)
                    self.target_entry.insert(0, str(target_balance + trim_amount))
            else:
                self.log_message("Could not retrieve BTC balance. Skipping this check.")
            
            time.sleep(120)  # Wait for 2 minutes before next check
    
    def start_monitoring(self):
        threading.Thread(target=self.monitor_balance, daemon=True).start()
    
    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_message("Monitoring stopped.")

# Run the application
root = tk.Tk()
app = BTCMonitorApp(root)
root.mainloop()
