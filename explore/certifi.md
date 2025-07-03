## What does the certifi package do?

The `certifi` package plays a behind-the-scenes but important role in keeping Python applications secure on the internet 🌐

**🛡️ What does certifi do?**  
It provides a curated collection of Root Certificates that are used to verify the authenticity of SSL/TLS connections.

Essentially, it helps Python applications trust that a website they’re connecting to is genuinely secure and not impersonated.

These certificates are extracted from Mozilla’s root certificate store—which is one of the most trusted sources.

**🔗 Why is this important?**  
When Python libraries like `requests`, `httpx`, or any HTTPS-enabled tool connect to a website, they use certifi to:

- Validate the SSL certificate of the website.
- Ensure the connection is encrypted and trustworthy.

**🧰 Where is it used?**  
- Commonly used with libraries like `requests`, `urllib3`, and `httpx`.
- Helps avoid SSL certificate verification errors, especially in environments where the system’s native certificate store isn’t reliable or up-to-date.

If you're running web scrapers, APIs, or just downloading files over HTTPS—certifi is that silent bodyguard in your corner.

---

## Can you provide examples of how to use the certifi package?

Absolutely! While certifi isn’t something you usually interact with directly, here's how it fits into real-world Python scenarios—especially when making secure web requests.

### 🔹 Example 1: Using certifi with requests

```python
import requests
import certifi

url = 'https://example.com'
response = requests.get(url, verify=certifi.where())

print("Status Code:", response.status_code)
```

✅ In this example:
- `verify=certifi.where()` tells requests to use the trusted certificate bundle from certifi.
- Ensures your HTTPS request verifies the site’s identity using up-to-date certificates.

### 🔹 Example 2: Using certifi with urllib3

```python
import urllib3
import certifi

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
response = http.request('GET', 'https://example.com')

print("Response Data:", response.data)
```

✅ This is ideal when you’re manually managing HTTPS connections and want tight control over certificate verification.

**🔧 Why bother setting it explicitly?**  
Most modern libraries use certifi behind the scenes by default. But in cases where:
- You're on a system with an outdated certificate store,
- Or using Python embedded in an environment like AWS Lambda or Docker,

…setting the path explicitly ensures secure verification.

---

## I have to update my certificates. What do I do?

If you're referring to updating the CA certificates used by Python (such as those provided by the certifi package), it's pretty straightforward. Here’s what you can do:

### 🔄 Option 1: Update the certifi package via pip

If you’ve installed certifi using pip, just upgrade it like this:

```bash
pip install --upgrade certifi
```

This will fetch the latest root certificates bundled by Mozilla.

### 📍 Option 2: Manually confirm or use updated path

Sometimes it's handy to see where the certificates are stored:

```python
import certifi
print(certifi.where())
```

If you're getting SSL errors, you can point your HTTP libraries to this updated path using:
- `verify=certifi.where()` in requests
- `ca_certs=certifi.where()` in urllib3

### 🐍 Bonus Tip: For system-wide SSL issues

If Python or your system is using outdated certs (outside the certifi ecosystem):

- **On macOS:**  
    ```bash
    sudo security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain > certs.pem
    ```
- **On Linux:**  
    Use your distro’s certificate update tools:
    - Debian/Ubuntu: `sudo update-ca-certificates`
    - Red Hat/CentOS: `sudo update-ca-trust`

If you tell me more about your setup—like your OS or how you're using certificates—I can tailor the steps even more.

---

## I've installed my certificates in my Windows system. How do I make Python use them by default?

If you’ve installed custom CA certificates on your Windows system and want Python to use those by default—rather than relying on packages like certifi—you’ve got a few options:

### 🛠️ Option 1: Set the SSL_CERT_FILE Environment Variable

You can point Python to your system certificate bundle using an environment variable:

1. Locate your certificate bundle (e.g. a `.pem` file) that contains your trusted CAs.
2. Set a system-wide environment variable:

     - Open Start > System Environment Variables.
     - Under “System variables”, click “New”:
         - **Variable name:** `SSL_CERT_FILE`
         - **Variable value:** Path to your `.pem` file (e.g. `C:\certs\my_ca_bundle.pem`)
     - Restart your terminal or IDE to apply it.

✅ This will make Python’s SSL module automatically pick up your certificates.

### 🐍 Option 2: Override Certificate Settings in Code (If Needed)

If you prefer not to set global environment variables, you can hard-code the certificate path when making requests:

```python
import requests

response = requests.get(
        'https://your-secure-api.com',
        verify='C:\\certs\\my_ca_bundle.pem'
)
```

### ⚙️ Option 3: Patch ssl Default Behavior (Advanced)

If you want every Python module to use your certs without modifying each call:

```python
import ssl

ssl._create_default_https_context = ssl.create_default_context(
        cafile='C:\\certs\\my_ca_bundle.pem'
)
```

Use this at the top of your script to globally override.

---

## I have to do it once and globally

If you want Python to use your own trusted certificate bundle globally and once, the most reliable way is to set the `SSL_CERT_FILE` environment variable system-wide. Here's how to do it on Windows:

### 🧭 Step-by-Step: Configure Python to Use Your Custom Certificates Globally

1. **Make sure you have your `.pem` certificate file**  
     It should include all the necessary CA certificates you trust.  
     Example: `C:\certs\my_custom_certs.pem`

