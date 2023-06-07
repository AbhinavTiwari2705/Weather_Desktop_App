import requests as r
from prettytable import PrettyTable
import tkinter as tk
from tkinter import messagebox
import config
import art
from ttkthemes import ThemedTk
from colorama import init, Fore, Style

init()  # Initialize colorama

def get_weather(city):
    url = f"{config.url}?q={city}&appid={config.api_key}&units=metric"

    try:
        response = r.get(url)
        response.raise_for_status()

        weather_data = response.json()

        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        visibility = weather_data['visibility']

        table = PrettyTable()
        table.field_names = [Fore.GREEN + "Weather Forecast" + Style.RESET_ALL, ""]
        table.add_row(["City", city])
        table.add_row(["Temperature", f"{temperature}°C"])
        table.add_row(["Description", description])
        table.add_row(["Humidity", f"{humidity}%"])
        table.add_row(["Wind Speed", f"{wind_speed} m/s"])
        table.add_row(["Visibility", f"{visibility} m"])

        result_text.delete("1.0", tk.END)  # Clear previous result
        result_text.insert(tk.END, str(table) + "\n\n")
        # result_text.insert(tk.END, art.weather)

    except r.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not get weather data for {city}")
    except KeyError:
        messagebox.showerror("Error", "Invalid response received from the API. Please try again.")

def handle_submit():
    city = city_entry.get()
    if city:
        get_weather(city)
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")

root = ThemedTk(theme="arc")  # Create a themed root window
root.title("Weather Forecast")
root.geometry("500x600")  # Set the window size

frame = tk.Frame(root)
frame.pack(pady=20)

city_label = tk.Label(frame, text="Enter the name of the city:")
city_label.grid(row=0, column=0, padx=10, pady=5)

city_entry = tk.Entry(frame, font=("Arial", 12))
city_entry.grid(row=0, column=1, padx=10, pady=5)

submit_button = tk.Button(frame, text="Get Weather", command=handle_submit)
submit_button.grid(row=1, columnspan=2, padx=10, pady=5)

result_text = tk.Text(root, font=("Courier", 12), wrap="word")
result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

root.mainloop()
