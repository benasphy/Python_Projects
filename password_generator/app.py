import streamlit as st
import random
import string

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols):
    # Define character sets
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    # Ensure at least one character set is selected
    if not characters:
        return "Please select at least one character type."
    
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    st.title("🔐 Password Generator")
    
    # Password length slider
    length = st.slider("Password Length", min_value=4, max_value=32, value=12)
    
    # Character type checkboxes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        use_uppercase = st.checkbox("Uppercase", value=True)
    with col2:
        use_lowercase = st.checkbox("Lowercase", value=True)
    with col3:
        use_digits = st.checkbox("Digits", value=True)
    with col4:
        use_symbols = st.checkbox("Symbols", value=True)
    
    # Generate button
    if st.button("Generate Password"):
        password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols)
        
        # Display generated password
        st.success(f"🎉 Generated Password: `{password}`")
        
        # Copy to clipboard
        st.code(password)
        st.write("Click the copy button in the code block to clipboard!")

if __name__ == "__main__":
    main()
