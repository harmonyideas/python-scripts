$(document).ready(function() {
    //elementid counter
    var gIdCounter = 0;
    var userId;

    function generateID(baseStr) {
        return (baseStr + gIdCounter++);
    }

    async function startFileTask(e) {
        e.preventDefault();

        // Get the total number of files to upload.
        const totalFiles = document.getElementById('files').files.length;

        // If there are no files to upload, return.
        if (totalFiles === 0) {
            return;
        }

        // Create a new FormData object to store the files and other data.
        const data = new FormData();

        // Append the user ID to the FormData object.
        data.append('userid', userId);

        // Get the file input element.
        const input = document.querySelector('input[type="file"]');

        // Iterate over the files and append them to the FormData object.
        for (let index = 0; index < totalFiles; index++) {
            // Generate a unique ID for the file upload job.
            const jobId = generateID('filejob');

            // Generate a unique ID for the progress element.
            const progressId = generateID('progress');

            // Append the file name, job ID, and progress ID to the FormData object.
            data.append(`file_uploads[${index}].name`, document.getElementById('files').files[index].name);
            data.append(`file_uploads[${index}].jobid`, jobId);
            data.append(`file_uploads[${index}].progressId`, progressId);

            // Append the file to the FormData object.
            data.append('file', input.files[index]);
            // Build status elements in HTML string
            const html = `
	    <div class="row">
	      <div id="${data.get(`file_uploads[${index}].jobid`)}">
                <div class="column">File: [ ${document.getElementById('files').files[index].name} ]</div>
	        <div class="column"><progress id="${data.get(`file_uploads[${index}].progressId`)}" max="100"></div>
	        <button type="button" class="collapsible">Show Results</button>
	        <div class="result" id="result"></div> 
	      </div>
	    </div>
	    <hr>
	    `;

            // Append the HTML string to the #filejob element
            $('#filejob').append(html);
        }

        // Start the file upload task by submitting the FormData object to the server.
        const response = await fetch('/upload', {
            method: 'POST',
            body: data,
        });

        // If the response is successful, update the status message.
        if (response.status === 202) {
            const taskIds = JSON.parse(await response.text()).task_ids;
            if (taskIds.length > 0) {
                $('#status').text('[ File(s) uploaded successfully. Task Started...]');
            } else {
                $('#status').text('[ Task ID not received - please check file extension]');
            }
        } else {
            $('#status').text('[An unexpected error has occured!]');
        }
    }


    function updateProgress(data) {
        // Update progress bar
        const percent = Math.floor(data.current / data.total * 100);
        document.getElementById(data.progressId).value = percent;

        // Update status
        //const statusElement = $('#' + data.filejobid).find("#" + 'statusId');
        //statusElement.text('Status: [' + data.status + ']');

        // Update progress
        const progressElement = $('#' + data.filejobid).find('.progressId');
        progressElement.text('Progress: [' + percent + '%]');

        // Show result if available
        if (data.result) {
            const resultElement = $('#' + data.filejobid).find('.result');
            resultElement.html('Result for file: ' + data.filepath + data.result);
        }
    }

    $(function() {
        $('#file_submit').click(startFileTask);
    });

    // Setup socketio functions
    var namespace = '/events'; // change to an empty string to use the global namespace
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + location.hostname + ':' + location.port + namespace);
    socket.on('connect', function(msg) {});
    // event handler for userid.  On initial connection, the server
    // sends back a unique userid
    socket.on('userid', function(msg) {
        userId = msg.userid;
    });
    // event handler for server sent celery status
    // the data is displayed in the "FileJob" section of the page
    socket.on('celerystatus', function(msg) {
        updateProgress(msg);
    });
    // event handler for server sent general status
    // the data is displayed in the "Status" section of the page
    socket.on('status', function(msg) {
        $('#status').text(msg.status);
    });
});
