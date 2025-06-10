Skip to content
You said:
my odbc connnection is failing for the said reason. but my jdbc connection worked and connection through python snowflake connector worked . why is this happening. i did not change anything on system level. no changes to firewall or hostnames and port numbers. im using snowflake_jwt to auth. 
in a linux system with snowflake-odbc configured defaultly.
the error is below

Error: nanodbc/nanodbc.cpp:1135: 01S00: [Snowflake][Snowflake] (4) REST request for URL *** failed: CURLerror (curl_easy_perform() failed) - code=60 msg='SSL peer certificate or SSH remote key was not OK'. Use the SYSTEM$ALLOWLIST or check your firewalls settings
ChatGPT said:
The error you're seeing in your ODBC connection:

Error: nanodbc/nanodbc.cpp:1135: 01S00: [Snowflake][Snowflake] (4) REST request for URL *** failed: CURLerror (curl_easy_perform() failed) - code=60 msg='SSL peer certificate or SSH remote key was not OK'. Use the SYSTEM$ALLOWLIST or check your firewalls settings
means that the ODBC driver failed to verify the SSL certificate when trying to connect to Snowflake. This kind of error (CURL code 60) is specifically an SSL certificate validation failure.

Why JDBC and Python connectors worked but ODBC didn't
There are a few reasons this might happen:

✅ 1. ODBC uses libcurl directly
The ODBC driver depends on libcurl and system-level CA certificates for SSL validation, whereas:

JDBC uses the Java truststore (cacerts) which often includes a broad set of CA certificates.

Python Snowflake connector uses requests and the bundled CA certs in the certifi package.

If your Linux system's CA certificates are outdated or missing the cert that Snowflake uses, only the ODBC driver will fail.

✅ 2. Mismatch in trusted certificate authority (CA) list
The ODBC driver might be trying to validate against a different CA store (usually found in /etc/ssl/certs/ca-certificates.crt or /etc/pki/tls/certs/ca-bundle.crt). If your system hasn't updated CA certificates recently, Snowflake's cert may not be recognized.

Run:

sudo update-ca-certificates  # Debian/Ubuntu
sudo trust extract-compat     # RHEL/CentOS with p11-kit
✅ 3. ODBC driver SSL configuration
The ODBC driver might be stricter or configured to not use certain certs. You can specify a CA bundle path in the odbc.ini file:

Example:

[SnowflakeDSN]
Driver = /usr/lib/snowflake/odbc/lib/libsnowflakeodbc.so
Server = xyz.snowflakecomputing.com
Authenticator = snowflake_jwt
SSLTrustStore = /etc/ssl/certs/ca-certificates.crt  # or whatever path applies
Or you might need to explicitly disable SSL certificate verification (not recommended in prod):

SSLValidation = false
✅ 4. Environment variable override
If your system has something like CURL_CA_BUNDLE or SSL_CERT_FILE set for the environment in which Python or JDBC runs, but not for the ODBC context (e.g., a different shell or daemon), it may cause the ODBC to fail.

✅ 5. Version mismatch or bug in ODBC driver
Ensure you're using the latest Snowflake ODBC driver. Older versions may not support the current CA cert Snowflake uses.

You can check the version:

odbcinst -q -d -n "Snowflake"
Then cross-check with the latest on Snowflake’s official ODBC downloads.

What you can do next
🔧 Fix suggestions:
Update system CA certs:

sudo update-ca-certificates
Specify SSLTrustStore explicitly in your odbc.ini (use the correct path for your distro).

Temporarily disable SSL validation for testing only:

SSLValidation = false
Warning: This is insecure and should only be used for diagnostics.

Reinstall or update the Snowflake ODBC driver.

Export cert paths to ODBC runtime:

export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
isql -v SnowflakeDSN
Would you like me to help you locate the correct certificate file path on your system or validate which CA is missing?

