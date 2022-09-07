function delete_note(e) {
    let note_title = e.getAttribute("note-title");

    let confirm_smg = confirm(`Do you want to delete '${note_title}'`)
    if (confirm_smg) {
        document.querySelector("#delete_form").submit()
    }
}
