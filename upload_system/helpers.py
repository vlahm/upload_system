def handle_uploaded_file(f, dest):
    print('handle xlsx and csv')
    with open(dest, 'wb') as d:
        for chunk in f.chunks():
            d.write(chunk)

