import pandas as pd


def export_to_excel(data, filename):
    try:
        df = pd.DataFrame(data)

        df.to_excel(filename, index=False, engine="openpyxl")
        print(f"Results saved to: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return None
