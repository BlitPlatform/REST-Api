import os 
import zipfile
import io
from services.common.diroperations.dirservice import remove_user_directory

def zipfiles(filenames, user_id):
    zip_filename = user_id + "generated_stl.zip"

    stream = io.BytesIO()
    zip_file = zipfile.ZipFile(stream, "w")

    for file_path in filenames:
        _ ,file_name = os.path.split(file_path)

        zip_file.write(file_path, file_name)
    zip_file.close()

    return {'stream_value': stream.getvalue(), 'file_name': zip_filename}