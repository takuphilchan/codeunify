// This JavaScript script validates a user's input on a form before submission.

function validateForm(form) {
    let isValid = true;
    if (form.name.value === "") {
        alert("Name must be filled out");
        isValid = false;
    }
    if (form.email.value === "") {
        alert("Email must be filled out");
        isValid = false;
    }
    return isValid;
}

// Example usage of validation function
let form = {
    name: { value: "" },
    email: { value: "test@example.com" },
};
console.log(validateForm(form));  // Should return false due to empty name field
