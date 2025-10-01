# PicFrame Security Analysis Report

## Executive Summary

This document presents a comprehensive security analysis of the PicFrame digital picture frame application. The analysis covers authentication and authorization mechanisms, input validation and sanitization, and configuration security across all interfaces (HTTP, MQTT, and peripheral controls).

## 1. Authentication and Authorization Analysis

### 1.1 HTTP Basic Authentication Implementation

**Current Implementation:**
- HTTP interface supports optional Basic Authentication via configuration
- Credentials are Base64 encoded and stored in memory
- Authentication check performed in `do_AUTHHEAD()` method
- Failed authentication attempts are logged with source IP

**Security Findings:**

#### ✅ Strengths:
- Authentication is optional and can be disabled for trusted networks
- Failed authentication attempts are logged for security monitoring
- Source IP addresses are logged for failed attempts
- Proper HTTP status codes (401, 403) are returned for auth failures
- Connection is closed after authentication failure

#### ⚠️ Vulnerabilities and Concerns:

1. **Weak Credential Storage:**
   - Credentials stored as simple Base64 encoding in memory
   - Base64 is encoding, not encryption - easily reversible
   - No password hashing or secure credential storage

2. **Plaintext Password Transmission:**
   - HTTP Basic Auth sends credentials in Base64 over the wire
   - Without SSL/TLS, credentials are transmitted in plaintext
   - Susceptible to network sniffing and man-in-the-middle attacks

3. **No Session Management:**
   - No session tokens or expiration mechanisms
   - Credentials must be sent with every request
   - No ability to revoke access without changing passwords

4. **Limited Brute Force Protection:**
   - No rate limiting or account lockout mechanisms
   - No progressive delays for failed attempts
   - Could be vulnerable to brute force attacks

**Code Analysis:**
```python
# From interface_http.py line 254
elif self.headers.get("Authorization") != "Basic " + self.server._auth:
    self.send_response(403)
    # ... error handling
```

### 1.2 MQTT Authentication and TLS Configuration

**Current Implementation:**
- MQTT client supports username/password authentication
- TLS/SSL support available via certificate file configuration
- Connection parameters configurable via YAML

**Security Findings:**

#### ✅ Strengths:
- Supports TLS encryption for secure MQTT communications
- Username/password authentication supported
- Proper SSL context setup with certificate validation
- Connection errors are logged and handled gracefully

#### ⚠️ Vulnerabilities and Concerns:

1. **Certificate Validation:**
   - TLS certificate path is configurable but validation method unclear
   - No explicit certificate chain validation in code
   - Potential for accepting invalid or self-signed certificates

2. **Credential Storage:**
   - MQTT credentials stored in plaintext configuration files
   - No encryption of stored passwords
   - Configuration files may be readable by other users

3. **Connection Security:**
   - Default port 8883 for TLS, 1883 for plaintext
   - Risk of misconfiguration leading to plaintext transmission
   - No enforcement of TLS when credentials are present

**Code Analysis:**
```python
# From interface_mqtt.py
self.__client.username_pw_set(self.__login, self.__password)
if self.__tls:
    self.__client.tls_set(self.__tls)
```

### 1.3 File Handling Security

**Current Implementation:**
- File paths processed through `os.path.expanduser()` and `urlparse.unquote()`
- Static file serving from configured HTML directory
- Image file access through database queries

**Security Findings:**

#### ⚠️ Critical Vulnerabilities:

1. **Directory Traversal Risk:**
   - URL paths are decoded with `urlparse.unquote()` without validation
   - No explicit path traversal protection (../, ..\)
   - Could allow access to files outside intended directories

2. **Insufficient Path Validation:**
   - File paths not normalized or validated against allowed directories
   - No checks for symbolic link traversal
   - Potential for accessing system files

**Code Analysis:**
```python
# From interface_http.py line 285
page = urlparse.unquote(page)
if os.path.isfile(page):
    # File is served without additional validation
```

## 2. Input Validation and Sanitization Analysis

### 2.1 HTTP Interface Input Validation

**Current Implementation:**
- Query parameters parsed using `urlparse.parse_qsl()`
- Parameter values converted to appropriate types (bool, float)
- Controller method validation through `dir()` checks

**Security Findings:**

#### ✅ Strengths:
- Parameter names validated against controller attributes
- Type conversion with error handling
- JSON parameter validation for complex values

#### ⚠️ Vulnerabilities and Concerns:

1. **Insufficient Input Sanitization:**
   - No validation of parameter value ranges or formats
   - String parameters not sanitized for special characters
   - Potential for injection attacks through parameter values

2. **JSON Deserialization Risk:**
   - JSON parameters deserialized without validation
   - Could be vulnerable to JSON injection attacks
   - No size limits on JSON payloads

