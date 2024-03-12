can_receive_from: dict[str, list[str]] = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["AB-", "AB+", "A+", "A-"],
    "A+": ["AB+", "A+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"]
}

can_donate_to: dict[str, list[str]] = {
    "O-": ["O-", "O+"],
    "O+": ["O+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-"],
    "AB+": ["AB+"]
}