2. **Set the Environment Variable**
     - Press `Win + S`, type “Environment Variables”, and select “Edit the system environment variables”.
     - In the System Properties window, click “Environment Variables...”
     - Under System variables, click “New...”
         - **Variable name:** `SSL_CERT_FILE`
         - **Variable value:** `C:\certs\my_custom_certs.pem`
     - Click OK on all windows to save and apply.

💡 **Pro tip:** This affects any Python script, pip, or HTTPS client that uses Python's SSL module—even in virtual environments!

### 🚀 Test It Works

Open a new terminal and run:

```bash
python -c "import ssl; print(ssl.get_default_verify_paths().openssl_cafile)"
```

✅ It should return your custom path.

---

## Can I not use certifi?

Yes, you can avoid using certifi—Python doesn't require it by default. It’s just a convenient way to ensure your SSL certificates are always up to date. But if you’ve set up your own certificate infrastructure (like you did on Windows), here’s how you can skip certifi entirely:

### 🛠️ How to avoid using certifi

1. **Set your own certificate path globally**  
     Setting the `SSL_CERT_FILE` environment variable lets Python use your own CA bundle and bypass certifi:

     ```
     Variable name: SSL_CERT_FILE  
     Value: C:\path\to\your\certs.pem
     ```

     This takes precedence over certifi.

2. **Uninstall certifi (optional but possible)**  
     If you want to fully remove it:

     ```bash
     pip uninstall certifi
     ```

     Just make sure the libraries you use don’t rely on it explicitly.

3. **Use Python’s built-in ssl module directly**

     ```python
     import ssl
     import socket

     context = ssl.create_default_context(cafile="C:\\path\\to\\your\\certs.pem")
     with socket.create_connection(("example.com", 443)) as sock:
             with context.wrap_socket(sock, server_hostname="example.com") as ssock:
                     print("Secure connection established")
     ```

That gives you complete control—no certifi, just Python and your own trust anchors.

---

## Use certifi

Absolutely! Here's a quick, clean example showing how to use the certifi package to secure a web request using Python's requests library:

### 🔐 Example: Make a Secure HTTPS Request Using certifi

```python
import requests
import certifi

url = 'https://example.com'

response = requests.get(url, verify=certifi.where())

print("Status code:", response.status_code)
```

✅ This ensures your connection is verified using the up-to-date CA certificates bundled with certifi, which are maintained by Mozilla and trusted by major libraries.

**🤔 Why use certifi explicitly?**
- You ensure consistent certificate validation across different systems.
- It’s handy in cases where your OS’s certificate store might be outdated or misconfigured.
- It avoids the need for setting global environment variables like `SSL_CERT_FILE`.

---

## I'm using a Python embeddable package. I've installed pip using get-pip.py. I'm part of an organization's secure network. To reach my organization's websites it was throwing an SSL error. So I downloaded my certificates from the browser and installed them in my Windows system.

### How to update my certificates for Python? Can I use certifi to permanently modify that?

Thanks for explaining—this gives great clarity. Since you're using the Python embeddable package, things are a bit different from a full Python installation, but totally manageable.

### 🧩 The Challenge

The Python embeddable package doesn’t come with its own certificates or system-level configuration. When tools like pip or requests try to establish a secure HTTPS connection, they don’t know where your organization’s custom certificates are. That’s why you're getting SSL verification errors.

### ✅ Option 1: Use certifi and Patch It Permanently

The certifi package is read-only—it provides a fixed certificate bundle (`cacert.pem`) inside its site-packages. If you want to inject your organization’s CA certificates into certifi, here’s the clean way:

#### 🛠 Steps:

1. **Locate certifi’s cert bundle:**

     ```python
     import certifi
     print(certifi.where())
     ```

     Let’s say it outputs something like:
     ```
     C:\your\python\path\Lib\site-packages\certifi\cacert.pem
     ```

2. **Append your custom certificates to that file:**
     - Open your `.pem` file with your org’s certificates (downloaded from the browser).
     - Append its contents to `cacert.pem` (don’t overwrite).
     - Use a good text editor like Notepad++ to avoid encoding issues.

3. **(Optional) Lock It In with a Backup Script**  
     Every time you upgrade or reinstall certifi, this change will be lost. So you can write a helper script:

     ```python
     import certifi

     with open("my_org_certs.pem", "rb") as org, open(certifi.where(), "ab") as bundle:
             bundle.write(b"\n")
             bundle.write(org.read())
     ```

     Run this after reinstalling/upgrading certifi.

### 🔁 Option 2: Override certifi.where() Globally

If you’d rather not touch certifi's internals, you can override its behavior in your codebase:

```python
import certifi

def my_cert_path():
        return "C:\\path\\to\\your\\combined_bundle.pem"

certifi.where = my_cert_path
```

Then any module (like pip, requests, urllib3) that uses `certifi.where()` will get your version instead.

### ♻️ Alternative: Skip certifi Altogether Using SSL_CERT_FILE

If modifying certifi sounds brittle, you can instead:

- Set a system or session-wide environment variable:

    ```
    SSL_CERT_FILE=C:\path\to\your\custom.pem
    ```

Even in embeddable Python, this works as long as that variable is set before Python runs.

---

Let me know how you’re planning to run your scripts—via batch files, cron, manual terminal launch? I can help you wrap this up in a startup script or config to make it zero-hassle going forward.