3. **Error Information Disclosure:**
   - Exception details included in HTTP responses
   - Could reveal internal application structure
   - Potential information leakage to attackers

**Code Analysis:**
```python
# From interface_http.py line 322
try:
    if key in self.server._setters:
        setattr(self.server._controller, key, value)
    else:
        value = value.replace("\'", "\"")  # only " permitted in json
        getattr(self.server._controller, key)(**json.loads(value))
except Exception as e:
    message['ERROR'] = 'Excepton:{}>{};'.format(key, e)
```

### 2.2 MQTT Message Validation

**Current Implementation:**
- MQTT messages processed through callback functions
- Topic-based routing for different commands
- Message payload parsing and validation

**Security Findings:**

#### ⚠️ Vulnerabilities and Concerns:

1. **Limited Message Validation:**
   - No comprehensive validation of MQTT message payloads
   - Topic names not validated for malicious content
   - Potential for command injection through MQTT messages

2. **No Message Size Limits:**
   - No explicit limits on MQTT message sizes
   - Could be vulnerable to denial of service attacks
   - Large messages could consume excessive memory

### 2.3 Database Query Construction and SQL Injection Prevention

**Current Implementation:**
- SQLite database with parameterized queries in some places
- Dynamic WHERE clause construction from user filters
- String formatting used for SQL query building

**Security Findings:**

#### ✅ Strengths:
- Some parameterized queries used (e.g., `cursor.execute(sql, (time.time(), file_id))`)
- Basic input sanitization in filter building

#### ⚠️ Critical SQL Injection Vulnerabilities:

1. **Dynamic SQL Construction with String Formatting:**
   ```python
   # From image_cache.py line 253-255
   sql = """SELECT file_id FROM all_data WHERE {0} ORDER BY {1}
       """.format(where_clause, sort_clause)
   return cursor.execute(sql).fetchall()
   ```
   - WHERE clauses built using string formatting
   - Sort clauses constructed dynamically
   - No parameterized queries for user-controlled data

2. **Filter Building Vulnerabilities:**
   ```python
   # From model.py line 540
   val = val.replace(";", "").replace("'", "").replace("%", "").replace('"', '')  # SQL scrambling
   ```
   - Basic character filtering, but insufficient
   - Still vulnerable to SQL injection through other characters
   - Logic operators (AND, OR, NOT) passed through without validation

3. **WHERE Clause Construction:**
   ```python
   # From model.py line 696-697
   where_list = ["fname LIKE '{}/%'".format(picture_dir)]
   where_list.extend(self.__where_clauses.values())
   ```
   - Direct string formatting in LIKE clauses
   - User-controlled values inserted without parameterization

### 2.4 File Path Validation

**Current Implementation:**
- File paths expanded using `os.path.expanduser()`
- Database queries filter available files
- Extension-based file type validation

**Security Findings:**

#### ⚠️ Critical Vulnerabilities:

1. **Path Traversal Vulnerability:**
   - No validation against directory traversal attacks
   - Symbolic links could be exploited
   - No canonicalization of file paths

2. **Insufficient Extension Validation:**
   - File extensions checked but not validated securely
   - Could be bypassed with double extensions
   - No MIME type validation

### 2.5 Configuration Parameter Validation

**Current Implementation:**
- YAML configuration parsing
- Type conversion for numeric values
- Basic range checking for some parameters

**Security Findings:**

#### ⚠️ Vulnerabilities and Concerns:

1. **Insufficient Range Validation:**
   - Numeric parameters not validated for reasonable ranges
   - Could cause resource exhaustion with extreme values
   - No validation of file paths for existence and permissions

2. **Configuration Injection:**
   - YAML parsing could be vulnerable to YAML injection
   - No validation of configuration structure
   - Malicious configuration could affect application behavior

## 3. Configuration Security Assessment

### 3.1 Configuration File Handling

**Current Implementation:**
- YAML configuration files with sensitive data
- Configuration loaded at startup
- Default configuration example provided

**Security Findings:**

#### ⚠️ Vulnerabilities and Concerns:

1. **Plaintext Credential Storage:**
   - All passwords stored in plaintext in YAML files
   - MQTT credentials, HTTP auth passwords unencrypted
   - Configuration files may have overly permissive permissions

2. **Sensitive Data in Configuration:**
   - API keys (geo_key) stored in plaintext
   - Database file paths exposed
   - No encryption of sensitive configuration data

3. **Default Credentials Risk:**
   - Example configuration contains placeholder credentials
   - Risk of users deploying with default/weak passwords
   - No enforcement of strong password policies

**Code Analysis:**
```yaml
# From configuration_example.yaml
mqtt:
  login: "name"                           # your mqtt user
  password: "your_password"               # password for mqtt user
  
http:
  username: admin                         # username for basic auth
  password: null                          # password for basic auth
```

### 3.2 SSL/TLS Configuration

