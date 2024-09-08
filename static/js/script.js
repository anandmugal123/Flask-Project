function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.contains('dark-theme');
    body.classList.toggle('dark-theme', !isDark);
    body.classList.toggle('light-theme', isDark);
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

document.getElementById('csv_file').addEventListener('change', function() {
    const fileName = this.files[0].name;
    document.getElementById('file-selected').textContent = fileName;
});
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('csv_file');
    const fileSelectedSpan = document.getElementById('file-selected');
    const uploadForm = document.getElementById('uploadForm');
    const uploadButton = document.getElementById('uploadButton');
    const loadingSpinner = document.getElementById('loading');

    fileInput.addEventListener('change', () => {
        const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : 'No file chosen';
        fileSelectedSpan.textContent = fileName;
    });

    uploadForm.addEventListener('submit', (event) => {
        loadingSpinner.style.display = 'block';
        uploadButton.disabled = true;
        uploadButton.textContent = 'Uploading...';

        // Simulate a network request with setTimeout (remove in production)
        setTimeout(() => {
            loadingSpinner.style.display = 'none';
            uploadButton.disabled = false;
            uploadButton.textContent = 'Upload and Configure';
        }, 2000);
    });
});
