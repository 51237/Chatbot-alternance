import tempfile

def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.gettempdir()
    temp_file_path = f"{temp_dir}/{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_file_path