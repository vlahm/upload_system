def handle_uploaded_file(f, dest):
    with open(dest, 'w') as d:
        for chunk in f.chunks():
            d.write(chunk)