You said:
how to add my certificate dynamically
ChatGPT said:
To dynamically add your certificate (e.g. a custom root or intermediate certificate used by Snowflake) for ODBC on Linux, you have a few options depending on how temporary or permanent you want the change to be.

✅ 1. Dynamically using environment variable (CURL_CA_BUNDLE)
This is the fastest and most flexible method.

🧩 Steps:
If you have a custom CA certificate file (e.g. my_ca.crt):

export CURL_CA_BUNDLE=/path/to/my_ca.crt
isql -v SnowflakeDSN
This tells libcurl (used by the Snowflake ODBC driver) to use your custom certificate bundle only for this session.

You can also combine your cert with system certs:

cat /etc/ssl/certs/ca-certificates.crt my_ca.crt > combined_certs.crt
export CURL_CA_BUNDLE=/path/to/combined_certs.crt
isql -v SnowflakeDSN
✅ 2. Use SSLTrustStore in odbc.ini
You can explicitly point the ODBC driver to your custom certificate bundle.

Example odbc.ini:
[SnowflakeDSN]
Driver = /usr/lib/snowflake/odbc/lib/libsnowflakeodbc.so
Server = xyz.snowflakecomputing.com
Authenticator = snowflake_jwt
SSLTrustStore = /path/to/combined_certs.crt
If you're dynamically generating or modifying this file (e.g., in a script), you can inject that value programmatically.

✅ 3. Append cert to system CA store (semi-permanent)
If you want to do this system-wide (applies to all users and tools), you can add your cert to the system CA store.

For Debian/Ubuntu:

sudo cp my_ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
For RHEL/CentOS:

sudo cp my_ca.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust extract
This will permanently update /etc/ssl/certs/ca-certificates.crt (used by libcurl) with your cert.

✅ 4. Programmatic approach (e.g., in a shell or Python script)
If you're invoking ODBC via a shell script or Python, export the env var beforehand:

import os
import subprocess

os.environ["CURL_CA_BUNDLE"] = "/path/to/combined_certs.crt"
subprocess.run(["isql", "-v", "SnowflakeDSN"])
This avoids modifying global config files and is great for automation.

🔐 Tip for Snowflake JWT users
If you're using Snowflake JWT with a custom CA (e.g., self-signed intermediate used for signing the JWT cert), that CA must also be trusted by the ODBC driver. Even if auth works with other connectors, ODBC may fail without trust of the full chain.

Would you like a quick script that combines system CA certs and your own cert into a single file dynamically?

You said:
how to get my certificate for snowflake
ChatGPT said:
Great question! To get the SSL certificate (or certificate chain) that Snowflake uses, so you can trust it explicitly for your ODBC connection, here’s how you can do it:

Option 1: Fetch Snowflake server's SSL cert using openssl
You can directly grab the certificate from Snowflake’s hostname.

echo | openssl s_client -connect <your_account>.snowflakecomputing.com:443 -showcerts
Replace <your_account> with your actual Snowflake account host (e.g. xy12345.us-east-1).

This command outputs the entire certificate chain. It looks like this:

-----BEGIN CERTIFICATE-----
MIID...
...rest of cert...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIID... (intermediate CA)
-----END CERTIFICATE-----
Copy the root and intermediate certificates from the output into a .crt file (e.g., snowflake_cert_chain.crt).

Option 2: Export certificate using a browser
Open your Snowflake web UI in Chrome/Firefox: https://<your_account>.snowflakecomputing.com

Click the padlock icon next to the URL → View Certificate

Export the root and intermediate certificates in PEM format

Save them to a .crt file

Option 3: Get CA certificates from your OS / CA provider
Snowflake uses standard trusted CAs like DigiCert, Let's Encrypt, or similar, so normally your system's CA bundle already trusts it.

If you're behind a corporate firewall or proxy that intercepts SSL, then you likely need your company's internal root or intermediate cert instead (you’ll have to get that from your IT/security team).

What to do with the certificate
Save your collected cert(s) in a file, e.g. snowflake_ca.crt.

