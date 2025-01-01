# NALEnc - Python Encryption Library

NALEnc is a lightweight Python encryption library designed for securely encrypting and decrypting text and binary data. With an intuitive interface and robust functionality, it is ideal for developers seeking a straightforward yet effective encryption solution.

## Features

- Encrypt and decrypt strings or binary data.
- Supports passwords as strings, bytes, or lists of integers (0-255).
- Optimized for messages of size `2046n`, where `n ∈ N`.

## Installation

To install the library, use pip:

```bash
pip install nalenc
```

## Usage

### Importing the Library

```python
import nalenc
```

### Creating an Instance of NALEnc

To use the library, create an instance of the `NALEnc` class with a password. The password can be:

- A string
- A byte sequence
- An iterable of integers (each integer must be in the range `0-255`)

Example:

```python
import nalenc
import random

# Generate a password as a list of integers
password = [random.randint(0, 255) for _ in range(512)]
nal = nalenc.NALEnc(password)
```

### Encrypting Data

Use the `encrypt` method to encrypt a message. The message can be a:

- String
- Byte sequence
- Iterable of integers (each integer must be in the range `0-255`)

Example:

```python
# Encrypt a string
encrypted = nal.encrypt("Hello, World!")

# Encrypt binary data
binary_data = b"\x89PNG\r\n\x1a\n"
encrypted_binary = nal.encrypt(binary_data)
```

### Decrypting Data

Use the `decrypt` method to decrypt an encrypted message.

Example:

```python
# Decrypt the encrypted string
original = nal.decrypt(encrypted)  # Returns a list of integers

# Decrypt binary data
original_binary = nal.decrypt(encrypted_binary)
```

### Working with Binary Files

NALEnc supports encrypting and decrypting binary files. Simply read the file as binary data, encrypt or decrypt it, and then save the result. Note that the encrypted data needs to be cast to `bytes` before writing to a file.

Example:

```python
# Encrypt a binary file
with open("input.bin", "rb") as f:
    data = f.read()

encrypted_data = nal.encrypt(data)

with open("output.enc", "wb") as f:
    f.write(bytes(encrypted_data))

# Decrypt the binary file
with open("output.enc", "rb") as f:
    encrypted_data = f.read()

decrypted_data = nal.decrypt(encrypted_data)

with open("decrypted.bin", "wb") as f:
    f.write(bytes(decrypted_data))
```

## Optimal Message Size

For best performance, messages should have sizes of `2046n`, where `n` is a positive integer. This helps to maximize efficiency and ensure optimal encryption.

## API Reference

### Class: `NALEnc`

#### Constructor

```python
NALEnc(password: str | bytes | Iterable[int])
```

- **password**: The encryption password. It can be a string, byte sequence, or iterable of integers (each in the range `0-255`).

#### Methods

##### `encrypt(msg: str | bytes | Iterable[int])`

Encrypts the given message.

- **msg**: The message to encrypt. Can be a string, byte sequence, or iterable of integers (each in the range `0-255`).
- **Returns**: The encrypted message as a list of integers.

##### `decrypt(msg: str | bytes | Iterable[int])`

Decrypts the given encrypted message.

- **msg**: The encrypted message. Can be a string, byte sequence, or iterable of integers (each in the range `0-255`).
- **Returns**: The original message as a list of integers.

## Example Code

```python
import nalenc
import random

# Generate a random password
password = [random.randint(0, 255) for _ in range(512)]

# Create an instance of NALEnc
nal = nalenc.NALEnc(password)

# Encrypt a message
message = "Encrypt this message!"
encrypted = nal.encrypt(message)

# Decrypt the message
decrypted = nal.decrypt(encrypted)

print("Original:", message)
print("Encrypted:", bytes(encrypted))  # Cast to bytes for readability
print("Decrypted:", bytes(decrypted))
```

## License

This library is licensed under the LGPL License. See the LICENSE file for more information.

---

For questions, feedback, or contributions, feel free to open an issue on the [GitHub repository](https://github.com/AsfhtgkDavid/NAL-Encryption).