# %%
from img2table.document import Image
from io import BytesIO
from img2table.ocr import TesseractOCR

# image stored where?
img_path = "content_from_images/data/table_image.jpg"

# Read images file as bytes
with open(img_path, 'rb') as f:
    img_bytes = f.read()

# Transform to Image object
img = Image(src=BytesIO(img_bytes))

# Instantiate Tesseract object (basic params)
ocr = TesseractOCR(lang="eng")

# Table identification
img_tables = img.extract_tables(ocr=ocr, borderless_tables=True)

# Express table as dataframe
dataframe = img_tables[0].df

# Clean dataframe
# 1) First row as header
dataframe.columns = dataframe.iloc[0]
dataframe = dataframe[1:]
# 2) Clean up names (not perfect)
dataframe["Name"] = dataframe["Name"].str.extract(r"[0-9]?\)?\s(.*)")

# Export dataframe to csv
output_name = img_path.split("/")[-1].split(".")[0] + ".csv"
dataframe.to_csv(f"content_from_images/output/{output_name}")
