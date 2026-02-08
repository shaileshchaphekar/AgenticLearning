import math

# Accept temperature input from user
try:
    temperature = float(input("Enter the current temperature in Mumbai (°C): "))
    print(f"Current temperature in Mumbai: {temperature}°C")
    sqrt_temp = math.sqrt(temperature)
    print(f"Square root of temperature: {sqrt_temp:.2f}")
except ValueError:
    print("Invalid input. Please enter a valid number.")
except ValueError as e:
    print(f"Error: {e}")