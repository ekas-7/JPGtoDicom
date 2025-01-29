from PIL import Image
import pydicom
import os
import numpy as np


def process_conversion(input_files, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

    for input_file in input_files:
        try:
            # Open the image using Pillow
            with Image.open(input_file) as img:
                # Convert the image to grayscale (you can adjust as per need)
                img = img.convert("L")
                
                # Convert the image to a numpy array
                img_array = np.array(img)

                # Create a DICOM dataset
                dicom_data = pydicom.Dataset()

                # Set the necessary DICOM attributes
                dicom_data.PatientName = "Test Patient"
                dicom_data.PatientID = "12345"
                dicom_data.Modality = "CT"
                dicom_data.SamplesPerPixel = 1
                dicom_data.Rows = img.height
                dicom_data.Columns = img.width
                dicom_data.PhotometricInterpretation = "MONOCHROME2"
                dicom_data.PixelData = img_array.tobytes()  # Add the image pixel data
                
                # Set required DICOM attributes for endianess and VR
                dicom_data.is_little_endian = True  # Set to True for little endian format
                dicom_data.is_implicit_VR = True  # Set to True for implicit VR

                # Output path for DICOM file
                dicom_file_name = os.path.join(output_folder, f"{os.path.basename(input_file)}.dcm")
                
                # Save the dataset to a DICOM file
                dicom_data.save_as(dicom_file_name)
                
                print(f"Converted {input_file} to DICOM format and saved to {dicom_file_name}")
        
        except Exception as e:
            print(f"Error processing {input_file}: {e}")


# Path to the folder containing the images
image_folder = '/Users/ekaspreetsinghatwal/Desktop/hello2.zip/Lung X-Ray Image/Lung_Opacity/'

# Create a list of image files from 1.jpg to 100.jpg
input_files = [os.path.join(image_folder, f"{i}.jpg") for i in range(1, 101)]

# Create the output folder
output_folder = os.path.join(image_folder, 'output')

# Process the conversion for these files and save them in the output folder
process_conversion(input_files, output_folder)
