import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io


# Step 1: Create main window
root = tk.Tk()
root.title("Weather Dashboard 🌦️")
root.geometry("400x300")
root.configure(bg="#f0f8ff")  # Light blue background

# Step 2: City input
city_var = tk.StringVar()
city_label = tk.Label(root, text="Enter City:", font=("Arial", 12), bg="#f0f8ff")
city_label.pack(pady=10)

city_entry = tk.Entry(root, textvariable=city_var, width=30, font=("Arial", 12))
city_entry.pack()

# Step 3: Button to get weather
def get_weather():
    city = city_var.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    api_key = "7979abd13878f3b447f0105a5e1d60db"  # Replace with your actual key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", f"City '{city}' not found.")
            return

        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        temperature_var.set(f"Temperature: {temp}°C")
        condition_var.set(f"Condition: {condition.title()}")

        # Download icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)

        icon_label.configure(image=icon_photo)
        icon_label.image = icon_photo  # Save reference to avoid garbage collection

    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Failed to fetch data.\nCheck your internet.")

check_button = tk.Button(root, text="Check Weather", command=get_weather,
                         font=("Arial", 12), bg="#007acc", fg="white", padx=10, pady=5)
check_button.pack(pady=15)

temperature_var = tk.StringVar()
condition_var = tk.StringVar()

temp_label = tk.Label(root, textvariable=temperature_var, font=("Arial", 12), bg="#f0f8ff")
temp_label.pack(pady=5)

condition_label = tk.Label(root, textvariable=condition_var, font=("Arial", 12), bg="#f0f8ff")
condition_label.pack(pady=5)

icon_label = tk.Label(root, bg="#f0f8ff")
icon_label.pack(pady=5)


# Step 5: Run the app
root.mainloop()
