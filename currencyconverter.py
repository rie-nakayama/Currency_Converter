import requests
import customtkinter as ctk
import re
from datetime import datetime


class RealTimeCurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']
        self.last_updated = self.data.get('time_last_update_utc', 'Unknown Date')


    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        #first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        # limiting the precision to 4 decimal places 
            amount = round(amount * self.currencies[to_currency], 4) 
        return amount

class App(ctk.CTk):
    def __init__(self, converter):
        super().__init__()
        self.title('Currency Converter')
        self.geometry("500x300")
        self.configure(fg="#420217")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
    
        self.currency_converter = converter
        
        #Label
        
        self.intro_label = ctk.CTkLabel(self, text = 'Convert currency in real-time', font=('Inter', 18, 'bold'))
        self.intro_label.pack(pady=10)
        
        self.date_label = ctk.CTkLabel(self, text=f"1 JPY = {self.currency_converter.convert('JPY', 'USD', 1)} USD \n Last Updated: {self.currency_converter.last_updated}")
        self.date_label.pack()

        # Entry Fields
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Enter Amount")
        self.amount_entry.pack(pady=10)
        
        # Dropdowns
        self.from_currency = ctk.CTkComboBox(self, values=list(self.currency_converter.currencies.keys()))
        self.from_currency.set("JPY")
        self.from_currency.pack(pady=2)
        
        self.to_currency = ctk.CTkComboBox(self, values=list(self.currency_converter.currencies.keys()))
        self.to_currency.set("USD")
        self.to_currency.pack()
        
        # Convert Button
        self.convert_button = ctk.CTkButton(self, text="Convert", command=self.perform_conversion)
        self.convert_button.pack(pady=10)
        
        # Result Label
        self.result_label = ctk.CTkLabel(self, text="Converted Amount: ")
        self.result_label.pack()


    def perform_conversion(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
            self.result_label.configure(text=f"Converted Amount: {converted_amount} {to_curr}")
        except ValueError:
            self.result_label.configure(text="Invalid Input!")

if __name__ == '__main__':
    url = 'https://open.er-api.com/v6/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    app = App(converter)
    app.mainloop()