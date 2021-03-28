document.addEventListener('DOMContentLoaded', function () {
    const editor = new EditorJS({
        holder: 'editor',
        autofocus: true,
        placeholder: 'Curate an awesome article!',
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
                        byUrl: 'https://localhost:5000/story/fetch_url',
                        byFile: 'https://localhost:5000/story/upload_file',
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
        data: articleContent,
    });

    const saveButton = document.getElementById('save');
    saveButton.addEventListener('click', async function () {
        const jsonData = await editor.save();
        if (jsonData.blocks[0].type !== 'header') {
            alert('Your article should have a header as the first element. The header represents the title of the article.');
            return;
        }

        if (window.location.href.includes('edit')) {
            console.log('updating...')
            const storyId = window.location.href.split('/')[4];
            const response = await fetch(`${window.location.origin}/story/${storyId}`, {
                method: 'PUT',
                mode: 'cors',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });
            
            await response.json();
        } else {
            await fetch(`${window.location.origin}/new-story`, {
                method: 'POST',
                mode: 'cors',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });
        }
        setTimeout(function () {
            window.location.replace(`${window.location.origin}/stories`);
        }, 1000);
    });
});
