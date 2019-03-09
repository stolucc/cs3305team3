function updateProfile() {
    var csrftoken = "{{ csrf_token() }}"
    /* This function updates the user profile when the edit button is pressed */
    document.getElementById("fieldset1").disabled  = false;//allow edits to form
    document.getElementById("submit_button").style.display = "inline";
    document.getElementById("edit_profile_button").style.display = "none";
    document.getElementById("fieldset1").style.backgroundColor = "#f2f2f2";
    document.getElementById("fieldset1").style.paddingTop = "1em";
    document.getElementById("fieldset1").style.paddingBottom = "1em";
    document.getElementById("fieldset1").style.marginLeft = "10em";
    document.getElementById("fieldset1").style.marginRight = "10em";
    document.getElementById("fieldset1").style.marginBottom = "1em";

}