Use it with CURL_CA_BUNDLE or SSLTrustStore as I mentioned earlier.

If you want, I can help you with the exact commands or scripts to extract and create the proper certificate bundle file! Just let me know your Snowflake hostname.

You said:
how to mention my cert file to be used in R script connection string
ChatGPT said:
To use your custom certificate file in an R script when connecting to Snowflake via ODBC, you need to make sure the ODBC driver picks up that certificate during the connection.

Here’s how to do it:

1. Prepare your certificate file
Make sure your cert file (e.g., snowflake_ca.crt) includes the full trusted chain (root + intermediate).

2. Set the environment variable CURL_CA_BUNDLE in R
The Snowflake ODBC driver uses libcurl which respects the CURL_CA_BUNDLE environment variable for the SSL CA cert path.

Add this at the top of your R script before you create the DB connection:

Sys.setenv(CURL_CA_BUNDLE = "/full/path/to/snowflake_ca.crt")
3. Use DBI + odbc package to connect
Example:

library(DBI)
library(odbc)

# Set the CA bundle environment variable
Sys.setenv(CURL_CA_BUNDLE = "/full/path/to/snowflake_ca.crt")

# Connect to Snowflake using DSN or connection string
con <- dbConnect(odbc(),
                 Driver = "Snowflake",         # Or full path to ODBC driver
                 Server = "<your_account>.snowflakecomputing.com",
                 UID = "<your_username>",
                 Authenticator = "snowflake_jwt",
                 Database = "<database>",
                 Schema = "<schema>",
                 Warehouse = "<warehouse>",
                 Role = "<role>",
                 SSLTrustStore = "/full/path/to/snowflake_ca.crt"  # sometimes accepted
)

# Now use `con` to run queries
4. Alternative: Specify SSLTrustStore in connection string
Some versions of Snowflake ODBC allow you to specify the cert file directly in the connection string via the parameter SSLTrustStore:

con <- dbConnect(odbc(),
                 .connection_string = paste(
                   "Driver=Snowflake;",
                   "Server=<your_account>.snowflakecomputing.com;",
                   "UID=<your_username>;",
                   "Authenticator=snowflake_jwt;",
                   "Database=<database>;",
                   "Schema=<schema>;",
                   "Warehouse=<warehouse>;",
                   "Role=<role>;",
                   "SSLTrustStore=/full/path/to/snowflake_ca.crt;",
                   sep=""))
Summary:
Set CURL_CA_BUNDLE env var in R

Optionally add SSLTrustStore in the connection string

Use full absolute path to your .crt file

Connect via DBI::dbConnect() and odbc::odbc()

If you want, I can help write a full minimal R example tailored to your setup. Just share your connection details (without passwords) or let me know!

You said:
does odbc 3.51 accept
ChatGPT said:
The Snowflake ODBC Driver version 3.51 does support the SSLTrustStore parameter to specify a custom CA certificate file.

What this means for you:
You can use the SSLTrustStore parameter in your ODBC connection string or in your odbc.ini config file to point to your .crt file.

This tells the driver explicitly which CA bundle to trust for SSL validation.

Example usage with ODBC 3.51
In odbc.ini:

[SnowflakeDSN]
Driver = /path/to/libsnowflakeodbc.so
Server = <your_account>.snowflakecomputing.com
Authenticator = snowflake_jwt
SSLTrustStore = /full/path/to/your_ca_bundle.crt
In connection string (e.g., from R or other clients):

Driver=Snowflake;Server=<your_account>.snowflakecomputing.com;Authenticator=snowflake_jwt;SSLTrustStore=/full/path/to/your_ca_bundle.crt;...
A quick tip
Make sure your .crt file includes the full certificate chain (root + intermediates).

Always use the absolute path for SSLTrustStore.

If you see issues with certs, double-check file permissions and format (PEM format, i.e. -----BEGIN CERTIFICATE-----).

