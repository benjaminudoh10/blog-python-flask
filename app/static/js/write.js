document.addEventListener('DOMContentLoaded', function () {
    const editor = new EditorJS({
        holder: 'editor',
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
                        byUrl: `${window.location.origin}/story/fetch_url`,
                        byFile: `${window.location.origin}/story/upload_file`,
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
    const modalContainer = document.getElementById('modal-container');
    const editorContainer = document.getElementById('editor-container');
    const titleInput = document.getElementById('article-title');
    const descInput = document.getElementById('article-desc');
    let editorData = {};
    saveButton.addEventListener('click', async () => {
        modalContainer.style.display = 'flex';
        editorData = await editor.save();
        console.log(editorData);
        modalContainer.classList.add('show');
        editorContainer.classList.add('no-event');
        
        const textBlocks = editorData.blocks.filter(block => {
            return block.type === 'header' || block.type === 'paragraph'
        });
        titleInput.value = textBlocks[0] && textBlocks[0]?.data?.text || '';
        descInput.value = textBlocks[1] && textBlocks[1]?.data?.text || '';
        return;
    });

    const closeButton = document.getElementById('close');
    closeButton.addEventListener('click', () => {
        modalContainer.classList.remove('show');
        editorContainer.classList.remove('no-event');
    });

    const publishButton = document.getElementById('publish');
    publishButton.addEventListener('click', async () => {
        const data = {
            title: titleInput.value || '',
            first_paragraph: descInput.value,
            draft: false,
            content: editorData,
        }

        await saveArticle(data);
    });

    const draftButton = document.getElementById('draft');
    draftButton.addEventListener('click', async () => {
        const data = {
            title: titleInput.value || '',
            first_paragraph: descInput.value,
            draft: true,
            content: editorData,
        }

        await saveArticle(data);
    });
});

async function saveArticle(data) {
    if (window.location.href.includes('edit')) {
        console.log('updating...')
        const storyId = window.location.href.split('/')[4];
        const response = await fetch(`${window.location.origin}/story/${storyId}`, {
            method: 'PUT',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        await response.json();
    } else {
        await fetch(`${window.location.origin}/new-story`, {
            method: 'POST',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
    }
    setTimeout(function () {
        window.location.replace(`${window.location.origin}/stories`);
    }, 1000);
}
