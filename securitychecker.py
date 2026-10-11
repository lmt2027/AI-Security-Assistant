
# AI Security Assistant
# Security Checker
# This file checks for possible security problems.


def check_failed_logins(failed_attempts):

    # Five or more failed attempts triggers a warning
    if failed_attempts >= 5:

        return {
            "status": "Warning",
            "severity": "High",
            "title": "Possible Password Attack",
            "explanation": (
                "Someone may be trying to guess "
                "an employee's password."
            ),
            "recommendation": (
                "Ask the employee if they recognize "
                "the sign-in attempts. If they do not, "
                "change the password and turn on "
                "extra sign-in protection."
            )
        }

    else:

        return {
            "status": "No Warning",
            "severity": "Low",
            "title": "No Unusual Sign-in Activity Found",
            "explanation": (
                "The number of unsuccessful sign-in "
                "attempts is below our warning level."
            ),
            "recommendation": (
                "Continue keeping an eye on "
                "account activity."
            )
        }
