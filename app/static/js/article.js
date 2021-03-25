document.addEventListener('DOMContentLoaded', function () {
    const editor = new EditorJS({
        holder: 'editor',
        autofocus: true,
        // placeholder: 'Curate an awesome article!',
        readOnly: true, // tools Code doesn't support readOnly mode
        data: BlogContent, //temp parse from BE (write parser)
    });
});