If you want, I can help you generate a sample connection string or help verify your .crt file compatibility with the driver!

You said:
what is the CaBundleFile parameter
ChatGPT said:
The **CaBundleFile** parameter is an ODBC driver configuration option used to specify the path to a custom CA (Certificate Authority) bundle file that the Snowflake ODBC driver should trust when establishing a secure TLS/SSL connection.

🔹 What It Does
It tells the Snowflake ODBC driver to use a specific PEM-formatted certificate bundle (i.e., a file containing one or more trusted root and/or intermediate certificates) to validate the Snowflake server’s SSL certificate.

🔍 Difference between CaBundleFile vs SSLTrustStore
Parameter	Used In	Function
CaBundleFile	odbc.ini / connection string	Specifies a file with trusted CA certs (PEM)
SSLTrustStore	Deprecated alias or alternate name in some drivers	Effectively same in many cases, but CaBundleFile is preferred and officially documented in newer drivers
⚠️ Snowflake documentation recommends using CaBundleFile as the correct parameter name as of ODBC driver versions 2.24.5+.

✅ Example: In odbc.ini
[SnowflakeDSN]
Driver = /usr/lib/snowflake/odbc/lib/libsnowflakeodbc.so
Server = <your_account>.snowflakecomputing.com
Authenticator = snowflake_jwt
CaBundleFile = /path/to/snowflake_ca.crt
✅ Example: In R or connection string
con <- dbConnect(odbc(),
                 .connection_string = paste(
                   "Driver=Snowflake;",
                   "Server=<your_account>.snowflakecomputing.com;",
                   "Authenticator=snowflake_jwt;",
                   "CaBundleFile=/path/to/snowflake_ca.crt;",
                   sep=""))
🔧 Requirements for the CA Bundle File
Must be in PEM format (-----BEGIN CERTIFICATE-----)

Should include the full certificate chain (root + intermediates if needed)

Must be readable by the user executing the connection

🧠 Summary
✅ CaBundleFile is the correct and documented parameter to specify a custom CA cert file in the Snowflake ODBC driver

✅ Use it in your odbc.ini or connection string

❌ Don't confuse it with SSLTrustStore (older/less preferred)

📄 The file must be in PEM format and trusted by the ODBC driver via libcurl

Would you like help creating a valid CaBundleFile from Snowflake's actual cert chain?

You said:
i got the same eror even though i pointed it to a correct certificate
ChatGPT said:
If you're still getting this error:

CURLerror (curl_easy_perform() failed) - code=60 msg='SSL peer certificate or SSH remote key was not OK'

even after explicitly setting CaBundleFile to a valid certificate file, then here’s a step-by-step breakdown to isolate and fix the issue:

✅ Troubleshooting Checklist
🔹 1. Confirm the certificate file format
Make sure your certificate file is in PEM format and includes the full chain (intermediate + root).

✅ It should look like this (multiple certs in the same file):

-----BEGIN CERTIFICATE-----
MIIBIjANBgkqhkiG9w...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIEvjCCA6agAwIBAgIQ...
-----END CERTIFICATE-----
You can test it with:

openssl x509 -in /path/to/your_ca_bundle.crt -text -noout
If it prints details, the file is valid.

🔹 2. Test the cert with openssl s_client
Try connecting to Snowflake manually and verify what certs are being used:

openssl s_client -connect <your_account>.snowflakecomputing.com:443 -CAfile /path/to/your_ca_bundle.crt
You should not see this in the output:

Verify return code: 21 (unable to verify the first certificate)
If you do see that, your cert bundle is missing part of the chain.

🔹 3. Avoid using both CaBundleFile and SSLTrustStore
Use only one — preferably CaBundleFile. Some driver versions behave unpredictably when both are set.

🔹 4. Use absolute path and check permissions
Double-check that the path to CaBundleFile is absolute and correct.

Ensure the file is readable by the user running R or the process invoking the ODBC connection.