**Current Implementation:**
- SSL/TLS support for HTTP interface
- Certificate and key file paths configurable
- TLS support for MQTT connections

**Security Findings:**

#### ✅ Strengths:
- SSL/TLS encryption available for both HTTP and MQTT
- Configurable certificate and key file paths
- Proper SSL context setup

#### ⚠️ Vulnerabilities and Concerns:

1. **SSL Configuration Validation:**
   - No validation of certificate file existence or validity
   - No checks for certificate expiration
   - Weak cipher suites may be accepted

2. **Key File Security:**
   - Private key files not validated for proper permissions
   - No protection against key file exposure
   - No key rotation mechanisms

**Code Analysis:**
```python
# From controller.py line 598
if self.__http_config['use_ssl']:
    self.__interface_http.socket = ssl.wrap_socket(
                            self.__interface_http.socket,
                            keyfile=self.__http_config['keyfile'],
                            certfile=self.__http_config['certfile'],
                            server_side=True)
```

### 3.3 Password Management

**Current Implementation:**
- Optional auto-generation of HTTP passwords
- Passwords stored in configuration files
- No password complexity requirements

**Security Findings:**

#### ⚠️ Vulnerabilities and Concerns:

1. **Weak Password Generation:**
   - Auto-generated passwords may not meet security standards
   - No entropy requirements specified
   - Generated passwords stored in plaintext

2. **No Password Policy:**
   - No minimum password length requirements
   - No complexity requirements (uppercase, numbers, symbols)
   - No password expiration or rotation policies

3. **Password Storage:**
   - All passwords stored in plaintext
   - No hashing or encryption of stored passwords
   - Configuration files may be accessible to unauthorized users

### 3.4 YAML Configuration Security

**Current Implementation:**
- Uses `yaml.safe_load()` for configuration parsing
- Configuration merged with default values
- Error handling for YAML parsing failures

**Security Findings:**

#### ✅ Strengths:
- Uses `yaml.safe_load()` instead of `yaml.load()` (prevents code execution)
- Graceful error handling for malformed YAML
- Configuration validation through merging with defaults

**Code Analysis:**
```python
# From model.py line 384
conf = yaml.safe_load(stream)
for section in ['viewer', 'model', 'mqtt', 'http', 'peripherals']:
    self.__config[section] = {**DEFAULT_CONFIG[section], **conf[section]}
```

#### ⚠️ Vulnerabilities and Concerns:

1. **Configuration File Permissions:**
   - No validation of configuration file permissions
   - Files may be readable by unauthorized users
   - No checks for world-readable configuration files

2. **Sensitive Data Exposure:**
   - All sensitive data stored in plaintext YAML
   - API keys, passwords, and certificates paths exposed
   - No encryption of configuration data at rest

3. **Configuration Injection:**
   - While `safe_load()` prevents code execution, malicious configuration values could still affect application behavior
   - No validation of configuration value ranges or formats
   - Potential for resource exhaustion through extreme configuration values

### 3.5 File System Security

**Current Implementation:**
- Uses `os.path.expanduser()` for path expansion
- File operations without explicit permission checks
- Database and log files created with default permissions

**Security Findings:**

#### ⚠️ Vulnerabilities and Concerns:

1. **File Permission Management:**
   - No explicit setting of secure file permissions
   - Database files may be created with overly permissive permissions
   - Log files could be readable by unauthorized users

2. **Path Expansion Security:**
   - `os.path.expanduser()` used without validation
   - Could be exploited if user input controls paths
   - No canonicalization of file paths

3. **Temporary File Security:**
   - HEIF conversion uses fixed temporary file path (`/dev/shm/temp.jpg`)
   - No secure temporary file creation
   - Potential race conditions with concurrent access

**Code Analysis:**
```python
# From interface_http.py line 179
image.save("/dev/shm/temp.jpg")  # default 75% quality
```

### 3.6 Logging Security

**Current Implementation:**
- Configurable log levels and file output
- Logging of authentication failures and errors
- File-based logging with append mode

**Security Findings:**

#### ✅ Strengths:
- Authentication failures are logged with source IP
- Configurable log levels for security monitoring
- Error conditions are logged for debugging

#### ⚠️ Vulnerabilities and Concerns:

1. **Log File Security:**
   - Log files created with default permissions
   - No log rotation or size limits
   - Potential for log file exhaustion attacks

2. **Information Disclosure in Logs:**
   - Detailed error messages may reveal system information
   - Configuration details may be logged
   - Potential for sensitive data leakage in debug logs

3. **Log Injection:**
   - User-controlled data may be logged without sanitization
   - Potential for log injection attacks
   - No validation of logged content

## 4. Risk Assessment and Recommendations

### 4.1 Critical Security Issues (High Priority)

