// Handle the image upload and convert to Base64
document.getElementById('imageUpload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const uploadedImage = document.getElementById('uploadedImage');
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = 'block'; // Show the image
        };
        reader.readAsDataURL(file);  // Read the image as Base64 string
    }
});

// Handle form submission and send the Base64 image to the backend
document.getElementById('imageForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    
    const file = document.getElementById('imageUpload').files[0];
    if (!file) {
        alert("Please select an image to upload.");
        return;
    }

    // Convert the image to Base64
    const reader = new FileReader();
    reader.onload = function(e) {
        const base64Image = e.target.result.split(',')[1]; // Remove data URL prefix

        // console.log(base64Image);  // Print the Base64 string

        // Send the Base64 string to the backend via a POST request
        fetch('http://localhost:5000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: base64Image,  // Send only the base64 string
            })
        })
        .then(response => response.json())
        .then(data => {
            // console.log('Success:', data);
            alert('Class: ' + data.class);
        })
        .catch((error) => {
            // console.error('Error:', error);
            alert('Error uploading image.');
        });
    };

    reader.readAsDataURL(file);  // Convert the image to Base64
});