ls -l /path/to/your_ca_bundle.crt
🔹 5. Try setting CURL_CA_BUNDLE
Set this environment variable in your R script or shell before connecting:

Sys.setenv(CURL_CA_BUNDLE = "/path/to/your_ca_bundle.crt")
Or in shell:

export CURL_CA_BUNDLE=/path/to/your_ca_bundle.crt
Rscript your_script.R
This is a lower-level override and sometimes works when CaBundleFile doesn’t.

🔹 6. Driver version
What version of the Snowflake ODBC driver are you using?

odbcinst -q -d -n "Snowflake"
If it’s not v2.24.5 or newer, upgrade. Older versions have SSL verification bugs.

🔁 If nothing works…
Try this fail-safe method:

Get the full certificate chain from Snowflake:

openssl s_client -connect <your_account>.snowflakecomputing.com:443 -showcerts </dev/null | awk '/BEGIN CERTIFICATE/,/END CERTIFICATE/ { print $0 }' > snowflake_ca_bundle.crt
Use only this in CaBundleFile.

Want help analyzing your current cert file?
If you're comfortable sharing (you can redact sensitive parts), I can help validate it. Or I can guide you interactively to rebuild a proper CaBundleFile.

Let me know!

You said:
if it stilll fails does that mean i have to do firewall settings?
ChatGPT said:
If your ODBC connection still fails with this error even after using a valid CaBundleFile, and you’ve confirmed your certificate is correct and readable, then yes, it’s possible the problem is not the certificate itself, but something like:

🔒 Likely Causes Beyond Cert File:
🔹 1. Outbound HTTPS traffic being intercepted or blocked
Many corporate environments intercept HTTPS using proxy firewalls or SSL inspection, which:

Replaces Snowflake’s cert with a corporate one

Breaks certificate validation unless your CA bundle includes your company’s root/intermediate CA

✅ If this is the case:

You need to get your corporate root CA cert from your IT/security team

Then add it to your custom CaBundleFile

🔹 2. Corporate firewall or outbound proxy altering or blocking traffic
ODBC (libcurl) might be making raw HTTPS requests that:

Go through a proxy that modifies the cert chain

Are outright blocked or redirected

✅ Test with curl (uses same libcurl as ODBC):

curl -v https://<your_account>.snowflakecomputing.com
If you see SSL errors or proxy-related issues here, the problem is at the network or proxy level.

🔹 3. Proxy required, but not configured
ODBC doesn’t auto-detect proxies like browsers or Java (JDBC) do.

✅ If your company requires proxy access, you’ll need to manually set:

export http_proxy=http://your.proxy.company.com:port
export https_proxy=http://your.proxy.company.com:port
Or configure it in your .odbc.ini using the proxyHost, proxyPort, etc.

🔹 4. OCSP or CRL blocked by firewall
Snowflake does OCSP (Online Certificate Status Protocol) checks for revocation. If those requests are blocked by your firewall:

The ODBC driver might reject the connection

✅ Fix: Ensure outbound connections to OCSP servers (like ocsp.digicert.com) are allowed on port 443.

🔍 How to Confirm It’s a Network Issue
Try this command to simulate a clean TLS handshake (no ODBC involved):

openssl s_client -connect <your_account>.snowflakecomputing.com:443
If this fails with certificate issues even though JDBC and Python work, it's nearly guaranteed the issue is with:

A corporate MITM proxy

Missing corporate CA cert in your trust bundle

Firewall/proxy tampering with TLS

🧩 What You Should Do
✅ Confirm whether TLS is intercepted:

Run curl -v and openssl s_client to Snowflake

✅ Ask IT/security for the corporate root/intermediate CA

Add to your CA bundle file used by ODBC

✅ Ensure proxy config is set if required

✅ Allow Snowflake domains and OCSP endpoints through firewall

Would you like help analyzing your curl or openssl output?
You can paste the results (redact account details), and I’ll tell you whether it’s a network issue or cert issue.

