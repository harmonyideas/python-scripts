$(document).ready(function () {
    //elementid counter
    var gIdCounter = 0;
    var userId;

    function generateID(baseStr) {
        return (baseStr + gIdCounter++);
    }

    function start_file_task(e) {
        e.preventDefault();
        var totalfiles = document.getElementById('files').files.length;
        if (totalfiles > 0) {
            //  get filename(s) for upload and append it for FormData object
            var data = new FormData();
            data.append("userid", userId);
            var input = document.querySelector('input[type="file"]');
            // Read selected files
            for (var index = 0; index < totalfiles; index++) {
                // add task status elements (figure out better method for handling array)
                data.append(`file_uploads[${index}].name`, document.getElementById('files').files[index].name);
                data.append(`file_uploads[${index}].jobid`, generateID("filejob"));
                data.append(`file_uploads[${index}].progressId`, generateID("progress"));
                data.append('file', input.files[index]);
                // build status elements in html string (needs cleanup)
                const cbutton = `<button type="button" class="collapsible">Show Results</button>`;
                const div = `<div class="row"><div id=${data.get(`file_uploads[${index}].jobid`)}>
                        <div class="column">File: [ ${document.getElementById('files').files[`${index}`].name} ]</div>
                        <div class="column">Waiting for results...</div>
                        <div class="column">Waiting for results...</div>
                        <div class="column"><progress id=${data.get(`file_uploads[${index}].progressId`)} max="100"></div>
                        ${cbutton}
                        <div class="result" id="result"></div> 
                        </div></div><hr>`;
                $('#filejob').append(div);
            }

            // send ajax POST request to start background job
            $.ajax({
                type: 'POST',
                url: '/upload',
                contentType: "application/json; charset=utf-8",
                data: data,
                processData: false,
                contentType: false,
                success: function (data, status, request) {
                    // Do something on successful file upload or with task ids
                    data.task_id.length > 0 ? 
                    $('#status').text("[ File(s) uploaded successfully. Task Started...]"):
                    $('#status').text("[ Task ID not received - please check file extension]");
                },
                error: function () {
                    $('#status').text("[An unexpected error has occured!]");;
                }
            });
        }
    }
    function updateProgress(data) {
      // Update the progress bar.
      const progressBar = document.getElementById(data.progressId);
      progressBar.value = parseInt(data.current / data.total * 100);

      // Update the status of the job.
      const statusElement = document.querySelector(`#${data.fileJobId} > .status`);
      statusElement.textContent = `Status: ${data.status}`;

      // Update the progress of the job.
      const progressElement = document.querySelector(`#${data.fileJobId} > .progress`);
      progressElement.textContent = `Progress: ${parseInt(data.current / data.total * 100)}%`;

      // If the job is finished, show the result.
      if ('result' in data) {
        const resultElement = document.querySelector(`#${data.fileJobId} > .result`);
        resultElement.textContent = `Result: ${data.result}`;
      }
    }

    function update_progress(data) {
        //update progress bar
        percent = parseInt(data['current'] * 100 / data['total']);
        document.getElementById(data.progressId).value = percent;
        var ele = $('#' + data.filejobid); //get parent elementid of <div> tag
        $(ele[0].childNodes[5]).text('Status: ' + "[" + data['status'] + "]");
        $(ele[0].childNodes[3]).text('Progress: ' + "[" + percent + '%' + "]");
        if ('result' in data) {
            // show result 
            $(ele[0].childNodes[11]).html('Result for file: ' + data['filepath'] + data['result']);
        }
    }

    $(function () {
        $('#csv_submit').click(start_file_task);
    });

    // Setup socketio functions
    var namespace = '/events'; // change to an empty string to use the global namespace
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + location.hostname + ':' + location.port + namespace);
    socket.on('connect', function (msg) { });
    // event handler for userid.  On initial connection, the server
    // sends back a unique userid
    socket.on('userid', function (msg) {
        userId = msg.userid;
    });
    // event handler for server sent celery status
    // the data is displayed in the "FileJob" section of the page
    socket.on('celerystatus', function (msg) {
        updateProgress(msg);
    });
    // event handler for server sent general status
    // the data is displayed in the "Status" section of the page
    socket.on('status', function (msg) {
        $('#status').text(msg.status);
    });
});