1. **SQL Injection Vulnerabilities**
   - **Risk:** Critical - Could allow database manipulation and data access
   - **Recommendation:** Replace string formatting with parameterized queries
   - **Action:** Implement proper SQL parameter binding for all user-controlled data

2. **Directory Traversal Vulnerability**
   - **Risk:** High - Could allow access to system files
   - **Recommendation:** Implement path canonicalization and validation
   - **Action:** Add `os.path.realpath()` and validate against allowed directories

3. **Plaintext Credential Storage**
   - **Risk:** High - Credentials easily compromised if files accessed
   - **Recommendation:** Implement credential encryption or secure storage
   - **Action:** Use password hashing for stored credentials

4. **Insufficient Input Validation**
   - **Risk:** Medium-High - Potential for injection attacks
   - **Recommendation:** Implement comprehensive input sanitization
   - **Action:** Add parameter validation and sanitization functions

### 4.2 Medium Priority Issues

1. **Weak Authentication Mechanisms**
   - **Risk:** Medium - Credentials vulnerable to interception
   - **Recommendation:** Enforce HTTPS for authentication
   - **Action:** Require SSL/TLS when authentication is enabled

2. **Information Disclosure**
   - **Risk:** Medium - Error messages reveal internal structure
   - **Recommendation:** Implement generic error responses
   - **Action:** Log detailed errors but return generic messages to clients

3. **No Rate Limiting**
   - **Risk:** Medium - Vulnerable to brute force attacks
   - **Recommendation:** Implement rate limiting and account lockout
   - **Action:** Add request rate limiting to HTTP interface

### 4.3 Low Priority Issues

1. **Configuration File Permissions**
   - **Risk:** Low-Medium - Depends on system configuration
   - **Recommendation:** Document proper file permissions
   - **Action:** Add security documentation for deployment

2. **Certificate Validation**
   - **Risk:** Low - Depends on deployment environment
   - **Recommendation:** Implement certificate validation
   - **Action:** Add certificate expiration checks

## 5. Security Improvement Recommendations

### 5.1 Immediate Actions Required

1. **Fix SQL Injection Vulnerabilities:**
   ```python
   # Replace string formatting with parameterized queries
   def query_cache_secure(self, where_params, sort_clause='fname ASC'):
       cursor = self.__db.cursor()
       # Build parameterized WHERE clause
       where_clause = " AND ".join(["fname LIKE ?"] + ["field LIKE ?" for field in where_params])
       sql = "SELECT file_id FROM all_data WHERE {} ORDER BY {}".format(where_clause, sort_clause)
       return cursor.execute(sql, tuple(where_params)).fetchall()
   ```

2. **Implement Path Validation:**
   ```python
   def validate_file_path(requested_path, allowed_base):
       real_path = os.path.realpath(requested_path)
       real_base = os.path.realpath(allowed_base)
       return real_path.startswith(real_base)
   ```

3. **Add Input Sanitization:**
   ```python
   def sanitize_parameter(value, param_type):
       if param_type == 'string':
           return re.sub(r'[<>&"\'`]', '', str(value))
       # Add other type validations
   ```

4. **Implement Credential Hashing:**
   ```python
   import hashlib
   import secrets
   
   def hash_password(password):
       salt = secrets.token_hex(16)
       return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
   ```

5. **Secure File Permissions:**
   ```python
   import os
   import stat
   
   def create_secure_file(filepath, content):
       # Create file with restrictive permissions
       with open(filepath, 'w') as f:
           f.write(content)
       os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)  # 600 permissions
   ```

### 5.2 Medium-term Improvements

1. **Add Rate Limiting**
2. **Implement Session Management**
3. **Add Certificate Validation**
4. **Improve Error Handling**

### 5.3 Long-term Security Enhancements

1. **Security Audit Logging**
2. **Intrusion Detection**
3. **Automated Security Testing**
4. **Security Configuration Validation**

## 6. Conclusion

The PicFrame application has several security vulnerabilities that should be addressed, particularly around file path validation, credential storage, and input sanitization. While the application includes some security features like optional authentication and SSL/TLS support, the implementation has significant gaps that could be exploited by attackers.

The most critical issues are the directory traversal vulnerability and plaintext credential storage, which should be addressed immediately. The application would benefit from a comprehensive security review and implementation of the recommended security controls.

**Overall Security Rating: High Risk**
- Critical SQL injection vulnerabilities present
- Multiple high-risk security issues requiring immediate attention
- Directory traversal and credential storage vulnerabilities
- Requires comprehensive security remediation before production deployment

**Priority Actions:**
1. **Immediate:** Fix SQL injection vulnerabilities in database queries
2. **Immediate:** Implement path validation for file operations
3. **High:** Encrypt or hash stored credentials
4. **High:** Add comprehensive input validation and sanitization
5. **Medium:** Implement proper file permissions and logging security