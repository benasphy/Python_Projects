import streamlit as st
from pyshorteners import Shortener
import validators

def is_valid_url(url):
    # Check if URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        # Add https:// if not present
        url = f'https://{url}'
    return validators.url(url)

def main():
    st.title("🔗 URL Shortener")
    
    # URL Shortening Section
    st.header("Create Short URL")
    long_url = st.text_input("Enter the URL to shorten:")
    
    if st.button("Shorten URL") and long_url:
        try:
            # Create a shortener instance
            shortener = Shortener()
            # Generate short URL
            short_url = shortener.tinyurl.short(long_url)
            st.success(f"Short URL: {short_url}")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # URL Lookup Section
    st.header("Expand URL")
    short_url = st.text_input("Enter the short URL to expand:")
    
    if st.button("Expand URL") and short_url:
        try:
            # Create a shortener instance
            shortener = Shortener()
            # Expand URL
            long_url = shortener.tinyurl.expand(short_url)
            st.success(f"Original URL: {long_url}")
            
        except Exception as e:
            # Handle TinyURL specific errors
            if "URL is not valid" in str(e):
                st.error("Please enter a valid TinyURL format (e.g., https://tinyurl.com/xxxxxx)")
            else:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
