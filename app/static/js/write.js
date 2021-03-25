document.addEventListener('DOMContentLoaded', function () {
    const editor = new EditorJS({
        holder: 'editor',
        autofocus: true,
        placeholder: 'Curate an awesome article!',
        // readOnly: true, // tools Code doesn't support readOnly mode
        tools: {
            header: {
                class: Header,
                config: {
                    placeholder: 'Enter a title',
                    levels: [1, 2, 3],
                    defaultLevel: 1
                }
            },
            checklist: {
                class: Checklist,
                inlineToolbar: false,
            },
            list: {
                class: List,
                inlineToolbar: true,
            },
            quote: {
                class: Quote,
                inlineToolbar: true,
                shortcut: 'CMD+SHIFT+O',
                config: {
                    quotePlaceholder: 'Enter a quote',
                    captionPlaceholder: 'Quote\'s author',
                },
            },
            // delimeter: Delimeter,
            alert: {
                class: Alert,
                inlineToolbar: false,
                shortcut: 'CMD+SHIFT+A',
                config: {
                    defaultType: 'primary',
                    messagePlaceholder: 'Enter something',
                },
            },
            Marker: {
                class: Marker,
                shortcut: 'CMD+SHIFT+M',
            },
            image: {
                class: ImageTool,
                config: {
                    endpoints: {
                        byUrl: 'http://localhost:5000/story/fetch_url',
                        byFile: 'http://localhost:5000/story/upload_file',
                    }
                }
            },
            inlineCode: {
                class: InlineCode,
                config: {
                    foregroundColor: "green",
                    backgroundColor: "yellow"
                },
                shortcut: 'CMD+SHIFT+M',
            },
            underline: Underline,
        },
    });

    const publishButton = document.getElementById('publish');
    publishButton.addEventListener('click', async function () {
        const jsonData = await editor.save();
        console.log(jsonData);
    });
});
