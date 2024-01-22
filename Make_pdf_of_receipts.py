
import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(folder_path, output_pdf):
    # Ensure the folder path ends with a slash
    folder_path = folder_path.rstrip('/') + '/'

    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter only the files with image extensions
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Sort the image files to maintain order
    image_files.sort()
    print(image_files)

    # Create a PDF file
    pdf_path = os.path.join(folder_path, output_pdf)
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Iterate through each image and add it to the PDF
    for i, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(folder_path, image_file)

        # Open the image using PIL
        image = Image.open(image_path)

        # Set the title as the image name
        page_title = f"{image_file}"

        # Add a page to the PDF
        c.showPage()

        # Draw the title on the page
        c.setFont("Helvetica", 30)
        c.drawString(30, 10, page_title)

        # Draw the image on the page
        c.drawInlineImage(image_path, 50, 50, width=500, height=700)

        # Optionally, you can close the image file
        image.close()

    # Save the PDF
    c.save()
    print(f'PDF created: {pdf_path}')

folder_path = "/Users/lars/Downloads/Receipts_dec_part2"
output_pdf = "output.pdf"
create_pdf(folder_path, output_pdf)