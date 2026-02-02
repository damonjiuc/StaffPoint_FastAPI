const image_upload_handler = (blobInfo, progress) => new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = false;
    xhr.open('POST', '/api/upload-image/'); // твой API роут

    xhr.upload.onprogress = (e) => {
        progress(e.loaded / e.total * 100); // TinyMCE покажет прогресс
    };

    xhr.onload = () => {
        if (xhr.status === 403) {
            reject({ message: 'HTTP Error: ' + xhr.status, remove: true });
            return;
        }

        if (xhr.status < 200 || xhr.status >= 300) {
            reject('HTTP Error: ' + xhr.status);
            return;
        }

        let json;
        try {
            json = JSON.parse(xhr.responseText);
        } catch (err) {
            reject('Invalid JSON: ' + xhr.responseText);
            return;
        }

        if (!json || typeof json.location !== 'string') {
            reject('Invalid JSON: ' + xhr.responseText);
            return;
        }

        resolve(json.location); // ✅ TinyMCE вставит картинку
    };

    xhr.onerror = () => {
        reject('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
    };

    const formData = new FormData();
    formData.append('file', blobInfo.blob(), blobInfo.filename());

    xhr.send(formData);
});

document.addEventListener("DOMContentLoaded", () => {
    tinymce.init({
        selector: 'textarea[name="content"]',
        height: 600,
        menubar: "view insert format tools table",
        menu: {
            view: { title: "View", items: "code | visualaid | preview" },
            insert: { title: "Insert", items: "link image media template | charmap hr | anchor" },
            format: { title: "Format", items: "bold italic underline strikethrough | formats | removeformat" },
            tools: { title: "Tools", items: "spellchecker code" },
            table: { title: "Table", items: "inserttable | cell row column | tableprops deletetable" }
        },
        plugins: [
            "advlist", "autolink", "lists", "link", "image", "charmap",
            "print", "preview", "anchor", "searchreplace", "visualblocks",
            "code", "fullscreen", "insertdatetime", "media", "table",
            "paste", "help", "wordcount", "autosave", "emoticons",
            "codesample", "template"
        ],
        toolbar: [
            "undo redo | bold italic underline strikethrough | forecolor backcolor | fontsizeselect fontselect | bullist numlist | alignleft aligncenter | blockquote hr | link image media table template  | code "
        ],
        formats: {
            accent: { inline: "span", classes: "accent-color" }
        },
        branding: false,
        license_key: 'gpl',
        automatic_uploads: true,  // для drag&drop
        images_upload_handler: image_upload_handler
    });
});