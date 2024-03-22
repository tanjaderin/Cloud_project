def create_file(filename, size_in_mb):
    # Size in bytes; round down to the nearest byte if necessary
    size_in_bytes = int(size_in_mb * 1024 * 1024)
    with open(filename, "wb") as file:
        file.seek(size_in_bytes - 1)
        file.write(b"\0")

# Create a 1GB file
create_file("1gb", 1024)

# Create a 1MB file
create_file("1mb", 1)

# Create a 1KB file
create_file("1kb", 1/1024)
