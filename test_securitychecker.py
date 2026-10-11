
from securitychecker import check_failed_logins

# Test with 8 unsuccessful sign-in attempts
result = check_failed_logins(5)

print("Security Check Results")
print("----------------------")
print("Status:", result["status"])
print("Severity:", result["severity"])
print("Warning:", result["title"])
print("Explanation:", result["explanation"])
print("Recommended Action:", result["recommendation"])
